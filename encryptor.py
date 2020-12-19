#!/usr/bin/env python3
import subprocess
import sys

cmd = "python3 "
for i in range(1, len(sys.argv)):
    cmd += sys.argv[i] + ' '

p = subprocess.Popen(cmd, shell = True)
p.wait()
