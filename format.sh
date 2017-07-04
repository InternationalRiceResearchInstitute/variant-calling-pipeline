#!/bin/bash

#SBATCH -J format_reference
#SBATCH -o format_reference.%j.out
#SBATCH --partition=batch
#SBATCH -e format_reference.%j.error
#SBATCH --mail-user=jppascual2@up.edu.ph
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --requeue
formatted=1

module load samtools/1.0
module load bwa/0.7.10
module load jdk

if [ -f /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa.amb -a -f /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa.ann -a -f /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa.bwt -a -f /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa.fai -a -f /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa.pac -a -f /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa.sa -a -f /home/jppascual/ref_genome/IRGSP-1.0_chr01.dict ]; then
formatted=0
fi

if [ "$formatted" -eq 1 ]; then
bwa index -a is /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa

java -Xmx8g -jar /home/jppascual/software/picard-tools-1.119/CreateSequenceDictionary.jar REFERENCE=/home/jppascual/ref_genome/IRGSP-1.0_chr01.fa OUTPUT=/home/jppascual/ref_genome/IRGSP-1.0_chr01.dict

samtools faidx /home/jppascual/ref_genome/IRGSP-1.0_chr01.fa
fi
