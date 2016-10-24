#!/usr/bin/env python2.7
#project 02
#hulk.py
#amunch,mpruitt1,amukasya

import hashlib
import string
import sys
import itertools
import random
import getopt
import os
#Constants
ALPHABET=string.ascii_lowercase+string.digits
LENGTH=int(8)
HASHES="hashes.txt"
PREFIX=""
PROGRAM_NAME= os.path.basename(sys.argv[0])

#utility function
def md5sum(s):
	return hashlib.md5(s).hexdigest()

def error(message, *args):
	print >>sys.stderr,message.format(*args)
	sys.exit(1)
def usage(exit_code=0):
	error('''Usage: {} options...

	Options:
		-a ALPHABET Alphabet used for passwords
		-l LENGTH   Length for passwords
		-s HASHES   Path to file containing hashes
		-p PREFIX   PRefix to use for each candiate password'''.format(PROGRAM_NAME),exit_code)
#parsing command line
try:
	opts,args=getopt.getopt(sys.argv[1:],"a:l:s:p:")
except getopt.GetoptError as e:
	print e
	usage(1)
for o,a in opts:
	if o =="-a":
		ALPHABET=a
	elif o == "-l":
		LENGTH=a
	elif o == "-s":
		HASHES=a
	elif o == "-p":
		PREFIX=a
	else:
		usage(1)

#main
if __name__ == '__main__':
	hashes=set([l.strip() for l in open(HASHES)])

	for candidate in itertools.product(ALPHABET,repeat=int(LENGTH)):
		candidate=''.join(candidate)
		candidate = PREFIX + candidate
		checksum=md5sum(candidate)
		if checksum in hashes:
			if PREFIX is not "":
				if str(candidate[:len(PREFIX)]) == str(PREFIX):
					print candidate
			else:
				print candidate
