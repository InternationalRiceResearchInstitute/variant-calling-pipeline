#!/usr/bin/env python

import sys, re, os
import os.path
from classes import CreateMergeBAMParams
from classes import writeFile

file = sys.argv[1]
disk = sys.argv[2]

params = CreateMergeBAMParams()
attributes = [attr for attr in dir(params) if not callable(getattr(params, attr)) and not attr.startswith("__")]

for line in open(params.fp):
	if re.findall(r'analysis_dir', line):
		params.analysis_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'input_dir', line):
		params.input_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'reference_dir', line):
		params.reference_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'scripts_dir', line):
		params.scripts_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'output_dir', line):
		params.output_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'email', line):
		params.email = line.split('=')[-1].rstrip()

	elif re.findall(r'partition', line):
		params.partition = line.split('=')[-1].rstrip()

for line in open(file):
	line = line.split(":")
	genome = line[0]

	path = params.analysis_dir + "/" + disk
	genomeFile = "submit_mergebam_slurm.sh"

	script = open(os.path.join(path, genomeFile), "w")
	path = params.analysis_dir + "/" + disk + "/" + genome
	genomeFile = genome + "-mergebam.sh"
	writeFile(script, os.path.join(path, genomeFile))
	script.close()

	merge_bam = open(os.path.join(path, genomeFile), "w")
	merge_bam.write("#!/bin/bash\n")
	merge_bam.write("\n")

	merge_bam.write("#SBATCH -J " + genome + "\n")
	merge_bam.write("#SBATCH -o " + genome + "-mergebam.%j.out\n")
	merge_bam.write("#SBATCH --cpus-per-task=6\n")
	merge_bam.write("#SBATCH --partition=" + partition + "\n")
	merge_bam.write("#SBATCH -e " + genome + "-mergebam.%j.error\n")
	merge_bam.write("#SBATCH --mail-user=" + email + "\n")
	merge_bam.write("#SBATCH --mail-type=begin\n")
	merge_bam.write("#SBATCH --mail-type=end\n")
	merge_bam.write("#SBATCH --requeue\n")
	merge_bam.write("\n")

	merge_bam.write("module samtools/1.0\n")
	merge_bam.write("\n")

	merge_bam.write("perl " + params.scripts_dir + "/mergebam.pl " + params.output_dir + genome + "\n")
	merge_bam.write("mv " + genome + "-sam2bam*.error " + genome + "-sam2bam.*.out " + params.analysis_dir + "/" + disk + "/" + genome + "/logs")
	merge_bam.close()
