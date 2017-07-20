#!/usr/bin/env python

import os, re
import os.path
import subprocess

fp = 'config'
input_dir = ''

for line in open(fp):
    if re.findall(r'input_dir', line):
        input_dir = line.split('=')[-1].rstrip()
        break

# checks if input.info exists
if os.path.isfile('input.info'):
    os.remove('input.info')

file = open("input.info", "w")

# system call for getting the inputs in input_dir
p = os.popen('ls ' + input_dir, "r")
while 1:
    line = p.readline().rstrip()
    if not line: break

    # counts fastq files in its folder
    p2 = os.popen('ls ' + input_dir + '/' + line + '/* | wc -l', "r")
    while  2:
        line2 = p2.readline().rstrip()
        if not line2: break

        # writes in a file
        file.write(line + ":" + line2 + "\n")

file.close()
