#!/usr/bin/env python

import sqlite3
from sys import argv

_, db_file_name, blank_file_name, output_file_name = argv

conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

output_file = open(output_file_name, "w")

genome_query = '''select
	genotype
from
	genome
where
	chromosome = ? and
	position = ? and
	identifier = ?
'''

for i, line in enumerate(open(blank_file_name, "r")):
	if i != 0:
		output_file.write("\r\n")
	if line == "":
		break
		
	line = line.rstrip()
	output_file.write(line)
	
	if line.startswith("#"):
		continue
	
	try:
		identifier, chromosome, position = line.split("\t")[:3]
	except:
		continue
	
	cursor.execute(genome_query, (chromosome, int(position), identifier))
	row = cursor.fetchone()
	if row is None:
		output_file.write("\t--")
		continue
	
	output_file.write("\t" + row[0])

output_file.write("\r\n")
output_file.close()

conn.close()