#!/usr/bin/env python

import sys, re, os
import os.path
from classes import CreateVariantCallingParams
from classes import writeFile

# get the genome file
file = sys.argv[1]
disk = sys.argv[2]

# get the parameters in the class CreateVariantCallingParams
params = CreateVariantCallingParams()
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

	elif re.findall(r'software_dir', line):
		params.software_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'tmp_dir', line):
		params.tmp_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'gatk', line):
		params.gatk = line.split('=')[-1].rstrip()

	elif re.findall(r'bgzip', line):
		params.bgzip = line.split('=')[-1].rstrip()

	elif re.findall(r'tabix', line):
		params.tabix = line.split('=')[-1].rstrip()

	elif re.findall(r'email', line):
		params.email = line.split('=')[-1].rstrip()

	elif re.findall(r'cpu', line):
		params.cpu = line.split('=')[-1].rstrip()

	elif re.findall(r'samtools', line):
		params.samtools = line.split('=')[-1].rstrip()

	elif re.findall(r'htslib', line):
		params.htslib = line.split('=')[-1].rstrip()

	elif re.findall(r'partition', line):
		params.partition = line.split('=')[-1].rstrip()

# reads the file containing the genome
for line in open(file):
	line = line.split(":")
	genome = line[0]

	# directory where slurm script will store
	path = params.analysis_dir + "/" + disk
	slurm_file = "submit_bam2vcf_slurm.sh"

	output_path = params.analysis_dir + "/" + disk + "/" + genome
	bamvcf_File = genome + "-bam2vcf.sh"

	# creates a submit shell script between job submission
	# to prevent timeout
	script = open(os.path.join(path, slurm_file), "w")
	writeFile(script, os.path.join(output_path, bamvcf_file))
	script.close()

	# creates slurm script
	bamvcf = open(os.path.join(path, bamvcfFile), "w")
	bamvcf.write("#!/bin/bash\n")
	bamvcf.write("\n")

	bamvcf.write("#SBATCH -J " + genome + "-bam2vcf\n")
	bamvcf.write("#SBATCH -o " + genome + "-bam2vcf.%j.out\n")
	bamvcf.write("#SBATCH -c " + params.cpu + "\n")
	bamvcf.write("#SBATCH --partition=" + params.partition + "\n")
	bamvcf.write("#SBATCH -e " + genome + "-bam2vcf.%j.error\n")
	bamvcf.write("#SBATCH --mail-user=" + params.email + "\n")
	bamvcf.write("#SBATCH --mail-type=ALL\n")
	bamvcf.write("#SBATCH --requeue\n")
	bamvcf.write("\n")

	# loads the modules
	bamvcf.write("module load jdk\n")
	bamvcf.write("module load samtools/" + params.samtools + "\n")
	bamvcf.write("module load htslib/" + params.htslib + "\n")
	# bamvcf.write("module load python/2.7.11\n")
	bamvcf.write("\n")

	# get the first pair of a fastq file and assign for use
	bamvcf.write("python " + params.scripts_dir + "/bam2vcf.py -b " + params.output_dir + "/" +  genome + "/" +  genome + ".merged.bam -r " + params.reference_dir + "r -g " + params.gatk + " -t " + params.tmp_dir + " -z " + params.bgzip + " -x " + params.tabix + "\n")
	bamvcf.write("mv " + genome + "-mergebam.*.error " + genome + "-mergebam.*.out " + genome + "-bam2vcf.*.error " + genome + "-bam2vcf.*.out " + params.analysis_dir + "/" + disk + "/" + genome + "/logs")
	bamvcf.close()
