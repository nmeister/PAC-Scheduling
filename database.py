#!/usr/bin/env python
#---------------------------------------------------------------------
# database.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from sqlite3 import connect
from collections import defaultdict

#---------------------------------------------------------------------

def regdatabase(commands, DATABASE_NAME):
    connection = connect(DATABASE_NAME)
    cursor = connection.cursor()
    keys = list(commands.keys())
    values = list(commands.values())
    if(len(commands) != 0):
        values.pop(0)
        keys.pop(0)

        stmtStr = 'SELECT classid, dept, coursenum, area, title ' 
        stmtStr += 'FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid '
        stmtStr += 'INNER JOIN classes ON crosslistings.courseid = classes.courseid '
       
        stmtStr += 'WHERE '
        stmtStr += keys[0][1:] + ' COLLATE UTF8_GENERAL_CI LIKE ?'
        for i in range(1, len(keys)):
            stmtStr +=  ' AND ' + keys[i][1:] + ' COLLATE UTF8_GENERAL_CI LIKE ?'
        stmtStr += 'ORDER BY dept ASC, coursenum ASC, classid ASC'
        cursor.execute(stmtStr, values)
     
    else: 
        stmtStr = 'SELECT classid, dept, coursenum, area, title FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON crosslistings.courseid = classes.courseid '
        stmtStr += 'ORDER BY dept ASC, coursenum ASC, classid ASC'
        cursor.execute(stmtStr)
    row = cursor.fetchall()
    cursor.close()
    connection.close()
    return(row)  


def regDetailsdatabase(DATABASE_NAME, classId):
	connection = connect(DATABASE_NAME)
	cursor = connection.cursor()
	stuff = ['courseid', 'days', 'starttime', 'endtime', 'bldg', 'roomnum', 'dept', 'coursenum', 'area', 'title', 'descrip', 'prereqs', 'profname']
	stmtStr = 'SELECT crosslistings.courseid, days, starttime, endtime, bldg, roomnum, dept, coursenum, area, title, descrip, prereqs, profname '
	stmtStr += 'FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON '
	stmtStr += 'crosslistings.courseid = classes.courseid INNER JOIN coursesprofs ON '
	stmtStr += 'classes.courseid = coursesprofs.courseid INNER JOIN profs ON coursesprofs.profid = profs.profid '
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