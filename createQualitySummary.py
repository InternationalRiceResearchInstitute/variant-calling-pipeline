#!/usr/bin/env python

import os, re, sys
import zipfile
import os.path
from classes import CreateQualityParams

# get the genome file
input_file = sys.argv[1]
fixMisencoded = 0;

# get the parameters in the class CreateQualityParams
params = CreateQualityParams()
attributes = [attr for attr in dir(params) if not callable(getattr(params, attr)) and not attr.startswith("__")]

# reads the config file and get the respective values for each
for line in open(params.fp):
	if re.findall(r'input_dir', line):
		params.input_dir = line.split('=')[-1].rstrip()
	elif re.findall(r'output_dir', line):
		params.output_dir = line.split('=')[-1].rstrip()
	elif re.findall(r'qcheck_dir', line):
		params.qcheck_dir = line.split('=')[-1].rstrip()

# create a directory for the output of quality check/control
# os.makedirs(params.output_dir + "/output_qcheck/")
params.output_dir = os.path.join(params.output_dir, "output_qcheck")

# reads the file containing the genome
for pair in open(input_file):
	pair = pair.split(':')
	genome = pair[0]

	# get the fastq.gz files inside their directories
	p = os.popen('ls ' + params.input_dir + '/' + genome + '/', "r")
	while 1:
		line = p.readline().rstrip()
		if not line: break

		# path for the fastqc and fastq.gz files
		# run the fastqc and store the outputs
		fastqc = os.path.join(params.qcheck_dir, "fastqc")
		fq_file = os.path.join(params.input_dir, genome)

		os.system("chmod 755 " + params.qcheck_dir + "/./fastqc")
		os.system(fastqc + " -o " + params.output_dir  + " " + fq_file + "/" + line)

		line = line.replace('.fastq.gz', '_fastqc.zip')

		# FOR READING ZIP FILES

		# reading the zipfile
		with zipfile.ZipFile(params.output_dir + '/' + line) as z:
			# list all the files
			for filename in z.namelist():
				
				# check the fastqc_data.txt
				# determine the encoding used and set fixMisencoded if needed
				if re.findall(r'fastqc_data', filename):
					with z.open(filename) as f:
						for encoding in f:
							if re.findall(r'(Sanger | Illumina 1+\.+8+\+)', encoding):
								fixMisencoded = 1
								break
				# elif re.findall(r'summary', filename):
				# 	with z.open(filename) as f:
				# 		for stats in f:
				# 			print stats
				# 			continue

		# FOR FIXMISENCODED

		# read a list of lines into data
		with open(params.fp, 'r') as file:
			data = file.readlines()

			# change the line and take note of the new line
			for i, line in enumerate(data):
				if line.startswith("[MISENCODED EQUALS]"):
					if fixMisencoded == 1:
						data[i+1] = data[i+1] + 'fixMisencoded=TRUE\n\n'
					else:
						data[i+1] = data[i+1] + 'fixMisencoded=FALSE\n\n'
					break

		# and write everything back
		with open(params.fp, 'w') as file:
			file.writelines(data)
