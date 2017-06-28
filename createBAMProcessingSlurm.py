#!/usr/bin/env python

import sys, re, os
import os.path
from classes import CreateBAMProcessingParams
from classes import writeFile

file = sys.argv[1]
disk = sys.argv[2]

params = CreateBAMProcessingParams()
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

	elif re.findall(r'software_dir', line):
		params.software_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'tmp_dir', line):
		params.tmp_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'gatk', line):
		params.gatk = line.split('=')[-1].rstrip()

	elif re.findall(r'picard', line):
		params.picard = line.split('=')[-1].rstrip()

	elif re.findall(r'email', line):
		params.email = line.split('=')[-1].rstrip()

	elif re.findall(r'partition', line):
		params.partition = line.split('=')[-1].rstrip()

for line in open(file):
	line = line.split(":")
	genome = line[0]
	count = int(line[1]) / 2

	os.makedirs(params.analysis_dir + "/" + disk + "/" + genome + "/logs")
	
	path = params.analysis_dir + "/" + disk
	genomeFile = "submit_sam2bam_slurm.sh"

	script = open(os.path.join(path, genomeFile), "w")
	path = params.analysis_dir + "/" + disk + "/" + genome
	genomeFile = genome + "-sam2bam.sh"
	writeFile(script, os.path.join(path, genomeFile))
	script.close()

	sam_bam = open(os.path.join(path, genomeFile), "w")
	sam_bam.write("#!/bin/bash\n")
	sam_bam.write("\n")

	sam_bam.write("#SBATCH -J " + genome + "\n")
	sam_bam.write("#SBATCH -o " + genome + "-sam2bam.%j.out\n")
	sam_bam.write("#SBATCH --cpus-per-task=6\n")
	sam_bam.write("#SBATCH --array=1-" + str(count) + "\n")
	sam_bam.write("#SBATCH --partition=" + partition + "\n")
	sam_bam.write("#SBATCH -e -" + genome + "sam2bam.%j.error\n")
	sam_bam.write("#SBATCH --mail-user=" + email + "\n")
	sam_bam.write("#SBATCH --mail-type=begin\n")
	sam_bam.write("#SBATCH --mail-type=end\n")
	sam_bam.write("#SBATCH --requeue\n")
	sam_bam.write("\n")

	# sam_bam.write("module load python\n")
	sam_bam.write("module load jdk\n")
	sam_bam.write("filename=`find " + params.output_dir + "/" + genome + " -name \"*.sam\" | tail -n +\${SLURM_ARRAY_TASK_ID} | head -1`\n")
	sam_bam.write("\n")

	sam_bam.write("python " + params.scripts_dir + "/sam2bam.py -s \$filename -r " + params.reference_dir + " -p " + params.picard + " -g " + params.gatk +" -j " + params.jvm + " -t " + params.tmp_dir + "\n")
	sam_bam.write("mv " + genome + "-fq2sam.*.error " + genome + "-fq2sam.*.out " + params.analysis_dir + "/" + disk + "/" + genome + "/logs")
	sam_bam.close()
