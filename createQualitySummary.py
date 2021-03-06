#!/usr/bin/env python

import os, re, sys, os.path, zipfile, contextlib
from classes import CreateQualityParams

# get the genome file
input_file = 'input.info'
fixMisencoded = 0;

# get the parameters in the class CreateQualityParams
params = CreateQualityParams()

# function to check if the fixMisencoded for the genome exists
def checkIfExists(reference_genome):
	for line in open(params.fp):
		if re.findall('fixMisencoded-' + reference_genome + '=FALSE\n', line): return True
		elif re.findall('fixMisencoded-' + reference_genome + '=TRUE\n', line): return True

	return False

# main program
# reads the config file and get the respective values for each
for line in open(params.fp):
	if re.findall(r'input_dir=', line): params.input_dir = line.split('=')[-1].rstrip()
	elif re.findall(r'output_dir=', line): params.output_dir = line.split('=')[-1].rstrip()
	elif re.findall(r'qcheck_dir=', line): params.qcheck_dir = line.split('=')[-1].rstrip()

# create a directory for the output of quality check/control
if not os.path.exists(params.output_dir + "/output_check/"):
	os.makedirs(params.output_dir + "/output_check/")

params.output_dir = os.path.join(params.output_dir, "output_check")

# reads the file containing the genome
for pair in open(input_file):
	pair = pair.split(':')
	genome = pair[0]

	# get the fastq.gz files inside their directories
	p = os.popen('ls ' + params.input_dir + '/' + genome + '/', "r")
	while 1:
		line = p.readline().rstrip()
		if not line: break

		if not re.findall(r'fastq+\.+gz$', line): continue

		# path for the fastqc and fastq.gz files
		# run the fastqc and store the outputs
		fastqc = os.path.join(params.qcheck_dir, "fastqc")
		fq_file = os.path.join(params.input_dir, genome)

		os.system("chmod 755 " + params.qcheck_dir + "/./fastqc")
		os.system(fastqc + " -o " + params.output_dir  + " " + fq_file + "/" + line)

		line = line.replace('.fastq.gz', '_fastqc.zip')

		# FOR READING ZIP FILES

		# reading the zipfile
		with contextlib.closing(zipfile.ZipFile(params.output_dir + '/' + line)) as z:
			# list all the files
			for filename in z.namelist():

				# check the fastqc_data.txt
				# determine the encoding used and set fixMisencoded if needed
				if re.findall(r'fastqc_data', filename):
					with contextlib.closing(z.open(filename)) as f:
						for encoding in f:
							if re.findall(r'(Sanger | Illumina 1+\.+8+\+)', encoding):
								fixMisencoded = 1
								break
				elif re.findall(r'summary', filename):
					with contextlib.closing(z.open(filename)) as f:
						for data in f:
							with open("statistics.txt", "a") as fp:
								fp.write(data)


		# FOR FIXMISENCODED

		ref_genome = re.split('_1.fastq|_2.fastq', line)[0]

		# read a list of lines into data
		with open(params.fp, 'r') as file:
			data = file.readlines()

			# change the line and take note of the new line
			for i, line in enumerate(data):
				if line.startswith("[MISENCODED EQUALS]"):
					if not checkIfExists(ref_genome):
						if fixMisencoded == 0: data[i] = data[i] + 'fixMisencoded-' + ref_genome + '=TRUE\n'
						else: data[i] = data[i] + 'fixMisencoded-' + ref_genome + '=FALSE\n'
						break

		# and write everything back
		with open(params.fp, 'w') as file:
			file.writelines(data)
