#!/usr/bin/env python

import sys, getopt, os
import os.path

def main(argv):

    input_file = 'input.info'

    #get arguments
    try:
        opts, args = getopt.getopt(
            argv,
            "ho:g:",
            ["input=","out=", "gene="])
    except getopt.GetoptError:
        print 'mergebam.py ' + \
                '-o <output_dir> ' + \
                '-g <raw_dir>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mergebam.py ' + \
                    '-o <output_dir> ' + \
                    '-g <raw_dir>'
            sys.exit()
        elif opt in ("-o", "--out"):
            output_dir = arg
        elif opt in ("-g", "--gene"):
            raw_dir = arg

    for line in open(input_file):
        line = line.split(":")
        genome = line[0]
        count = line[1]

        if raw_dir == genome:
            if int(count) > 2:
                mergebam = raw_dir + ".merged.bam"
                if not os.path.exists(output_dir + '/' + raw_dir + '/' + mergebam):
                    merge = 'samtools merge ' + \
                            output_dir + '/' + \
                            raw_dir + '/' + \
                            mergebam + ' ' + \
                            output_dir + '/' + \
                            raw_dir + '/' + \
                            '*.realign.bam'

                    os.system(merge)

                if not os.path.exists(output_dir + '/' + raw_dir + '/' + mergebam + '.bai'):
                    index = 'samtools index ' + \
                            output_dir + '/' + \
                            raw_dir + '/' + \
                            mergebam

                    os.system(index)

                lists = 'rm ' + \
                        output_dir + '/' + \
                        raw_dir + '/' + \
                        '*.list'

                realignbam = 'rm ' + \
                        output_dir + '/' + \
                        raw_dir + '/' + \
                        '*.realign.bam'

                realignbai = 'rm ' + \
                        output_dir + '/' + \
                        raw_dir + '/' + \
                        '*.realign.bai'

                os.system(lists)
                os.system(realignbam)
                os.system(realignbai)

if __name__ == "__main__":
    main(sys.argv[1:])
