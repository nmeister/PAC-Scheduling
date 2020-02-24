#!/usr/bin/env python
#---------------------------------------------------------------------
# reg.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect

#---------------------------------------------------------------------
# mangela

def parse(argv):
    i = 1
    commands = {}
    if (len(argv) == 1) or (len(argv) == 2 and argv[1] == '-h'):
        return (commands)

    if argv[1] == '-h':
        commands['-h'] = 'YES'
        i+=1
    else:
        commands['-h'] = 'NO'

    while i < len(argv): 
        if ((argv[i] != '-dept') and (argv[i] != '-coursenum') and (argv[i] != '-area') and 
            (argv[i] !='-title')):
            print('reg: invalid key')
            exit(1)
        if argv[i] in commands:
            print('reg: duplicate key')
            exit(1)
        if (len(argv) % 2 != 0) and (i == 2):
            print('reg: missing value')
            exit(1)
        if (len(argv) % 2 == 0) and (i != 2):
            print('reg: missing value')
            exit(1)   
        if '_' in argv[i+1]:
            udscr = argv[i+1].find('_')
            oldarg = argv[i+1]
            argv[i+1] = oldarg[0:udscr-1] + '\\' + oldarg[udscr:]
        if '%' in argv[i+1]:
            udscr = argv[i+1].find('%')
            oldarg = argv[i+1]
            argv[i+1] = oldarg[0:udscr-1] + '\\' + oldarg[udscr:]
        commands[argv[i]] = '%' + argv[i+1] + '%'
        i += 2

  

    return(commands)

  
def database(commands, DATABASE_NAME):
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


def format(rows):
   
    for x in rows: 
        pstr = ''
        for j in x: 
            pstr += str(j) + '\t'
        print(pstr)


def readable(rows): 
    headers = ['ClsId', 'Dept', 'CrsNum', 'Area', 'Title']
    print('ClsId Dept CrsNum Area Title')
    print('----- ---- ------ ---- -----')
    
    for row in rows: 
        pstr = ''
        count = 0
        rightJ = 0
        total = len(headers[0]) + len(headers[1]) + len(headers[2]) + len(headers[3])
        for col in row: 
            rightJ = len(headers[count])
            if (count == 4): 
                title = str(col).split(' ')
                line = ''
                lineCount = 0 
                for word in title:   
                    if (total + len(word) + 1 > 72): 
                        print(line.ljust(49))
                        total = len(headers[0]) + len(headers[1]) + len(headers[2]) + len(headers[3])
                        line = word + ' '
                        lineCount += 1
                    else:   
                        line += word + ' '
                        total += len(word) + 1
                if (line != '' and lineCount > 0): 
                    print('%-23s' % ' ', end = '')
                    print(line.ljust(49), end = '')
                else: 
                    print(line.ljust(49), end = '')
            else: 
                print(str(col).rjust(rightJ), end = ' ')
            count += 1
        print('\n', end = '')



def main(argv):

    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        raise Exception('reg: database reg.sqlite not found')
    commands = parse(argv)
    values = list(commands.values())
    check = values.pop(0)
    rows = database(commands, DATABASE_NAME)

    if (check == 'YES'):
        readable(rows)
    else: 
        format(rows)
    


#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
