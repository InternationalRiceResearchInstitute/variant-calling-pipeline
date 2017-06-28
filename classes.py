#!/usr/bin/env python

# classes for each steps
class CreateFormatReferenceParams():
	reference_dir = ''
	scripts_dir = ''
	picard = ''
	email = ''
	partition = ''
	dictionary_out = ''
	regex = '.fa'
	dictionary = '.dict'
	fp = 'config'

class CreateAlignmentParams():
	analysis_dir = ''
	input_dir = ''
	reference_dir = ''
	scripts_dir = ''
	output_dir = ''
	email = ''
	partition = ''
	bwa = ''
	cpu = ''
	fp = 'config'

class CreateBAMProcessingParams():
	analysis_dir = ''
	input_dir = ''
	reference_dir = ''
	scripts_dir = ''
	output_dir = ''
	software_dir = ''
	tmp_dir = ''
	picard = ''
	gatk = ''
	email = ''
	cpu = ''
	partition = ''
	jvm = '8g'
	fp = 'config'

class CreateMergeBAMParams():
	analysis_dir = ''
	input_dir = ''
	reference_dir = ''
	scripts_dir = ''
	output_dir = ''
	email = ''
	cpu = ''
	samtools = ''
	partition = ''
	fp = 'config'

class CreateVariantCallingParams():
	analysis_dir = ''
	input_dir = ''
	reference_dir = ''
	scripts_dir = ''
	output_dir = ''
	software_dir = ''
	tmp_dir = ''
	gatk = ''
	bgzip = ''
	tabix = ''
	email = ''
	cpu = ''
	samtools = ''
	htslib = ''
	partition = ''
	fp = 'config'

def writeFile(script, output):
	script.write("#!/bin/bash\n")
	script.write("\n")
	script.write("sbatch " + output + "\n")
	script.write("sleep 10m\n")
