#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Helen & Angela 
#-----------------------------------------------------------------------

from sqlite3 import connect
from os import path
from sys import argv, stderr, exit
from course import Course
from coursedets import CourseDets

#-----------------------------------------------------------------------

class Database:
    
    def __init__(self):
        self._connection = None

    def connect(self):      
        DATABASE_NAME = 'reg.sqlite'
        if not path.isfile(DATABASE_NAME):
            print('missing database reg.sqlite', file=stderr)
            return 'dberror.html'
        self._connection = connect(DATABASE_NAME)
        return None
                    
    def disconnect(self):
        self._connection.close()

    def regDB(self, commands):
        cursor = self._connection.cursor()
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
                stmtStr += ' AND ' + keys[i][1:] + ' COLLATE UTF8_GENERAL_CI LIKE ?'
            stmtStr += ' ESCAPE "#" '
            stmtStr += ' ORDER BY dept ASC, coursenum ASC, classid ASC'
            try: 
                cursor.execute(stmtStr, values)
            except Exception as e:
                return -100
        else:
            stmtStr = 'SELECT classid, dept, coursenum, area, title FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON crosslistings.courseid = classes.courseid '
            stmtStr += 'ORDER BY dept ASC, coursenum ASC, classid ASC'
            try: 
                cursor.execute(stmtStr)
            except Exception as e:
                return -100
        courses = []
        row = cursor.fetchone()
        while row is not None: 
            course = Course(row[0], row[1], row[2], row[3], row[4])
            courses.append(course)
            row = cursor.fetchone()
        cursor.close()
        return courses

    	
    def querySingle3(self, stmt, classid, col):
        cursor = self._connection.cursor()
        try: 
            cursor.execute(stmt, [classid])
        except Exception as e:
            return -100
        row = cursor.fetchone()
        if row == None:
            return None
        cursor.close()
        return row[0]

    def A3(self, classid, queryCourse, queryDays, queryStart, 
                queryEnd, queryBldg, queryRoom, queryArea, queryDeptnum2,
                queryTitle, queryPrereqs, queryProfs, queryDescrip):
        q3 = self.querySingle3
        courseid = q3(queryCourse, classid, 'courseid')
        if courseid == -100: 
            return -100
        days = q3(queryDays, classid, 'days')
        if days == -100: 
            return -100
        start = q3(queryStart, classid, 'starttime')
        if start == -100: 
            return -100
        end = q3(queryEnd, classid, 'endtime')
        if end == -100: 
            return -100
        bldng = q3(queryBldg, classid, 'bldg')
        if bldng == -100: 
            return -100
        rm = q3(queryRoom, classid, 'roomnum')
        if rm == -100: 
            return -100

        # query database for dept and coursenum
        cursor = self._connection.cursor()
        try:
            cursor.execute(queryDeptnum2, [classid])
        except Exception as e:
            return -100
        row = cursor.fetchone()
        deptnum = []
        while row is not None:
            deptnum.append(str(row[0]) + ' ' + str(row[1]))
            row = cursor.fetchone()
   
        cursor.close()

        # execute query for area, title, descrip, prereqs
        area = q3( queryArea, classid, 'area')
        if area == -100:
            return -100
        title = q3(queryTitle, classid, 'title')
        if title == -100:
            return -100
        descrip = q3(queryDescrip, classid, 'descrip')
        if descrip == -100:
            return -100
    
        preq = q3(queryPrereqs, classid, 'prereqs')
        if preq == -100:
            return -100
        # execute query for profnames
        cursor = self._connection.cursor()
        try: 
            cursor.execute(queryProfs, [classid])
        except Exception as e:
            return -100
        row = cursor.fetchone()
        profs = []
        while row is not None:
            profs.append(row[0])
            row = cursor.fetchone()
        cursor.close()
        dets = CourseDets(classid, courseid, days, 
                start, end, bldng, 
                rm, deptnum, area, title, 
                descrip, preq, profs)
        return dets

    def regDDB(self, classid):
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
        dets = self.A3(classid, queryCourse, queryDays, queryStart, 
                    queryEnd, queryBldg, queryRoom, queryArea, queryDeptnum2,
                    queryTitle, queryPrereqs, queryProfs, queryDescrip)
        if dets == None:
            return None
        if dets == -100: 
            return -100
        return dets


#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    database.disconnect()


