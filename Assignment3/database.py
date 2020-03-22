#!/usr/bin/env python
# ---------------------------------------------------------------------
# database.py
# Authors: Helen Chen & Angela Li
# ---------------------------------------------------------------------
from sqlite3 import connect
from collections import defaultdict
from format import readableRegResults
from os import path
from argv import checkRegDetailsArgv
from sys import argv, stderr, exit
# ---------------------------------------------------------------------

# querying


def regdatabase(commands):
    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        stderr.write('reg: missing database reg.sqlite file\n')
        exit(1)
    connection = connect(DATABASE_NAME)
    cursor = connection.cursor()
    keys = list(commands.keys())
    values = list(commands.values())
    if(len(commands) > 1):
        values.pop(0)
        keys.pop(0)

        stmtStr = 'SELECT classid, dept, coursenum, area, title '
        stmtStr += 'FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid '
        stmtStr += 'INNER JOIN classes ON crosslistings.courseid = classes.courseid '

        stmtStr += 'WHERE '
        stmtStr += keys[0][1:] + ' COLLATE UTF8_GENERAL_CI LIKE ?'
        for i in range(1, len(keys)):
            stmtStr += ' AND ' + keys[i][1:] + \
                ' COLLATE UTF8_GENERAL_CI LIKE ?'
        stmtStr += ' ESCAPE "#" '
        stmtStr += ' ORDER BY dept ASC, coursenum ASC, classid ASC'
        cursor.execute(stmtStr, values)

    else:
        stmtStr = 'SELECT classid, dept, coursenum, area, title FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON crosslistings.courseid = classes.courseid '
        stmtStr += 'ORDER BY dept ASC, coursenum ASC, classid ASC'
        cursor.execute(stmtStr)
    row = cursor.fetchall()
    cursor.close()
    connection.close()
    return(row)


def truncString(row, label):
    section = ''
    charcount = len(label)
    phrase = str(row[0]).split(' ')
    line = ''
    for word in phrase:
        if (charcount + len(word) + 1 > 72):
            section += line
            section += '\n'
            charcount = len(word)
            line = word + ' '
        else:
            line += word + ' '
            charcount += len(word) + 1
    if (line != ''):
        section += line
    section += '\n'
    section += '\n'
    return section


def createString(row, col, string):  # prints human readable form for single column query
    if col == 'courseid':
        section = 'Course Id: ' + str(row[0]) + '\n' + '\n'
        string += section
    if col == 'days':
        section = 'Days: ' + row[0] + '\n'
        string += section
    if col == 'starttime':
        section = 'Start time: ' + row[0] + '\n'
        string += section
    if col == 'endtime':
        section = 'End time: ' + row[0] + '\n'
        string += section
    if col == 'bldg':
        section = 'Building: ' + row[0] + '\n'
        string += section
    if col == 'roomnum':
        section = 'Room: ' + row[0] + '\n' + '\n'
        string += section
    if col == 'area':
        section = 'Area: ' + row[0] + '\n' + '\n'
        string += section
    if col == 'title':
        string += 'Title: '
        string += truncString(row, 'Title: ')
    if col == 'descrip':
        string += 'Description: '
        string += truncString(row, 'Description: ')
    if col == 'prereqs':
        string += 'Prerequisites: '
        string += truncString(row, 'Prerequisites: ')
    return string


# Query database for a single column
def querySingle(stmt, connection, classid, readable, col, string):
    cursor = connection.cursor()
    cursor.execute(stmt, [classid])
    row = cursor.fetchone()
    string = createString(row, col, string)
    cursor.close()
    return string

# gets all the information from regdetails


def regDetailsDatabase(classid, readable):
    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        stderr.write('regdetails: missing database reg.sqlite file\n')
        exit(1)
    connection = connect(DATABASE_NAME)
    # query courseid, days, start time, end time, building, roomnum from classes
    queryCourse = 'SELECT courseid FROM classes WHERE classid = ?'
    queryDays = 'SELECT days FROM classes WHERE classid = ?'
    queryStart = 'SELECT starttime FROM classes WHERE classid = ?'
    queryEnd = 'SELECT endtime FROM classes WHERE classid = ?'
    queryBldg = 'SELECT bldg FROM classes WHERE classid = ?'
    queryRoom = 'SELECT roomnum FROM classes WHERE classid = ?'
    # query dept and coursenum from crosslistings table
    queryDeptnum1 = '(SELECT courseid FROM classes WHERE classid = ?) AS q1 ON q1.courseid = crosslistings.courseid ORDER BY dept, coursenum'
    queryDeptnum2 = 'SELECT dept, coursenum FROM crosslistings INNER JOIN '
    queryDeptnum2 += queryDeptnum1
    # query area, title, descrip, prereqs from courses table
    queryCrs = '(SELECT courseid FROM classes WHERE classid = ?) AS q1 ON q1.courseid = courses.courseid'
    queryArea = 'SELECT area FROM courses INNER JOIN '
    queryArea += queryCrs
    queryTitle = 'SELECT title FROM courses INNER JOIN '
    queryTitle += queryCrs
    queryDescrip = 'SELECT descrip FROM courses INNER JOIN '
    queryDescrip += queryCrs
    queryPrereqs = 'SELECT prereqs FROM courses INNER JOIN '
    queryPrereqs += queryCrs
    # query profnames from profs table
    queryCrs = '(SELECT courseid FROM classes WHERE classid = ?) AS q1 ON q1.courseid = coursesprofs.courseid) AS q2 ON q2.profid = profs.profid ORDER BY profname'
    queryProfid = '(SELECT profid FROM coursesprofs INNER JOIN '
    queryProfid += queryCrs
    queryProfs = 'SELECT profname FROM profs INNER JOIN '
    queryProfs += queryProfid

   # create a string of human readable format
    readableString = ''

    readableResults = defaultdict(list)
    # execute query from database courseid, days, starttime, endtime, building, roomnum
    readableString = querySingle(
        queryCourse, connection, classid, readable, 'courseid', readableString)
    readableString = querySingle(
        queryDays, connection, classid, readable, 'days', readableString)
    readableString = querySingle(
        queryStart, connection, classid, readable, 'starttime', readableString)
    readableString = querySingle(
        queryEnd, connection, classid, readable, 'endtime', readableString)
    readableString = querySingle(
        queryBldg, connection, classid, readable, 'bldg', readableString)
    readableString = querySingle(
        queryRoom, connection, classid, readable, 'roomnum', readableString)

    # query database for dept and coursenum
    cursor = connection.cursor()
    cursor.execute(queryDeptnum2, [classid])
    row = cursor.fetchone()
    while row is not None:
        """if readable == True:
            print('Dept and Number: ' + row[0] + ' ' + row[1])
        else:
            print(row[0], row[1])"""
        readableString += 'Dept and Number: ' + \
            str(row[0]) + ' ' + str(row[1]) + '\n'
        row = cursor.fetchone()
    """if readable == True:
        print('')"""
    cursor.close()

    # execute query for area, title, descrip, prereqs
    readableString = querySingle(
        queryArea, connection, classid, readable, 'area', readableString)
    readableString = querySingle(
        queryTitle, connection, classid, readable, 'title', readableString)
    readableString = querySingle(
        queryDescrip, connection, classid, readable, 'descrip', readableString)
    readableString = querySingle(
        queryPrereqs, connection, classid, readable, 'prereqs', readableString)

    # execute query for profnames
    cursor = connection.cursor()
    cursor.execute(queryProfs, [classid])
    row = cursor.fetchone()
    while row is not None:
   
        readableString += 'Professor: ' + row[0] + '\n'
        row = cursor.fetchone()
    cursor.close()

    connection.close()
    return readableString
