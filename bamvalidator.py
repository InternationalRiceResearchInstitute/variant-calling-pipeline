#!/usr/bin/python

import sys, getopt, subprocess, os, re
from subprocess import Popen, PIPE
from subprocess import call

def main(argv):

    #get arguments
    try:
        opts, args = getopt.getopt(
            argv,
            "hb:o:",
            ["bam=", "outputdir="])
    except getopt.GetoptError:
        print 'bamvalidator.py ' + \
                '-b <BAM file> ' + \
                '-o <output dir>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'bamvalidator.py ' + \
                    '-b <BAM file> ' + \
                    '-o <output dir>'
            sys.exit()
        elif opt in ("-b", "--bamfile"):
            bam = arg
        elif opt in ("-o", "--outputdir"):
            output_dir = arg

    bam = bam.rstrip('\n')

    # checks what kind of bam file is in the ouput folder
    # merged or realign bam
    p = os.popen('ls ' + bam, "r")
    while 1:
        genome = p.readline().rstrip()
        if not genome: break

        if re.findall(r'(merged+\.+bam)', genome):
            bam = bam + genome
            break
        elif re.findall(r'(realign+\.+bam)', genome):
            bam = bam +  genome
            break

    # splits the path into three
    split_dir = re.search(r'(.*)/(.*)/(.*bam)', bam, re.M)
    if split_dir:
        input_dir = split_dir.group(1)
        genome = split_dir.group(2)
        bamfile = split_dir.group(3)
    else:
        print "Nothing found!"

    # write bam statistics in the file
    bam_out = bamfile.replace('bam', 'txt')
    with open(output_dir + '/' + bam_out, 'w') as out:
        subprocess.call(['bam', 'validate', '--in', bam, '--verbose'], stdout=out, stderr=subprocess.STDOUT)
    print "Input:" + bam

if __name__ == "__main__":
    main(sys.argv[1:])
