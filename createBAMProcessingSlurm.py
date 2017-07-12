#!/usr/bin/env python

import sys, re, os
import os.path
from classes import CreateBAMProcessingParams
from classes import writeFile

# get the genome file
input_file = sys.argv[1]
disk = sys.argv[2]

# get the parameters in the class CreateBAMProcessingParams
params = CreateBAMProcessingParams()
attributes = [attr for attr in dir(params) if not callable(getattr(params, attr)) and not attr.startswith("__")]

# reads the config file and get the respective values for each
for line in open(params.fp):
	if re.findall(r'tmp_dir=', line):
		params.tmp_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'input_dir=', line):
		params.input_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'output_dir=', line):
		params.output_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'scripts_dir=', line):
		params.scripts_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'analysis_dir=', line):
		params.analysis_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'software_dir=', line):
		params.software_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'reference_dir=', line):
		params.reference_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'jvm=', line):
		params.jvm = line.split('=')[-1].rstrip()

	elif re.findall(r'gatk=', line):
		params.gatk = line.split('=')[-1].rstrip()

	elif re.findall(r'email=', line):
		params.email = line.split('=')[-1].rstrip()

	elif re.findall(r'sleep=', line):
		params.sleep = line.split('=')[-1].rstrip()

	elif re.findall(r'picard=', line):
		params.picard = line.split('=')[-1].rstrip()

	elif re.findall(r'partition=', line):
		params.partition = line.split('=')[-1].rstrip()

	elif re.findall(r'cpu_sambam=', line):
		params.cpu_sambam = line.split('=')[-1].rstrip()

# reads the file containing the genome
for line in open(input_file):
	line = line.split(":")
	genome = line[0]

	# get its half for job array limit
	count = int(line[1]) / 2

	# create a directory for each genome
	os.makedirs(params.analysis_dir + "/" + disk + "/" + genome + "/logs")
	
	# directory where slurm script will store
	path = params.analysis_dir + "/" + disk
	slurm_file = "submit_sam2bam_slurm.sh"
	exec_file = os.path.join(path, slurm_file)

	output_path = params.analysis_dir + "/" + disk + "/" + genome
	sambam_file = genome + "-sam2bam.slurm"
	output_file = os.path.join(output_path, sambam_file)

	# creates a submit shell script between job submission
	# to prevent timeout
	script = open(exec_file, "w")
	script.write("#!/bin/bash\n")
	script.write("\n")
	script.write("sbatch " + output_file + "\n")
	script.write("sleep " + params.sleep + "\n")
	script.close()

	# creates slurm script
	sambam = open(output_file, "w")
	sambam.write("#!/bin/bash\n")
	sambam.write("\n")

	sambam.write("#SBATCH -J " + genome + "\n")
	sambam.write("#SBATCH -o " + genome + "-sam2bam.%j.out\n")
	sambam.write("#SBATCH -c " + params.cpu_sambam + "\n")
	sambam.write("#SBATCH --array=1-" + str(count) + "\n")
	sambam.write("#SBATCH --partition=" + params.partition + "\n")
	sambam.write("#SBATCH -e " + genome + "-sam2bam.%j.error\n")
	sambam.write("#SBATCH --mail-user=" + params.email + "\n")
	sambam.write("#SBATCH --mail-type=begin\n")
	sambam.write("#SBATCH --mail-type=end\n")
	sambam.write("#SBATCH --requeue\n")
	sambam.write("\n")

	# loads the module to be used
	sambam.write("module load jdk\n")
	# sambam.write("module load python" + params.python + "\n")
	sambam.write("\n")

	# get the first pair of a fastq file and assign for use
	sambam.write("filename=`find " + params.output_dir + "/" + genome + " -name \"*.sam\" | tail -n +${SLURM_ARRAY_TASK_ID} | head -1`\n")
	sambam.write("python " + params.scripts_dir + "/sam2bam.py -s $filename -r " + params.reference_dir + " -p " + params.picard + " -g " + params.gatk + " -j " + params.jvm + " -t " + params.tmp_dir + "\n")
	sambam.write("mv " + genome + "-fq2sam.*.error " + genome + "-fq2sam.*.out " + params.analysis_dir + "/" + disk + "/" + genome + "/logs")
	sambam.close()
