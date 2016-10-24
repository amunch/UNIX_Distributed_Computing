#!/usr/bin/env python2.7
#project 02
#hulk.py
#amunch,mpruitt1,amukasya

import sys
import os
import work_queue
import itertools
import string
import json

HASHES = "hashes.txt"
PORT = 9199
TASKS = 100
ALPHABET=string.ascii_lowercase+string.digits

if __name__ == '__main__':
	JOURNAL = json.load(open('journal.json'))
	
	queue = work_queue.WorkQueue(PORT, name='hulk-amunch', catalog=True)
	queue.specify_log('fury.log')

	for num in range(1,6):
		command = './hulk.py -l {}'.format(num)
		if command in JOURNAL:
			print >>sys.stderr, 'Already did', command
		else:
			task = work_queue.Task(command)
			for source in ('hulk.py', HASHES):
				task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)
	
			queue.submit(task)
	for num in range(1,4):
		for prefix in itertools.product(ALPHABET,repeat = int(num)):
			prefix = ''.join(prefix)
			command = './hulk.py -l 5 -p {}'.format(prefix)
			if command in JOURNAL:
				print >>sys.stderr, 'Already did', command
			else:
				task = work_queue.Task(command)
		       	        for source in ('hulk.py', HASHES):
		       	                task.specify_file(source, source, work_queue.WORK_QUEUE_INPUT)

		                queue.submit(task)

	while not queue.empty():
		task = queue.wait()

		if task and task.return_status == 0:
			JOURNAL[task.command] = task.output.split()
			with open('journal.json.new', 'w') as stream:
				json.dump(JOURNAL, stream)
			os.rename('journal.json.new', 'journal.json')
