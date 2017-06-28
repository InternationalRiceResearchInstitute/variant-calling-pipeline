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
	partition = ''
	fp = 'config'

def writeFile(script, output):
	script.write("#!/bin/bash\n")
	script.write("\n")
	script.write("sbatch " + output + "\n")
	script.write("sleep 10m\n")
