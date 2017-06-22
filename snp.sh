#!/bin/bash

filename="sample.input.info"
disk="10"

#create slurm scripts for each step
python createAlignmentSlurm.py $filename $disk
python createBAMProcessingSlurm.py $filename $disk
python createMergeBAMSlurm.py $filename $disk
python createVariantCallingSlurm.py $filename $disk
