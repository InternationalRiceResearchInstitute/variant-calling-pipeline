#!/usr/bin/python

import sys, getopt, subprocess, os, re
from subprocess import Popen, PIPE
from subprocess import call

def main(argv):

    #get arguments
    try:
        opts, args = getopt.getopt(
            argv,
            "hv:o:",
            ["vcf=", "outputdir="])
    except getopt.GetoptError:
        print 'vcfvalidator.py ' + \
                '-v <VCF file> ' + \
                '-o <output dir>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'vcfvalidator.py ' + \
                    '-v <VCF file> ' + \
                    '-o <output dir>'
            sys.exit()
        elif opt in ("-v", "--vcffile"):
            vcf = arg
        elif opt in ("-o", "--outputdir"):
            output_dir = arg

    vcf = vcf.rstrip('\n')

    # checks vcf file is in the ouput folder
    p = os.popen('ls ' + vcf, "r")
    while 1:
        genome = p.readline().rstrip()
        if not genome: break

        if re.findall(r'(vcf+\.+gz)', genome):
            vcf = vcf + genome
            break

    # splits the path into three
    split_dir = re.search(r'(.*)/(.*)/(.*vcf+\.+gz)', vcf, re.M)
    if split_dir:
        input_dir = split_dir.group(1)
        genome = split_dir.group(2)
        vcf_file = split_dir.group(3)
    else:
        print "Nothing found!"

    # write vcf statistics in the file
    vcf_out = vcffile.replace('vcf.gz', 'txt')
    #command for alignment
    valid = 'vcf --stats ' + \
            output_dir + '/' + \
            genome + '/' + \
            vcf_file + '> ' + \
            output_dir + '/' + \
            genome + '/' + \
            genome + '.vcf.stats'

    #execute command
    os.system(valid)
    print "Input:" + vcf

if __name__ == "__main__":
    main(sys.argv[1:])
