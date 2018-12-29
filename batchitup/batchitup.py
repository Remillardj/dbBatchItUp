#!/usr/local/bin/python3

from subprocess import call
import main

def mysql_dump(database, table, defaults=False, user=False, password=False):
	if (defaults):
		try:
			defaults_file = "--defaults-file=" + defaults
			result_file = "--result-file=./batchitup.sql"
			call(["mysqldump", defaults_file, "--databases", database, "--tables", table, "--extended-insert=FALSE", result_file])
		except Exception as e:
			print("Error!", e)
	else:
		try:
			call(["mysqldump", "--databases", database, "--tables", table, "--extended-insert=FALSE", "--user", user, "--password", password])
		except Exception as e:
			print("Error!", e)