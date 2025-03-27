#!/usr/bin/env python3
"""
SNPSnip - Interactive VCF filtering tool

This tool provides an interactive web interface for filtering VCF files
in multiple stages, with checkpointing to allow resuming sessions.
It can operate in both online (API-based) and offline (static HTML) modes.
"""

import argparse
import json
import logging
import os
import random
import subprocess
import sys
import tempfile
import threading
import shlex
import shutil
import time
import csv
import multiprocessing
import uuid
import base64
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union, Callable

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request, send_from_directory
from sklearn.decomposition import PCA
from waitress import serve
from tqdm import tqdm
import jinja2


from ._version import __version__, __version_tuple__
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("snpsnip")

# Standalone function for processing a region (needed for multiprocessing)
def process_region(region, input_file, temp_dir, pipeline_cmds, check=True, filters: List[str] = None, input_format: str = "-Ou", vcf_out: bool = True):
    """
    Process a single genomic region with bcftools.

    Args:
        region: Genomic region string (e.g. "chr1:1000-2000")
        input_file: Path to input VCF file
        temp_dir: Directory for temporary output
        pipeline_cmds: List of command lists to run in pipeline
        check: Whether to check return codes

    Returns:
        Path to output file or None if processing failed
    """
    region_safe = region.replace(":", "_").replace("-", "_")
    ext = "bcf" if vcf_out else "txt"
    region_output = os.path.join(temp_dir, f"region_{region_safe}.{ext}")

    if filters is None:
        filters = []
    # Construct the command for this region
    region_cmd = [["bcftools", "view", input_format, "-r", region,  *filters, input_file]] + pipeline_cmds
    if vcf_out:
        region_cmd.append(
            ["bcftools", "view", "-Ob1", "--write-index", "-o", region_output]
        )

    # Convert command lists to strings
    cmd_strings = [shlex.join(cmd) for cmd in region_cmd]
    full_cmd = " | ".join(cmd_strings)

    # Run the command
    logger.debug(f"Processing region {region}: {full_cmd}")
    try:
        if vcf_out:
            subprocess.run(full_cmd, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            with open(region_output, 'wb') as out_file:
                subprocess.run(full_cmd, shell=True, check=check, stdout=out_file, stderr=subprocess.PIPE)
        return region, region_output
    except subprocess.CalledProcessError as e:
        logger.error(f"Error processing region {region}: {e}")
        if e.stderr:
            logger.error(e.stderr)
        return region, None

# Constants
DEFAULT_PORT = 2790
DEFAULT_HOST = "localhost"
STATE_FILE = "snpsnip_state.json"
TEMP_DIR = "snpsnip_temp"
SUBSET_FREQ = 0.01

class SNPSnip:
    """Main class for SNP filtering application."""

    def __init__(self, args):
        """Initialize with command line arguments."""
        self.args = args
        self.vcf_file = args.vcf
        self.output_dir = Path(args.output_dir)
        self.processes = args.processes
        self.region_size = args.region_size
        self.offline_mode = args.offline
        self.next_file = args.next

        if args.state_file:
            self.state_file = Path(args.state_file)
        else:
            self.state_file = self.output_dir / "state.json"
        if args.temp_dir:
            self.temp_dir = Path(args.temp_dir)
        else:
            self.temp_dir = self.output_dir / "tmp"

        self.host = args.host
        self.port = args.port
        self.subset_freq = args.subset_freq

        # Initial filters
        self.maf = args.maf
        self.max_missing = args.max_missing
        self.min_qual = args.min_qual

        # State variables
        self.state = self._load_state() or {
            "stage": "init",
            "subset_vcf": None,
            "sample_stats": None,
            "variant_stats": None,
            "sample_groups": {},
            "filter_thresholds": {},
            "completed": False,
            "predefined_groups": {}
        }

        # If next file is provided, load it and update state
        if self.next_file and os.path.exists(self.next_file):
            self._load_next_file()

        # Load predefined groups if provided
        if args.groups_file:
            self._load_groups_from_file(args.groups_file, args.group_column, args.sample_column)

        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

        # Web app (only created in online mode)
        self.app = self._create_app() if not self.offline_mode else None
        self.server_thread = None

    def _load_state(self) -> Optional[Dict]:
        """Load state from state file if it exists."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse state file {self.state_file}")
                return None
        return None

    def _load_next_file(self):
        """Load data from a next file (downloaded from previous step)."""
        try:
            with open(self.next_file, 'r') as f:
                next_data = json.load(f)
                
            # Update state based on the stage
            if "groups" in next_data:
                # This is from sample filtering
                self.state["sample_groups"] = next_data["groups"]
                self.state["stage"] = "sample_filtered"
                logger.info(f"Loaded sample groups from {self.next_file}")
            elif "thresholds" in next_data:
                # This is from variant filtering
                self.state["filter_thresholds"] = next_data["thresholds"]
                self.state["stage"] = "ready_for_final"
                logger.info(f"Loaded variant thresholds from {self.next_file}")
            else:
                logger.warning(f"Unrecognized format in next file: {self.next_file}")
                
            self._save_state()
        except Exception as e:
            logger.error(f"Error loading next file {self.next_file}: {e}")
            raise

    def _save_state(self):
        """Save current state to state file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _load_groups_from_file(self, groups_file: str, group_column: str="group", sample_column: str = "sample"):
        """Load sample groups from a CSV or TSV file."""
        logger.info(f"Loading sample groups from {groups_file}")

        # Determine delimiter based on file extension
        delimiter = ',' if groups_file.lower().endswith('.csv') else '\t'

        groups = {}
        try:
            with open(groups_file, 'r') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                if sample_column not in reader.fieldnames and group_column not in reader.fieldnames:
                    logger.error(f"Groups file must contain '{sample_column}' and '{group_column}' columns. Found: {reader.fieldnames}")
                    return

                for row in reader:
                    try:
                        sample = row[sample_column]
                        group = row[group_column]
                        if group not in groups:
                            groups[group] = []
                        groups[group].append(sample)
                    except KeyError as e:
                        print(f"Strange line: {row}: {str(e)}")
                        raise e

            # Store all predefined groups
            self.state["predefined_groups"] = groups
            self.state["sample_groups"] = groups.copy()
            logger.info(f"Loaded {len(groups)} groups with {sum(len(samples) for samples in groups.values())} samples")
        except Exception as e:
            logger.error(f"Error loading groups file: {e}")
            raise e

    def _create_app(self) -> Flask:
        """Create Flask app for the web interface (online mode only)."""
        app = Flask(__name__,
                   static_folder=str(Path(__file__).parent / "static"),
                   template_folder=str(Path(__file__).parent / "templates"))

        @app.route('/')
        def index():
            return render_template('index.html', state=self.state, offline_mode=False)

        @app.route('/api/state')
        def get_state():
            # Filter out predefined groups with no samples
            state_copy = self.state.copy()
            if "predefined_groups" in state_copy:
                state_copy["predefined_groups"] = {
                    group: samples for group, samples in state_copy["predefined_groups"].items() 
                    if samples
                }
            if "sample_groups" in state_copy:
                state_copy["sample_groups"] = {
                    group: samples for group, samples in state_copy["sample_groups"].items() 
                    if samples
                }
            return jsonify(state_copy)

        @app.route('/api/sample_stats')
        def get_sample_stats():
            if self.state["sample_stats"]:
                return jsonify(self.state["sample_stats"])
            return jsonify({"error": "Sample stats not available"}), 404

        @app.route('/api/variant_stats/<group>')
        def get_variant_stats(group):
            if group in self.state.get("variant_stats", {}):
                return jsonify(self.state["variant_stats"][group])
            return jsonify({"error": f"Variant stats for group {group} not available"}), 404

        @app.route('/api/pca')
        def get_pca():
            if "pca" in self.state:
                return jsonify(self.state["pca"])
            return jsonify({"error": "PCA not available"}), 404

        @app.route('/api/submit_sample_filters', methods=['POST'])
        def submit_sample_filters():
            data = request.json
            self.state["sample_groups"] = data["groups"]
            self.state["stage"] = "sample_filtered"
            self._save_state()

            # Process variant stats for each group
            self._process_variant_stats()

            return jsonify({"success": True})

        @app.route('/api/submit_variant_filters', methods=['POST'])
        def submit_variant_filters():
            data = request.json
            self.state["filter_thresholds"] = data["thresholds"]
            self.state["stage"] = "ready_for_final"
            self._save_state()

            # Apply final filters
            self._apply_final_filters()

            return jsonify({"success": True, "output_files": self.state.get("output_files", [])})

        return app
        
    def _generate_static_html(self, stage):
        """Generate static HTML file with embedded data for offline mode."""
        template_path = Path(__file__).parent / "templates" / "index.html"
        
        # Load the template
        with open(template_path, 'r') as f:
            template_content = f.read()
            
        # Create Jinja2 environment and template
        env = jinja2.Environment()
        template = env.from_string(template_content)
        
        # Prepare data to embed in the HTML
        embedded_data = {
            "offline_mode": True,
            "stage": stage
        }
        
        if stage == "ready_for_sample_filtering":
            # Embed sample stats and PCA data
            embedded_data["sample_stats"] = self.state["sample_stats"]
            embedded_data["pca"] = self.state["pca"]
            
            # Filter out predefined groups with no samples
            predefined_groups = {
                group: samples for group, samples in self.state.get("predefined_groups", {}).items() 
                if samples
            }
            sample_groups = {
                group: samples for group, samples in self.state.get("sample_groups", {}).items() 
                if samples
            }
            embedded_data["predefined_groups"] = predefined_groups
            embedded_data["sample_groups"] = sample_groups
            output_file = self.output_dir / "sample_filtering.html"
            
        elif stage == "ready_for_variant_filtering":
            # Embed variant stats and sample groups
            embedded_data["sample_groups"] = self.state["sample_groups"]
            embedded_data["variant_stats"] = self.state["variant_stats"]
            output_file = self.output_dir / "variant_filtering.html"
        elif stage == "completed":
            # No html output for completion
            return None
        else:
            logger.error(f"Unknown stage for static HTML generation: {stage}")
            return None
            
        # Render the template with embedded data
        html_content = template.render(
            state=self.state,
            offline_mode=True,
            embedded_data=json.dumps(embedded_data)
        )
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(html_content)
            
        logger.info(f"Generated static HTML file: {output_file}")
        return output_file

    def run(self):
        """Main execution flow."""
        if self.state["stage"] == "init":
            logger.info("Starting initial processing...")
            self._create_snp_subset()
            self._compute_sample_stats()
            self._compute_pca()
            self.state["stage"] = "ready_for_sample_filtering"
            self._save_state()

        if self.state["stage"] == "sample_filtered":
            logger.info("Processing variant statistics...")
            self._process_variant_stats()
            self._save_state()

        if self.state["stage"] == "ready_for_final" and not self.state.get("completed", False):
            logger.info("Applying final filters...")
            self._apply_final_filters()
            self.state["completed"] = True
            self._save_state()

        # Handle offline or online mode
        if self.offline_mode:
            self._handle_offline_mode()
        else:
            # Start web server if not completed in online mode
            if not self.state.get("completed", False):
                self._start_web_server()
            else:
                logger.info("Processing completed. Output files:")
                for file in self.state.get("output_files", []):
                    logger.info(f"  - {file}")
                    
    def _handle_offline_mode(self):
        """Handle offline mode by generating appropriate static HTML files."""
        if self.state["stage"] == "ready_for_sample_filtering":
            # Generate HTML for sample filtering
            html_file = self._generate_static_html("ready_for_sample_filtering")
            logger.info(f"Generated sample filtering HTML: {html_file}")
            logger.info("Open this file in a browser, make your selections, and download the JSON file.")
            logger.info("Then run: snpsnip --vcf <vcf_file> --offline --next <downloaded_json>")
            
        elif self.state["stage"] == "ready_for_variant_filtering":
            # Generate HTML for variant filtering
            html_file = self._generate_static_html("ready_for_variant_filtering")
            logger.info(f"Generated variant filtering HTML: {html_file}")
            logger.info("Open this file in a browser, make your selections, and download the JSON file.")
            logger.info("Then run: snpsnip --vcf <vcf_file> --offline --next <downloaded_json>")
            
        elif self.state.get("completed", False):
            # Generate completion HTML
            logger.info("Processing completed. Output files:")
            for file in self.state.get("output_files", []):
                logger.info(f"  - {file}")

    def _start_web_server(self):
        """Start the web server in a separate thread."""
        def run_server():
            logger.info(f"Starting web server at http://{self.host}:{self.port}")
            serve(self.app, host=self.host, port=self.port)

        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        try:
            # Keep running until processing is completed
            while self.server_thread.is_alive() and not self.state.get("completed", False):
                time.sleep(1)

            if self.state.get("completed", False):
                logger.info("Processing completed. Shutting down server...")
                # Give a moment for any final requests to complete
                time.sleep(2)
                sys.exit(0)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            sys.exit(0)

    def _run_pipeline(self, cmds: List[List[str]], check: bool = True, stdout=subprocess.PIPE) -> subprocess.CompletedProcess:
        cmds = [shlex.join(c) for c in cmds]
        shellcmd = " | ".join(cmds)
        logger.info(f"Running: {shellcmd}")
        proc =  subprocess.run(shellcmd, shell=True, text=True, stdout=stdout, stderr=subprocess.PIPE, check=False)
        try:
            if check:
                proc.check_returncode()
            return proc
        except subprocess.CalledProcessError as exc:
            logger.error(proc.stderr)
            raise exc

    def _run_bcftools(self, cmd: List[str], check: bool = True, stdout=subprocess.PIPE) -> subprocess.CompletedProcess:
        """Run a bcftools command."""
        full_cmd = ["bcftools"] + cmd
        return self._run_pipeline([full_cmd,], check=check, stdout=stdout)

    def run_bcftools_pipeline(self,
                             input_file: str,
                             output_file: str,
                             pipeline_cmds: List[List[str]],
                             merge_cmd: List[str] = None,
                             filters: List[str] = None,
                             input_format: str = "-Ou",
                             out_format: str = "-Oz",
                             processes: int = None,
                             check: bool = True) -> None:
        """
        Run a BCFtools pipeline in parallel by processing regions separately.

        Args:
            input_file: Path to input VCF/BCF file
            output_file: Path to output file
            pipeline_cmds: List of commands to run in a pipeline
            merge_cmd: Command to merge region outputs (defaults to bcftools concat for VCF, cat for text)
            processes: Number of parallel processes (defaults to CPU count)
            check: Whether to check return codes

        Returns:
            None
        """
        if processes is None:
            processes = self.processes if hasattr(self, 'processes') else max(1, multiprocessing.cpu_count() - 1)

        # Create a temporary directory for region outputs
        temp_dir = Path(self.temp_dir) / f"regions_{uuid.uuid4().hex}"
        temp_dir.mkdir(exist_ok=True)
        temp_dir_str = str(temp_dir)
        logger.info(f"Running {' | '.join(shlex.join(x) for x in pipeline_cmds)} in parallel")

        # Get list of chromosomes and their lengths
        contigs_cmd = ["bcftools", "index", "--stats", input_file]
        logger.debug(f"Getting contigs: {shlex.join(contigs_cmd)}")
        result = subprocess.run(contigs_cmd, text=True, capture_output=True, check=check)

        regions = []
        for line in result.stdout.strip().split('\n'):
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                try:
                    chrom = parts[0]
                    length = int(parts[1])
                except ValueError as exc:
                    print(f"ERROR parsing chrom length from vcf header: {line}")
                    regions.append(chrom)
                    continue

                # Create regions of specified size
                region_size = self.region_size if hasattr(self, 'region_size') else 1000000
                for start in range(1, length, region_size):
                    end = min(start + region_size - 1, length)
                    regions.append(f"{chrom}:{start}-{end}")

        if filters is None:
            filters = []
        if not regions:
            logger.warning("No regions found in the VCF file")
            # Fall back to running without regions
            with open(output_file, 'w') as fh:
                self._run_pipeline([["bcftools", "view", input_format, input_file, *filters]] + pipeline_cmds, check=check, stdout=fh)
            return

        logger.info(f"Processing {len(regions)} regions with {processes} processes")

        # Determine merge command if not provided
        is_vcf = any(output_file.endswith(ext) for ext in ['.vcf', '.vcf.gz', '.bcf'])
        if merge_cmd is None:
            # Check if output is likely VCF or text
            if is_vcf:
                merge_cmd = ["bcftools", "concat", "--allow-overlaps", "--verbose", "0", out_format, "--threads", str(processes), "--write-index", "-o", output_file]
            else:
                merge_cmd = ["cat"]

        # Process regions in parallel using the standalone function
        region_outputs = {}
        with ProcessPoolExecutor(max_workers=processes) as executor:
            # Create a list of arguments for each region
            futures = [
                executor.submit(process_region, region, input_file, temp_dir_str, pipeline_cmds, check, filters=filters, input_format=input_format, vcf_out=is_vcf)
                for region in regions
            ]

            # Collect results as they complete
            for future in tqdm(futures, total=len(futures), desc="Parallel VCF Processing", unit="region"):
                region, result = future.result()
                if result:
                    region_outputs[region]=str(result)

        if not region_outputs:
            logger.error("All region processing failed")
            return

        # Merge the region outputs
        merge_cmd_str = shlex.join(merge_cmd)
        if not is_vcf and merge_cmd == ["cat"]:
            # For text outputs, just concatenate
            logger.debug("Merging outputs with simple concatenation")
            with open(output_file, 'wb') as out_file:
                for region in regions:
                    region_file = region_outputs[region]
                    with open(region_file, 'rb') as in_file:
                        shutil.copyfileobj(in_file, out_file)
        else:
            # For VCF outputs, use the provided merge command
            for region in regions:
                region_file = region_outputs[region]
                merge_cmd.append(region_file)
            logger.debug(f"Merging outputs: {shlex.join(merge_cmd)}")
            subprocess.run(merge_cmd, check=check)
            if not Path(output_file + ".csi").exists():
                logger.debug("Merging did not create an index, so I have to make one...")
                subprocess.run(["bcftools", "index", "-f", output_file], check=check)

        # Clean up temporary files
        for file_path in region_outputs:
            try:
                os.remove(file_path)
            except OSError as e:
                logger.debug(f"Failed to remove temporary file {file_path}: {e}")
        try:
            os.rmdir(temp_dir)
        except OSError as e:
            logger.debug(f"Failed to remove temporary directory {temp_dir}: {e}")

    def _create_snp_subset(self):
        """Create a random subset of SNPs passing basic filters."""
        logger.info("Creating SNP subset...")

        # Create initial filter string
        filters = []
        if self.maf:
            filters.append(f"MAF>{self.maf}")
        if self.max_missing:
            filters.append(f"F_MISSING<{self.max_missing}")
        if self.min_qual:
            filters.append(f"QUAL>{self.min_qual}")
        filter_str = " && ".join(filters) if filters else None
        filters = ["-i", filter_str] if filter_str else []

        filled_vcf = str(self.temp_dir / "subset_filled.vcf.gz")
        commands = [
           ["awk", f'/^#/ {{print; next}} {{if (rand() < {self.subset_freq}) print}}'],
           ["bcftools", "+fill-tags", '-Ou', "--", "-t", "all,F_MISSING,DP:1=int(sum(FORMAT/DP))"]
        ]
        self.run_bcftools_pipeline(
            input_file=self.vcf_file,
            output_file=filled_vcf,
            pipeline_cmds=commands,
            filters=filters,
            input_format="-Ov",
        )

        self.state["subset_vcf"] = filled_vcf

    def _compute_sample_stats(self):
        """Compute per-sample statistics."""
        logger.info("Computing sample statistics...")

        subset_vcf = self.state["subset_vcf"]

        # Get sample names
        samples_result = self._run_bcftools(["query", "-l", subset_vcf])
        samples = samples_result.stdout.strip().split('\n')

        # Compute per-sample missingness
        missing_file = str(self.temp_dir / "vcf_stats.txt")

        # Use parallel processing for stats calculation
        self.run_bcftools_pipeline(
            input_file=subset_vcf,
            output_file=missing_file,
            pipeline_cmds=[["bcftools", "stats", "-s", "-"]],
            merge_cmd=["cat"],
        )

        # Parse stats files
        sample_stats = {sample: {"id": sample} for sample in samples}

        # Process missing data
        try:
            with open(missing_file, 'r') as f:
                for line in f:
                    if line.startswith("PSC"):
                        parts = line.strip().split('\t')
                        sample = parts[2]
                        nrefhom, nalthom, nhet, nts, ntv, nindel, mean_depth, nsingle, nhapref, nhapalt, nmissing = map(float, parts[3:14])
                        ncall = nrefhom + nalthom + nhet + nindel + nsingle + nhapref + nhapalt
                        missing_rate = nmissing / ncall if ncall > 0 else 0
                        # Calculate heterozygosity rate
                        het_rate = nhet / ncall if ncall > 0 else 0
                        if sample in sample_stats:
                            sample_stats[sample]["missing_rate"] = missing_rate
                            sample_stats[sample]["mean_depth"] = mean_depth
                            sample_stats[sample]["het_rate"] = het_rate
        except Exception as e:
            logger.error(f"Error processing missing data: {e}")
            raise e

        self.state["sample_stats"] = list(sample_stats.values())

    def _compute_pca(self):
        """Compute PCA for samples."""
        logger.info("Computing PCA...")

        subset_vcf = self.state["subset_vcf"]

        # Extract genotypes as a matrix
        geno_file = str(self.temp_dir / "genotypes.txt")

        # Use parallel processing for genotype extraction
        self.run_bcftools_pipeline(
            input_file=subset_vcf,
            output_file=geno_file,
            pipeline_cmds=[["bcftools", "query", "-f", "[%GT\t]\n"]],
            merge_cmd=["cat"],
            check=False
        )

        # Get sample names
        samples_result = self._run_bcftools(["query", "-l", subset_vcf])
        samples = samples_result.stdout.strip().split('\n')

        # Parse genotype matrix
        try:
            # Read genotype data
            geno_matrix = []
            with open(geno_file, 'r') as f:
                for line in f:
                    row = []
                    for gt in line.strip().split('\t'):
                        # Convert genotype to numeric value (0, 1, 2)
                        if gt in ("0/0", "0|0"):
                            row.append(0)
                        elif gt in ("0/1", "0|1", "1|0", "1/0"):
                            row.append(1)
                        elif gt in ("1/1", "1|1"):
                            row.append(2)
                        else:
                            row.append(np.nan)  # Missing or other genotypes
                    geno_matrix.append(row)

            # Convert to numpy array
            geno_array = np.array(geno_matrix, dtype=float).T  # Transpose to have samples as rows

            # Impute missing values with mean
            for i in range(geno_array.shape[0]):
                mask = np.isnan(geno_array[i])
                if mask.any():
                    valid = ~mask
                    if valid.any():
                        geno_array[i, mask] = np.mean(geno_array[i, valid])
                    else:
                        geno_array[i, mask] = 0

            # Run PCA
            pca = PCA(n_components=2)
            pca_result = pca.fit_transform(geno_array)

            # Format PCA results
            pca_data = []
            for i, sample in enumerate(samples):
                pca_data.append({
                    "sample": sample,
                    "pc1": float(pca_result[i, 0]),
                    "pc2": float(pca_result[i, 1])
                })

            self.state["pca"] = pca_data

        except Exception as e:
            logger.error(f"Error computing PCA: {e}")
            self.state["pca"] = []
            raise e

    def _process_variant_stats(self):
        """Process variant statistics for each sample group."""
        logger.info("Processing variant statistics for each sample group...")

        subset_vcf = self.state["subset_vcf"]
        sample_groups = self.state["sample_groups"]

        if not sample_groups:
            logger.warning("No sample groups defined")
            return

        self.state["variant_stats"] = {}

        for group_name, samples in sample_groups.items():
            if len(samples) < 1:
                logger.info(f"Skipping empty group: {group_name}")
                continue

            logger.info(f"Processing group: {group_name} with {len(samples)} samples")

            # Create a temporary file with sample names
            sample_file = str(self.temp_dir / f"{group_name}_samples.txt")
            with open(sample_file, 'w') as f:
                for sample in samples:
                    f.write(f"{sample}\n")

            # Create a subset VCF with only these samples
            group_vcf = str(self.temp_dir / f"{group_name}_subset.vcf.gz")

            # Use parallel processing for sample subsetting
            self.run_bcftools_pipeline(
                input_file=subset_vcf,
                output_file=group_vcf,
                pipeline_cmds=[
                    ["bcftools", "view", "-S", sample_file],
                    ["bcftools", "+fill-tags", '-Ou', "--", "-t", "all,F_MISSING,DP:1=int(sum(FORMAT/DP))"]
                ],
            )

            # Compute variant statistics
            stats = {}

            # Quality
            qual_file = str(self.temp_dir / f"{group_name}_qual.txt")
            self.run_bcftools_pipeline(
                input_file=group_vcf,
                output_file=qual_file,
                pipeline_cmds=[["bcftools", "query", "-f", "%QUAL\n"]],
                merge_cmd=["cat"],
                check=False
            )

            # Depth
            depth_file = str(self.temp_dir / f"{group_name}_depth.txt")
            self.run_bcftools_pipeline(
                input_file=group_vcf,
                output_file=depth_file,
                pipeline_cmds=[["bcftools", "query", "-f", "%INFO/DP\n"]],
                merge_cmd=["cat"],
                check=False
            )

            # Allele frequency
            af_file = str(self.temp_dir / f"{group_name}_af.txt")
            self.run_bcftools_pipeline(
                input_file=group_vcf,
                output_file=af_file,
                pipeline_cmds=[["bcftools", "query", "-f", "%INFO/AF\n"]],
                merge_cmd=["cat"],
                check=False
            )

            # Missing rate
            missing_file = str(self.temp_dir / f"{group_name}_missing.txt")
            self.run_bcftools_pipeline(
                input_file=group_vcf,
                output_file=missing_file,
                pipeline_cmds=[["bcftools", "query", "-f", "%F_MISSING\n"]],
                merge_cmd=["cat"],
                check=False
            )
            
            # Excess Heterozygosity
            exhet_file = str(self.temp_dir / f"{group_name}_exhet.txt")
            self.run_bcftools_pipeline(
                input_file=group_vcf,
                output_file=exhet_file,
                pipeline_cmds=[["bcftools", "query", "-f", "%INFO/ExcHet\n"]],
                merge_cmd=["cat"],
                check=False
            )

            # Parse statistics files
            try:
                # Quality
                quals = []
                with open(qual_file, 'r') as f:
                    for line in f:
                        try:
                            quals.append(float(line.strip()))
                        except ValueError:
                            pass
                stats["qual"] = self._compute_histogram(quals)

                # Depth
                depths = []
                with open(depth_file, 'r') as f:
                    for line in f:
                        try:
                            depths.append(float(line.strip()))
                        except ValueError:
                            pass
                stats["depth"] = self._compute_histogram(depths)

                # Allele frequency
                afs = []
                with open(af_file, 'r') as f:
                    for line in f:
                        try:
                            afs.append(float(line.strip()))
                        except ValueError:
                            pass
                stats["af"] = self._compute_histogram(afs)

                # Missing rate
                missing_rates = []
                with open(missing_file, 'r') as f:
                    for line in f:
                        try:
                            missing_rates.append(float(line.strip()))
                        except ValueError:
                            pass
                stats["missing"] = self._compute_histogram(missing_rates)
                
                # Excess Heterozygosity - transform to -log10 scale
                exhet_values = []
                with open(exhet_file, 'r') as f:
                    for line in f:
                        try:
                            value = float(line.strip())
                            if value > 0:  # Avoid log of zero or negative values
                                # Convert to -log10 scale
                                exhet_values.append(-np.log10(value))
                        except ValueError:
                            pass
                stats["exhet"] = self._compute_histogram(exhet_values)

                self.state["variant_stats"][group_name] = stats

            except Exception as e:
                logger.error(f"Error processing variant stats for group {group_name}: {e}")
                raise e

        self.state["stage"] = "ready_for_variant_filtering"
        self._save_state()

    def _compute_histogram(self, values, bins=50, use_percentiles=True):
        """Compute histogram for a list of values.
        
        Args:
            values: List of values to histogram
            bins: Number of bins to use
            use_percentiles: If True, limit range to 0.1-99.9 percentiles to avoid outliers
        """
        if not values:
            return {"bins": [], "counts": []}
            
        if use_percentiles and len(values) > 10:
            # Use percentiles to avoid extreme outliers expanding the range
            low = np.percentile(values, 0.1)
            high = np.percentile(values, 99.9)
            # Filter values to be within this range for the histogram
            filtered_values = [v for v in values if low <= v <= high]
            hist, bin_edges = np.histogram(filtered_values, bins=bins, range=(low, high))
        else:
            hist, bin_edges = np.histogram(values, bins=bins)
            
        return {
            "bins": bin_edges[:-1].tolist(),
            "counts": hist.tolist()
        }

    def _apply_final_filters(self):
        """Apply final filters to the full VCF file."""
        logger.info("Applying final filters to the full VCF file...")

        sample_groups = self.state["sample_groups"]
        filter_thresholds = self.state["filter_thresholds"]

        output_files = []

        for group_name, samples in sample_groups.items():
            if len(samples) < 1:
                logger.info(f"Skipping empty group: {group_name}")
                continue
            logger.info(f"Processing group: {group_name}")

            # Create a temporary file with sample names
            sample_file = str(self.temp_dir / f"{group_name}_samples.txt")
            with open(sample_file, 'w') as f:
                for sample in samples:
                    f.write(f"{sample}\n")

            # Get filter thresholds for this group
            group_filters = filter_thresholds.get(group_name, {})
            filter_expressions = []

            if "qual" in group_filters:
                min_qual = group_filters["qual"].get("min")
                max_qual = group_filters["qual"].get("max")
                if min_qual is not None:
                    filter_expressions.append(f"QUAL>={min_qual}")
                if max_qual is not None:
                    filter_expressions.append(f"QUAL<={max_qual}")

            if "depth" in group_filters:
                min_depth = group_filters["depth"].get("min")
                max_depth = group_filters["depth"].get("max")
                if min_depth is not None:
                    filter_expressions.append(f"INFO/DP>={min_depth}")
                if max_depth is not None:
                    filter_expressions.append(f"INFO/DP<={max_depth}")

            if "af" in group_filters:
                min_af = group_filters["af"].get("min")
                max_af = group_filters["af"].get("max")
                if min_af is not None:
                    filter_expressions.append(f"INFO/AF>={min_af}")
                if max_af is not None:
                    filter_expressions.append(f"INFO/AF<={max_af}")

            if "missing" in group_filters:
                min_missing = group_filters["missing"].get("min")
                max_missing = group_filters["missing"].get("max")
                if min_missing is not None:
                    filter_expressions.append(f"F_MISSING>={min_missing}")
                if max_missing is not None:
                    filter_expressions.append(f"F_MISSING<={max_missing}")
                    
            if "exhet" in group_filters:
                min_exhet = group_filters["exhet"].get("min")
                max_exhet = group_filters["exhet"].get("max")
                if min_exhet is not None:
                    # Convert from -log10 scale back to p-value
                    p_value = 10 ** (-min_exhet)
                    filter_expressions.append(f"INFO/ExcHet<={p_value}")
                if max_exhet is not None:
                    # Convert from -log10 scale back to p-value
                    p_value = 10 ** (-max_exhet)
                    filter_expressions.append(f"INFO/ExcHet>={p_value}")

            # Add initial filters
            if self.maf:
                filter_expressions.append(f"MAF>{self.maf}")
            if self.max_missing:
                filter_expressions.append(f"F_MISSING<{self.max_missing}")
            if self.min_qual:
                filter_expressions.append(f"QUAL>{self.min_qual}")

            # Combine filter expressions
            filter_str = " && ".join(filter_expressions) if filter_expressions else None

            # Output file path
            output_file = os.path.join(self.output_dir, f"{group_name}_filtered.vcf.gz")

            # Apply filters and extract samples
            filter_samples = ["-S", sample_file, ]
            pipeline_cmds = [
                ["bcftools", "+fill-tags", '-Ou', "--", "-t", "all,F_MISSING,DP:1=int(sum(FORMAT/DP))"],
            ]

            if filter_str:
                # NB: this has to happen after the initial filtering by
                # samples in a separate bcftools view cmd, as the filter
                # thresholds have to be updated by fill_tags first.
                view_cmd = ["bcftools", "view", "-Ou", "-i", filter_str]
                pipeline_cmds.append(view_cmd)
                logger.info(f"Running filter command: {shlex.join(view_cmd)}")

            # Use parallel processing for final filtering
            self.run_bcftools_pipeline(
                input_file=self.vcf_file,
                filters=filter_samples,
                output_file=output_file,
                pipeline_cmds=pipeline_cmds,
                check=True,
            )

            output_files.append(output_file)

        self.state["output_files"] = output_files
        self.state["completed"] = True
        self._save_state()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SNPSnip - Interactive VCF filtering tool", prog="snpsnip")

    # Input/output options
    parser.add_argument("--vcf", required=True, help="Input VCF/BCF file (must be indexed)")
    parser.add_argument("--output-dir", default=".", help="Output directory for filtered VCFs")
    parser.add_argument("--state-file", help="State file for checkpointing")
    parser.add_argument("--temp-dir", help="Directory for temporary files")

    # Web server options
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host to bind the web server to")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port for the web server")

    # Offline mode options
    parser.add_argument("--offline", action="store_true", help="Run in offline mode (generate static HTML)")
    parser.add_argument("--next", help="JSON file with selections from previous step (for offline mode)")

    # Initial filtering options
    parser.add_argument("--maf", type=float, help="Minimum minor allele frequency")
    parser.add_argument("--max-missing", type=float, help="Maximum missingness rate")
    parser.add_argument("--min-qual", type=float, help="Minimum variant quality")
    parser.add_argument("--subset-freq", type=float, default=SUBSET_FREQ,
                       help="Fraction of SNPs to sample for interactive analysis")
    parser.add_argument("--groups-file", help="CSV or TSV file with sample and group columns for predefined groups")
    parser.add_argument("--group-column", default="group", help="Column in CSV or TSV file for predefined groups")
    parser.add_argument("--sample-column", default="sample", help="CSV or TSV file for sample")
    parser.add_argument("--processes", type=int, default=max(1, multiprocessing.cpu_count() - 1),
                       help="Number of parallel processes to use")
    parser.add_argument("--region-size", type=int, default=1_000_000,
                       help="Size of each parallel region")

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.vcf):
        logger.error(f"Input VCF file not found: {args.vcf}")
        sys.exit(1)

    # Check if bcftools is available
    try:
        subprocess.run(["bcftools", "--version"], check=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.error("bcftools not found. Please install bcftools and make sure it's in your PATH.")
        sys.exit(1)

    # Run the application
    app = SNPSnip(args)
    app.run()

if __name__ == "__main__":
    main()
