#!/usr/bin/env python
#---------------------------------------------------------------------
# regdetails.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
from collections import defaultdict

#---------------------------------------------------------------------
# mangela

def database(DATABASE_NAME, classId):
	connection = connect(DATABASE_NAME)
	cursor = connection.cursor()
	stuff = ['courseid', 'days', 'starttime', 'endtime', 'bldg', 'roomnum', 'dept', 'coursenum', 'area', 'title', 'descrip', 'prereqs', 'profname']
	stmtStr = 'SELECT crosslistings.courseid, days, starttime, endtime, bldg, roomnum, dept, coursenum, area, title, descrip, prereqs, profname '
	stmtStr += 'FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON '
	stmtStr += 'crosslistings.courseid = classes.courseid INNER JOIN coursesprofs ON classes.courseid = coursesprofs.courseid INNER JOIN profs ON coursesprofs.profid = profs.profid '
	stmtStr += 'WHERE classes.classid= ? '
	stmtStr += 'ORDER BY dept, coursenum, profname'
	cursor.execute(stmtStr, [classId])
	results = defaultdict(list)
	row = cursor.fetchone()
	coursenum = row[7]
	while row is not None: 
		for i in range(0, len(stuff)): 
			if row[i] not in results[stuff[i]]:
				results[stuff[i]].append(row[i])
		row = cursor.fetchone()
	cursor.close()
	connection.close()
	return(results)

def dets(results): 
	coursenum = str(results['coursenum'][0])
	for x in results.keys(): 
		for y in results.get(x): 
			if (x == 'dept'):
				print(str(y), end =' ')
				print(coursenum)
			elif (x == 'coursenum'):
				continue
			else: 
				print(y)


def main(argv):
    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        raise Exception('Database connection failed')
    length = len(argv)
    classId = 0
    if length == 1:
    	print('regdetails: missing classid')
    	exit(1)
    if length == 2: 
    	if (isinstance(int(argv[1]), int) == False):
    		print('regdetails: classid is not an integer 1 ')
    		exit(1)
    	else: 
    		classId = argv[1]
    if length >= 3: 
    	if (argv[1].isnumeric() and argv[2].isnumeric()): 
    		print('regdetails: too many arguments')
    		exit(1)
    	if not isinstance(argv[2], int): 
    		print('regdetails: classid is not an integer 2')
    		exit(1)
    results = database(DATABASE_NAME, classId)
    dets(results)


#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)