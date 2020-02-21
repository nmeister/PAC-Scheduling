#!/usr/bin/env python
#---------------------------------------------------------------------
# reg.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect

#---------------------------------------------------------------------

def parse(argv):
    i = 1
    commands = {}
    #c checks for -h 
    if argv[1] == '-h':
        commands['-h'] = 'YES'
        i+=1
    else:
        commands['-h'] = 'NO'
    # checks for valid arguments 
    if (len(argv) % 2 != 0) and (i == 2):
        print('reg: missing value')
        exit(1)
        # do something error
    if (len(argv) % 2 == 0) and (i != 2):
        print('reg: missing value')
        exit(1)
        # do something error 
    # parse commands from arg 
    while i < len(argv): 
        if ((argv[i] != '-dept') and (argv[i] != '-coursenum') and (argv[i] != '-area') and 
            (argv[i] !='-title')):
            print('reg: invalid key')
            exit(1)
        if argv[i] in commands:
            print('reg: duplicate key')
            exit(1)
        commands[argv[i]] = argv[i+1];
        i += 2
    # print(commands)
    return (commands)

  
def database(commands, cursor):
    keys = list(commands.keys())
    values = list(commands.values())
    print(keys)
    stmtStr = 'SELECT '
    stmtStr += keys[1][1:]
    for i in range(2, len(keys)):
         stmtStr += ', ' + keys[i][1:] 
    print(stmtStr)
    stmtStr += ' FROM crosslistings, courses '
    stmtStr += 'WHERE '
    stmtStr += keys[1][1:] + ' = ?'
    for i in range(2, len(keys)):
        stmtStr +=  ' AND ' + keys[i][1:] + ' = ?'

    print(stmtStr)
    cursor.execute(stmtStr, values)



def main(argv):

    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        raise Exception('Database connection failed')
    commands = parse(argv)
    # print('outside')
    print(commands)
   
    connection = connect(DATABASE_NAME)
    cursor = connection.cursor()
    database(commands, cursor)

    


#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
