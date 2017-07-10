#!/usr/bin/python

import sys, re, getopt, os, subprocess

def main(argv):

    #get arguments
    try:
        opts, args = getopt.getopt(
            argv,
            "hb:r:g:t:z:x:",
            ["bam=", "ref=", "gatk=", "temp=", "bgzip", "tabix"])
    except getopt.GetoptError:
        print 'bam2vcf.py ' + \
                '-b <BAM file> ' + \
                '-r <reference> ' + \
                '-g <gatk> ' + \
                '-t <temp_dir> ' + \
                '-z <bgzip> ' + \
                '-x <tabix>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'bam2vcf.py ' + \
                    '-b <BAM file> ' + \
                    '-r <reference> ' + \
                    '-g <gatk> ' + \
                    '-t <temp_dir> ' + \
                    '-z <bgzip> ' + \
                    '-x <tabix>'
            sys.exit()
        elif opt in ("-b", "--bamfile"):
            bam = arg
        elif opt in ("-r", "--reference"):
            reference = arg
        elif opt in ("-g", "--gatk"):
            gatk = arg
        elif opt in ("-t", "--temp_dir"):
            temp_dir = arg
        elif opt in ("-z", "--bgzip"):
            bgzip = arg
        elif opt in ("-x", "--tabix"):
            tabix = arg

    p = os.popen('ls ' + bam, "r")
    while 1:
        genome = p.readline().rstrip()
        if not genome: break

        if re.findall(r'(merged+\.+bam)', genome):
	    print "merged.bam:    " + genome
            bam = bam + "/" + genome
            print "this is bam:   " + bam
            vcf = bam.replace('merged.bam', 'vcf')
            break
        elif re.findall(r'(realign+\.+bam)', genome):
            print "realign.bam:   " + genome
            bam = bam + "/" + genome
            print "this is bam r: " + bam
            vcf = bam.replace('realign.bam', 'vcf')
            break

    subprocess.call(['java', '-Xmx8g',
            '-Djava.io.tmpdir=' + temp_dir,
            '-jar', gatk,
            '-T', 'UnifiedGenotyper',
            '-R', reference,
            '-I', bam,
            '-o', vcf,
            '-glm', 'BOTH',
            '-mbq', '20',
            '-gt_mode', 'DISCOVERY',
            '-out_mode', 'EMIT_ALL_SITES',
            '-nt', '8'])

    vcfgz = vcf.replace('vcf', 'vcf.gz')
    subprocess.call([bgzip, vcf])
    subprocess.call([tabix, vcfgz])

if __name__ == "__main__":
    main(sys.argv[1:])