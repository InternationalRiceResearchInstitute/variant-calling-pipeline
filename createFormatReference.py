#!/usr/bin/env python

import sys, re, os
import os.path
from classes import CreateFormatReferenceParams

fasta = ".fasta"
params = CreateFormatReferenceParams()
attributes = [attr for attr in dir(params) if not callable(getattr(params, attr)) and not attr.startswith("__")]

for line in open(params.fp):
	if re.findall(r'scripts_dir=', line):
		params.scripts_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'reference_dir=', line):
		params.reference_dir = line.split('=')[-1].rstrip()
		#params.dictionary_out = params.reference_dir
		#params.dictionary_out = params.dictionary_out.replace(params.regex, params.dictionary)

	elif re.findall(r'bwa=', line):
		params.bwa = line.split('=')[-1].rstrip()

	elif re.findall(r'email=', line):
		params.email = line.split('=')[-1].rstrip()

	elif re.findall(r'picard=', line):
		params.picard = line.split('=')[-1].rstrip()

	elif re.findall(r'samtool=', line):
		params.samtools = line.split('=')[-1].rstrip()

	elif re.findall(r'partition=', line):
		params.partition = line.split('=')[-1].rstrip()

if fasta in params.reference_dir:
	params.reference_dir = params.reference_dir.replace(fasta, params.regex)

params.dictionary_out = params.reference_dir
params.dictionary_out = params.dictionary_out.replace(params.regex, params.dictionary)

for line in open(params.fp):
	path = params.scripts_dir

	if not os.path.exists(path):
		os.mkdir(path, 0755)
	
	slurm = open(os.path.join(path, "format.sh"), "w")
	slurm.write("#!/bin/bash\n")
	slurm.write("\n")

	slurm.write("#SBATCH -J format_reference\n")
	slurm.write("#SBATCH -o format_reference.%j.out\n")
	slurm.write("#SBATCH --partition=" + params.partition + "\n")
	slurm.write("#SBATCH -e format_reference.%j.error\n")
	slurm.write("#SBATCH --mail-user=" + params.email + "\n")
	slurm.write("#SBATCH --mail-type=begin\n")
	slurm.write("#SBATCH --mail-type=end\n")
	slurm.write("#SBATCH --requeue\n")
	slurm.write("formatted=1\n")
	slurm.write("\n")

	slurm.write("module load samtools/" + params.samtools + "\n")
	slurm.write("module load bwa/" + params.bwa + "\n")
	slurm.write("module load jdk\n")
	slurm.write("\n")

	slurm.write("if [ -f " + params.reference_dir + ".amb -a -f " + params.reference_dir + ".ann -a -f " + params.reference_dir + ".bwt -a -f " + params.reference_dir + ".fai -a -f " + params.reference_dir + ".pac -a -f " + params.reference_dir + ".sa -a -f " + params.dictionary_out + " ]; then\n")
	slurm.write("formatted=0\n")
	slurm.write("fi\n")
	slurm.write("\n")

	slurm.write("if [ \"$formatted\" -eq 1 ]; then\n")
	slurm.write("bwa index -a is " + params.reference_dir + "\n\n")
	slurm.write("java -Xmx8g -jar " + params.picard + "/CreateSequenceDictionary.jar REFERENCE=" + params.reference_dir + " OUTPUT=" + params.dictionary_out + "\n\n")
	slurm.write("samtools faidx " + params.reference_dir + "\n")
	slurm.write("fi\n")
	slurm.close()
