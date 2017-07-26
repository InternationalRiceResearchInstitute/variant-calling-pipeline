#!/usr/bin/python

import sys, getopt, re, os
import zipfile, contextlib, subprocess

fixMisencoded = 0
fp = 'config'

# function for determining the fixMisencoded value
def checkIfExists(ref_genome):
    for line in open(fp):
        if re.findall('fixMisencoded-' + ref_genome + '=FALSE\n', line):
            return True
        elif re.findall('fixMisencoded-' + ref_genome + '=TRUE\n', line):
            return True

    return False

def main(argv):

    #get arguments
    try:
        opts, args = getopt.getopt(
            argv,
            "hi:o:g:",
            ["input=","out=", "gene="])
    except getopt.GetoptError:
        print 'fq2sam.py ' + \
                '-i <input_dir> ' + \
                '-o <output_dir> ' + \
                '-g <genome>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'fastqc.py ' + \
                    '-i <input_dir> ' + \
                    '-o <output_dir> ' + \
                    '-g <genome>'
            sys.exit()
        elif opt in ("-i", "--input"):
            input_dir = arg
        elif opt in ("-o", "--out"):
            output_dir = arg
        elif opt in ("-g", "--gene"):
            genome = arg

    p = os.popen('ls ' + input_dir + '/' + genome + '/', "r")
    while 1:
        line = p.readline().rstrip()
        if not line: break

        #command for alignment
        unzip = 'fastqc -o ' + \
                output_dir + '/' + \
                genome + ' ' + \
                input_dir + '/' + \
                genome

        #execute command
        os.system(unzip)

        line = line.replace('.fastq.gz', '_fastqc.zip')

        # FOR READING ZIP FILES

        # reading the zipfile
        with contextlib.closing(zipfile.ZipFile(output_dir + '/' + genome + '/' + line)) as z:
            # list all the files
            for filename in z.namelist():

                # check the fastqc_data.txt
                # determine the encoding used and set fixMisencoded if needed
                if re.findall(r'fastqc_data', filename):
                    with contextlib.closing(z.open(filename)) as f:
                        for encoding in f:
                            if re.findall(r'(Sanger | Illumina 1+\.+8+\+)', encoding):
                                fixMisencoded = 1
                                break
                elif re.findall(r'summary', filename):
                    with contextlib.closing(z.open(filename)) as f:
                        for data in f:
                            with open("statistics.txt", "a") as fp:
                                fp.write(data)


        # FOR FIXMISENCODED

        ref_genome = re.split('1.fastq|2.fastq', line)[0]

        # read a list of lines into data
        with open(fp, 'r') as file:
            data = file.readlines()

            # change the line and take note of the new line
            for i, line in enumerate(data):
                if line.startswith("[MISENCODED EQUALS]"):
                    if not checkIfExists(ref_genome):
                        if fixMisencoded == 0: data[i] = data[i] + 'fixMisencoded-' + ref_genome + '=TRUE\n'
                        else: data[i] = data[i] + 'fixMisencoded-' + ref_genome + '=FALSE\n'
                        break

        # and write everything back
        with open(fp, 'w') as file:
            file.writelines(data)

if __name__ == "__main__":
    main(sys.argv[1:])
