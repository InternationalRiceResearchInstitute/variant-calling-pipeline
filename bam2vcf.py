#!/usr/bin/python

import sys, re, getopt, os, subprocess, os.path

def main(argv):
    exist = 0

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

    # get the path of merged.txt and/or realign.txt file
    p = os.popen('ls ' + bam, "r")
    while 1:
        genome = p.readline().rstrip()
        if not genome: break

        if re.findall(r'(merged+\.+txt)', genome):
            bam_txt = bam + genome
            break
        elif re.findall(r'(realign+\.+txt)', genome):
            bam_txt = bam + genome
            break

    # get the path of merged.bam and/or realign.bam file
    # and make a vcf file
    p = os.popen('ls ' + bam, "r")
    while 1:
        genome = p.readline().rstrip()
        if not genome: break

        if re.findall(r'(merged+\.+bam)', genome):
            bam = bam + genome
            vcf = bam.replace('merged.bam', 'vcf')
            break
        elif re.findall(r'(realign+\.+bam)', genome):
            bam = bam + genome
            vcf = bam.replace('realign.bam', 'vcf')
            break

    with open(bam_txt) as fp:
        for line in fp:
            if re.findall(r'SUCCESS', line):
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
                exist = 1
                break
            else:
                exist = 0

    if exist == 0:
        with open("bam_log.txt", "w") as f:
            f.write("Bam of is invalid")

if __name__ == "__main__":
    main(sys.argv[1:])
