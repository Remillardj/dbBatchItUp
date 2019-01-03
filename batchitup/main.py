#!/usr/local/bin/python3

import logging
import argparse
import os
import pwd
import batchitup

VERSION = "0.1.0"

def welcome_banner():
	print(""" \
 __    __     _                            _            ___       _       _      _____ _               
/ / /\ \ \___| | ___ ___  _ __ ___   ___  | |_ ___     / __\ __ _| |_ ___| |__   \_   \ |_ /\ /\ _ __  
\ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \   /__\/// _` | __/ __| '_ \   / /\/ __/ / \ \ '_ \ 
 \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | / \/  \ (_| | || (__| | | /\/ /_ | |_\ \_/ / |_) |
  \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  \_____/\__,_|\__\___|_| |_\____/  \__|\___/| .__/ 
                                                                                                |_|           
	""")
	print("- Starting BatchItUp! -\n- Version", VERSION, "-")

def check_str(checkThis):
	if (isinstance(checkThis, str)):
		return True
	return False

def check_file_exists(checkThis):
	return os.path.isfile(checkThis)

def get_sys_user():
	return pwd.getpwuid(os.getuid())[0]

def main(database, table, chunks, verbose=False, defaults=False, user=False, password=False):
	welcome_banner()
	# begin the dump
	if (defaults):
		batchitup.mysql_dump(database, table, defaults=defaults)
	else:
		batchitup.mysql_dump(database, table, user=user, password=password)

	insertPattern = "INSERT INTO"
	deletePattern = "DELETE"
	resultFile = "batchitup.sql"

	if (check_file_exists(resultFile)):
		batchitup.grep_file(resultFile, insertPattern)

	if not (os.path.exists("inserts")):
		os.makedirs("inserts")

	

if (__name__ == "__main__"):
	parser = argparse.ArgumentParser(description="Arguments for BatchItUp", allow_abbrev=True)
	parser.add_argument("-c", "--defaults", default=False)
	parser.add_argument("-u", "--user", default=False)
	parser.add_argument("-p", "--password", default=False)
	parser.add_argument("-d", "--database", default=False, required=True)
	parser.add_argument("-t", "--table", default=False, required=True)
	parser.add_argument("-i", "--inserts", default=True, action="store_true")
	parser.add_argument("-x", "--deletes", default=False, action="store_true")
	parser.add_argument("-s", "--chunk", default=500)
	parser.add_argument("-v", "--verbose", action="store_true")
	parser.add_argument("-l", "--log", default="./batchitup.log")
	args = parser.parse_args()

	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	logger_handler = logging.FileHandler(args.log)
	logger_handler.setLevel(logging.INFO)
	if (args.verbose):
		logger.setLevel(logging.DEBUG)
	logger_formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(process)d:%(levelname)s-%(message)s')
	logger_handler.setFormatter(logger_formatter)
	logger.addHandler(logger_handler)
	logger.info("Completed configuring logging")

	'''
	Check if the user entered in a path and filename to a defaults file or if they
	prefer to use a username and password combo for access to MySQL. Log responses,
	than checks if a database, table, and chunk number flag has been entered.
	'''
	logger.info("Checking inputs to see if they are valid")
	if ((args.defaults) and (check_file_exists(args.defaults))):
		logger.info("Using the defaults file %s" % args.defaults)
		if ((check_str(args.database)) and (check_str(args.table))):
			logger.info("Starting program on table: %s on %s : chunking by: %d" % (args.database, args.table, args.chunk))
			main(args.database, args.table, args.chunk, defaults=args.defaults)
	elif ((check_str(args.user)) and  (check_str(args.password))):
		logger.info("Using the user and password %s" % args.defaults)
		if ((check_str(args.database)) and (check_str(args.table))):
			logger.info("Starting program on table: %s on %s : chunking by: %d" % (args.database, args.table, args.chunk))
			main(args.database, args.table, args.chunk, user=args.user, password=args.password)
	else:
		logger.error("Neither defaults file or user and password entered")
		print("Please enter some of them arguments, either a defaults file or user and password")











