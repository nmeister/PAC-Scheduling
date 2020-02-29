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
    commands = regParse(argv)
    values = list(commands.values())
    check = values.pop(0)
    rows = regdatabase(commands, DATABASE_NAME)

    if (check == 'YES'):
        readable(rows)
    else: 
        regformat(rows)

#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
