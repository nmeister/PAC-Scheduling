#!/usr/bin/env python
#---------------------------------------------------------------------
# reg.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from os import path
from format import regformat, readable
from database import regdatabase
from argv import regParse
from sys import argv, stderr, exit

#---------------------------------------------------------------------
# mangela

def main(argv):

    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        raise Exception('reg: database reg.sqlite not found')
    parsedArgs = regParse(argv)
    parsedArgsValues = list(parsedArgs.values())
    isHumanReadable = False
    if (len(parsedArgs) > 0):
        isHumanReadable = parsedArgsValues.pop(0)
    results = regdatabase(parsedArgs, DATABASE_NAME)

    if (isHumanReadable == 'YES'):
        readable(results)
    else: 
        regformat(results)

#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
