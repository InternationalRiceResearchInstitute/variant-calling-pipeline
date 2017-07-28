#!/usr/bin/env python

import sys, re, os, os.path
from classes import CreateControlQualityParams

# get the genome file
input_file = sys.argv[1]
disk = sys.argv[2]

# get the parameters in the class CreateControlQualitySlurm
params = CreateControlQualityParams()

# reads the config file and get the respective values for each
for line in open(params.fp):
	if re.findall(r'email=', line): params.email = line.split('=')[-1].rstrip()
	elif re.findall(r'sleep=', line): params.sleep = line.split('=')[-1].rstrip()
	elif re.findall(r'fastqc=', line): params.fastqc = line.split('=')[-1].rstrip()
	elif re.findall(r'partition=', line): params.partition = line.split('=')[-1].rstrip()
	elif re.findall(r'cpu_fastq=', line): params.cpu_fastq = line.split('=')[-1].rstrip()
	elif re.findall(r'input_dir=', line): params.input_dir = line.split('=')[-1].rstrip()
	elif re.findall(r'output_dir=', line): params.output_dir = line.split('=')[-1].rstrip()
	elif re.findall(r'scripts_dir=', line): params.scripts_dir = line.split('=')[-1].rstrip()
	elif re.findall(r'analysis_dir=', line): params.analysis_dir = line.split('=')[-1].rstrip()

# reads the file containing the genome
for line in open(input_file):
	line = line.split(":")
	genome = line[0]
	count = '1'

	# create a directory for each genome
	os.makedirs(params.analysis_dir + "/" + disk + "/" + genome)
	os.makedirs(params.output_dir + "/" + genome)
	os.makedirs(params.analysis_dir + "/" + disk + "/" + genome + "/logs")
	
	# directory where slurm script will store
	path = params.analysis_dir + "/" + disk + "/"
	slurm_file = "submit_fastqc_slurm.sh"
	exec_file = os.path.join(path, slurm_file)

	output_path = params.analysis_dir + "/" + disk + "/" + genome + "/"
	fastqc_file = genome + "-fastqc.slurm"
	output_file = os.path.join(output_path, fastqc_file)

	# creates a submit shell script between job submission
	# to prevent timeout
	script = open(exec_file, "w")
	script.write("#!/bin/bash\n")
	script.write("\n")
	script.write("sbatch " + output_file + "\n")
	script.write("sleep " + params.sleep + "\n")
	script.close()

	# creates slurm script
	fastqc = open(output_file, "w")
	fastqc.write("#!/bin/bash\n")
	fastqc.write("\n")

	fastqc.write("#SBATCH -J " + genome + "-fastqc\n")
	fastqc.write("#SBATCH -o " + genome + "-fastqc.%j.out\n")
	fastqc.write("#SBATCH -c " + params.cpu_fastq + "\n")
	fastqc.write("#SBATCH --array=1-" + str(count) + "\n")
	fastqc.write("#SBATCH --partition=" + params.partition + "\n")
	fastqc.write("#SBATCH -e " + genome + "-fastqc.%j.error\n")
	fastqc.write("#SBATCH --mail-user=" + params.email + "\n")
	fastqc.write("#SBATCH --mail-type=begin\n")
	fastqc.write("#SBATCH --mail-type=end\n")
	fastqc.write("#SBATCH --requeue\n")
	fastqc.write("\n")

	# loads the module to be used
	fastqc.write("module load fastqc/" + params.fastqc + "\n")
	# fastqc.write("module load python/" + params.python + "\n")
	fastqc.write("\n")

	# get the first pair of a fastq file and assign for use
	fastqc.write("python " + params.scripts_dir + "/fastqc.py -i " + params.input_dir + " -o " + params.output_dir + " -g " + genome)

	fastqc.close()
