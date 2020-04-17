#!/usr/bin/env python

#-----------------------------------------------------------------------
# course.py
# Author: Helen & Angela 
#-----------------------------------------------------------------------

# trying to modularize course as an object 
class CourseDets:

    def __init__(self, classid, courseid, 
                days, start, end, bldng, 
                rm, deptnum, area, title, 
                descrip, preq, prof):
        self._classid = classid
        self._courseid = courseid
        self._days = days
        self._start = start
        self._end = end
        self._bldng = bldng
        self._rm = rm
        self._deptnum = deptnum
        self._area = area
        self._title = title
        self._descrip = descrip
        self._preq = preq
        self._prof = prof

    """def __str__(self):
        return self._author + ', ' + self._title + ', ' + \
           str(self._price)"""

    def getClassId(self):
        return self._classid

    def getCourseId(self):
        return self._courseid

    def getDays(self):
        return self._days

    def getStart(self):
        return self._start

    def getEnd(self):
        return self._end

    def getBldng(self):
        return self._bldng

    def getRm(self):
        return self._rm

    def getDeptnum(self):
        return self._deptnum

    def getArea(self):
        return self._area

    def getTitle(self):
        return self._title

    def getDescrip(self):
        return self._descrip

    def getPreq(self):
        return self._preq

    def getProf(self):
        return self._prof

