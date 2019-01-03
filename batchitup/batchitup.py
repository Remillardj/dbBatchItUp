#!/usr/local/bin/python3

from subprocess import call
import re

import main

'''
  get a dump of the data in mysql utilizing either a defaults file or a user/password combination
'''
def mysql_dump(database, table, defaults=False, user=False, password=False):
	resultFile = "--result-file=./batchitup.sql"
	if (defaults):
		try:
			defaultsFile = "--defaults-file=" + defaults
			call(["mysqldump", defaultsFile, "--databases", database, "--tables", table, "--extended-insert=FALSE", resultFile])
		except Exception as e:
			print("Error!", e)
	else:
		try:
			dumpPass = "-p" + password
			call(["mysqldump", "--user", user, dumpPass, "--databases", database, "--tables", table, "--extended-insert=FALSE", resultFile])
		except Exception as e:
			print("Error!", e)

'''
  since mysqldump comes with header crap, we need to filter that out by a keyword
  of either INSERT INTO or DELETE
'''
def grep_file(fileName, pattern):
	try:
		file = open("inserts.sql", "w")
		with open(fileName, "r") as origin:
			for line in origin:
				if (pattern in line):
					file.write(line)
		file.close()
	except Exception as e:
		print("Error!", e)

'''
  Since the goal of this program is to do batch inserts/deletes, this function chops it up by chunk size
'''
def chunky_monkey(fileName, chunk_size):
	numLines = sum(1 for line in open(fileName))
	totalLoops = numLines/chunk_size
	x = 0
	incrFiles = str(totalLoops) + ".sql"
	for i in range(totalLoops):
		with open(fileName, "r") as origin:
			file = open(incrFiles, "w")
			for line in origin:
				if (x == chunk_size):
					file.close()
					break
				file.write(line)
				x += 1















