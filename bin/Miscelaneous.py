#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

class Miscelaneous:
	def __init__(self):
		pass

	def progress_bar(self, value, max, barsize):
		chars = int(value * barsize / float(max))
		percent = int((value / float(max)) * 100)
		sys.stdout.write("#" * chars)
		sys.stdout.write(" " * (barsize - chars + 2))
		if value >= max:
			sys.stdout.write("Done. \n\n")
		else:
			sys.stdout.write("[%3i%%]\r" % (percent))
			sys.stdout.flush()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = "\033[1m"
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
