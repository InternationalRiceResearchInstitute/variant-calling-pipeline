#!/usr/bin/env python

import sys, re, os
import os.path
from classes import CreateAlignmentParams
from classes import writeFile

# get the genome file
input_file = sys.argv[1]
disk = sys.argv[2]

# get the parameters in the class CreateAlignmentParams
params = CreateAlignmentParams()
attributes = [attr for attr in dir(params) if not callable(getattr(params, attr)) and not attr.startswith("__")]

# reads the config file and get the respective values for each
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

	elif re.findall(r'partition=', line):
		params.partition = line.split('=')[-1].rstrip()

	elif re.findall(r'bwas=', line):
		params.bwa = line.split('=')[-1].rstrip()

# reads the file containing the genome
for line in open(input_file):
	line = line.split(":")
	genome = line[0]

	# get its half for job array limit
	count = int(line[1]) / 2

	# create a directory for each genome
	os.makedirs(params.analysis_dir + "/" + disk + "/" + genome)
	os.makedirs(params.output_dir + "/" + genome)
	
	# directory where slurm script will store
	path = params.analysis_dir + "/" + disk + "/"
	slurm_file = "submit_slurm.sh"
	exec_file = os.path.join(path, slurm_file)

	output_path = params.analysis_dir + "/" + disk + "/" + genome + "/"
	fqsam_file = genome + "-fq2sam.slurm"
	output_file = os.path.join(output_path, fqsam_file)

	# creates a submit shell script between job submission
	# to prevent timeout
	script = open(exec_file, "w")
	script.write("#!/bin/bash\n")
	script.write("\n")
	script.write("sbatch " + output_file  + "\n")
	script.write("sleep 10m\n")
	script.close()

	# creates slurm script
	fqsam = open(output_file, "w")
	fqsam.write("#!/bin/bash\n")
	fqsam.write("\n")

	fqsam.write("#SBATCH -J " + genome + "-fq2sam\n")
	fqsam.write("#SBATCH -o " + genome + "-fq2sam.%j.out\n")
	fqsam.write("#SBATCH -c " + params.cpu + "\n")
	fqsam.write("#SBATCH --array=1-" + str(count) + "\n")
	fqsam.write("#SBATCH --partition=" + params.partition + "\n")
	fqsam.write("#SBATCH -e " + genome + "-fq2sam.%j.error\n")
	fqsam.write("#SBATCH --mail-user=" + params.email + "\n")
	fqsam.write("#SBATCH --mail-type=begin\n")
	fqsam.write("#SBATCH --mail-type=end\n")
	fqsam.write("#SBATCH --requeue\n")
	fqsam.write("\n")

	# loads the module to be used
	fqsam.write("module load bwa/" + params.bwa + "\n")
	# fqsam.write("module load python/2.7.11\n")
	fqsam.write("\n")

	# get the first pair of a fastq file and assign for use
	fqsam.write("filename=`find " + params.input_dir + "/" + genome + " -name \"*1.fastq.gz\" | tail -n +${SLURM_ARRAY_TASK_ID} | head -1`\n")
	fqsam.write("\n")
	fqsam.write("python " + params.scripts_dir + "/fq2sam.py -r " + params.reference_dir + " -p $filename -o " + params.output_dir + " -t $SLURM_CPUS_PER_TASK\n")
	
	fqsam.close()
