#!/usr/bin/env python

#-----------------------------------------------------------------------
# course.py
# Author: Helen & Angela 
#-----------------------------------------------------------------------

# trying to modularize course as an object 
class Course:
   
    def __init__(self, classid, dept, num, area, title):
        self._classid = classid
        self._dept = dept
        self._num = num
        self._area = area
        self._title = title

    """def __str__(self):
        return self._author + ', ' + self._title + ', ' + \
           str(self._) """

    def getClassId(self):
        return self._classid

    def getDept(self):
        return self._dept

    def getNum(self):
        return self._num

    def getArea(self):
        return self._area

    def getTitle(self):
        return self._title

