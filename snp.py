#!/usr/bin/env python

import sys, re, os
import os.path

fp = 'config'
sudo_dir = ''
analysis_dir =''
scripts_dir = ''
disk = ''
file_input = 'input.info'
inc_pairs = False

# reads the config file and get the respective values for each
for line in open(fp):
	if re.findall(r'analysis_dir=', line):
		analysis_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'scripts_dir=', line):
		scripts_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'sudo_dir=', line):
		sudo_dir = line.split('=')[-1].rstrip()

	elif re.findall(r'disk=', line):
		disk = line.split('=')[-1].rstrip()

# os.makedirs(params.analysis_dir + "/" + params.disk)

# system call for getting the inputs in input_dir
for pair in open(file_input):
	pair = pair.split(":")
	genome = pair[0]

	p = os.popen('ls ' + sudo_dir + '/' + genome + '/', "r")
	while 1:
		line = p.readline().rstrip()
		if not line: break

		if re.findall(r'' + genome, line):
			if re.findall(r'(?:1.fastq.gz|1.fq.gz)', line):
				while 1:
					line2 = p.readline().rstrip()
					if not line2: break
					print line2

					if re.findall(r'' + genome, line):
						if re.findall(r'(?:2.fastq.gz|2.fq.gz)', line2):
							print "this " + line + " and " + line2
							break
						elif not re.findall(r'(?:1.fastq.gz|1.fq.gz)', line2):
							print "oh no"
							break

# os.system('perl ' + createFormatReference.pl)
formats = 'sbatch ' + os.path.join(scripts_dir, 'formats.sh')

createAlignment = os.path.join(scripts_dir, 'createAlignmentSlurm.py')
createBAMProcessing = os.path.join(scripts_dir, 'createBAMProcessingSlurm.py')
createMergeBAM = os.path.join(scripts_dir, 'createMergeBAMSlurm.py')
createVariantCalling = os.path.join(scripts_dir, 'createVariantCallingSlurm.py')

os.system('python ' + createAlignment + ' ' + file_input + ' ' + disk)
os.system('python ' + createBAMProcessing + ' ' + file_input + ' ' + disk)
os.system('python ' + createMergeBAM + ' ' + file_input + ' ' + disk)
os.system('python ' + createVariantCalling + ' ' + file_input + ' ' + disk)

for pair in open(file_input):
	pair = pair.split(":")
	genome = pair[0]

	job = 'ls ' + analysis_dir + '/' + disk + '/' + genome + '/*fq2sam.* '
	dep = 'sbatch --dependency=afterok:' + formats + ' ' + job
	samtobam = job + '/fq2sam./sam2bam.'

	#submit its corresponding sam2bam to the job scheduler w/ fq2sam as its dependency
	os.system('sbatch --dependency=afterok:' + dep + ' ' + samtobam)
	os.system('sleep 3m')

	mergebam = job + '/fq2sam./mergebam.'

	#submit *mergebam. to the job scheduler, set all sam2bam of the same genome as its dependency
	dep = 'sbatch --dependency=singleton' + mergebam

	bamtovcf = job + '/fq2sam./bam2vcf.'

	#submit its corresponding bam2vcf to the job scheduler w/ mergebam as its dependency
	os.system('sbatch --dependency=afterok:' + dep + ' ' + bamtovcf)
	os.system('sleep 3m')
