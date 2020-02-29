#!/usr/bin/env python
#---------------------------------------------------------------------
# regdetails.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from os import path
from format import regdformat, pregdformat
from database import regDetailsdatabase
from argv import checkRegDetailsArgv
from sys import argv, stderr, exit

#---------------------------------------------------------------------
# mangela


def main(argv):
    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        raise Exception('Database connection failed')
    classId = checkRegDetailsArgv(argv)
    results = regDetailsdatabase(DATABASE_NAME, classId)
    if (argv[1] == '-h'): 
    	pregdformat(results)
    else:
    	regdformat(results)


#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)