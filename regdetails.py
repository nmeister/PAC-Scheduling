#!/usr/bin/env python
#---------------------------------------------------------------------
# regdetails.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect

#---------------------------------------------------------------------
# mangela

def database(DATABASE_NAME, classId):
	connection = connect(DATABASE_NAME)
	cursor = connection.cursor()
	stuff = ['courseid', 'days', 'starttime', 'endtime', 'bldg', 'roomnum', 'dept', 'coursenum', 'area', 'title', 'descrip', 'prereqs', 'profname']
	stmtStr = 'SELECT crosslistings.courseid, days, starttime, endtime, bldg, roomnum, dept, coursenum, area, title, descrip, prereqs, profname FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON crosslistings.courseid = classes.courseid INNER JOIN profs'
	#stmtStr = 'SELECT days, starttime, endtime, bldg, roomnum, dept, coursenum, area, title, descrip, prereqs, profname FROM crosslistings INNER JOIN courses INNER JOIN classes INNER JOIN profs'
	stmtStr += ' WHERE classid= ? '
	cursor.execute(stmtStr, [classId])
	results = {} 
	row = cursor.fetchone()
	"""while row is not None: 
		for x in row: 

			if x not in results:"""
	row = cursor.fetchall()
	cursor.close()
	connection.close()
	return(row)

def dets(row): 
	for x in row: 
		print(x)

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
    row = database(DATABASE_NAME, classId)
    dets(row)


#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)