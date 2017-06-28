#!/usr/bin/env python

import sys, re, os
import os.path
from classes import CreateAlignmentParams
from classes import writeFile

file_input = sys.argv[1]
disk = sys.argv[2]

params = CreateAlignmentParams()
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

for line in open(file_input):
	line = line.split(":")
	genome = line[0]
	count = int(line[1]) / 2

	os.makedirs(params.analysis_dir + "/" + disk + "/" + genome)
	os.makedirs(params.output_dir + "/" + genome)
	
	path = params.analysis_dir + "/" + disk
	genomeFile = "submit_slurm.sh"

	script = open(os.path.join(path, genomeFile), "w")
	path = params.analysis_dir + "/" + disk + "/" + genome
	genomeFile = genome + "-fq2sam.sh"
	writeFile(script, os.path.join(path, genomeFile))
	script.close()

	fq_sam = open(os.path.join(path, genomeFile), "w")
	fq_sam.write("#!/bin/bash\n")
	fq_sam.write("\n")

	fq_sam.write("#SBATCH -J " + genome + "-fq2sam\n")
	fq_sam.write("#SBATCH -o " + genome + "-fq2sam.%j.out\n")
	fq_sam.write("#SBATCH --cpus-per-task=8\n")
	fq_sam.write("#SBATCH --array=1-" + str(count) + "\n")
	fq_sam.write("#SBATCH --partition=" + partition + "\n")
	fq_sam.write("#SBATCH -e " + genome + "-fq2sam.%j.error\n")
	fq_sam.write("#SBATCH --mail-user=" + email + "\n")
	fq_sam.write("#SBATCH --mail-type=begin\n")
	fq_sam.write("#SBATCH --mail-type=end\n")
	fq_sam.write("#SBATCH --requeue\n")
	fq_sam.write("\n")

	fq_sam.write("module load bwa/0.7.10\n")
	# fq_sam.write("module load python/2.7.11\n")
	fq_sam.write("filename=`find " + params.input_dir + "/" + genome + " -name \"*1.fastq.gz\" | tail -n +\${SLURM_ARRAY_TASK_ID} | head -1`\n")
	fq_sam.write("\n")

	fq_sam.write("python " + params.scripts_dir + "/fq2sam.py -r " + params.reference_dir + " -p \$filename -o " + params.output_dir + " -t \$SLURM_CPUS_PER_TASK\n")
	fq_sam.close()
