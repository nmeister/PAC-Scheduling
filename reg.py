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

    if (len(argv) % 2 != 0) and (i == 2):
        print('reg: missing value')
        exit(1)

    if (len(argv) % 2 == 0) and (i != 2):
        print('reg: missing value')
        exit(1)

    while i < len(argv): 
        if ((argv[i] != '-dept') and (argv[i] != '-coursenum') and (argv[i] != '-area') and 
            (argv[i] !='-title')):
            print('reg: invalid key')
            exit(1)
        if argv[i] in commands:
            print('reg: duplicate key')
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
        #row   = cursor.fetchall()
        stmtStr = 'SELECT classid, dept, coursenum, area, title FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON crosslistings.courseid = classes.courseid '
        """stmtStr += keys[0][1:]
        for i in range(1, len(keys)):
             stmtStr += ', ' + keys[i][1:] 
        print(stmtStr)
        stmtStr += ' FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid '    """
        stmtStr += 'WHERE '
        stmtStr += keys[0][1:] + ' COLLATE UTF8_GENERAL_CI LIKE ?'
        for i in range(1, len(keys)):
            stmtStr +=  ' AND ' + keys[i][1:] + ' COLLATE UTF8_GENERAL_CI LIKE ?'
        stmtStr += 'ORDER BY dept ASC, coursenum ASC, classid ASC'
        cursor.execute(stmtStr, values)
        # print(stmtStr)
        """row = cursor.fetchone()
        print(row)
        print(stmtStr)

        while row is not None:
            print(row)
            row = cursor.fetchone() 
        cursor.close()
        connection.close()"""
    else: 
        stmtStr = 'SELECT classid, dept, coursenum, area, title FROM crosslistings INNER JOIN courses ON crosslistings.courseid = courses.courseid INNER JOIN classes ON crosslistings.courseid = classes.courseid '
        stmtStr += 'ORDER BY dept ASC, coursenum ASC, classid ASC'
        cursor.execute(stmtStr)
    row = cursor.fetchall()
    cursor.close()
    connection.close()
    return(row)  


def format(rows):
    # row is a big list that contains tuples 
    for x in rows: 
        pstr = ''
        for j in x: 
            pstr += str(j) + '\t'
            #print('\t')
        print(pstr)

# need to right justify and also 72 characters, not end in words 
def readable(rows): 
    headers = ['ClsId', 'Dept', 'CrsNum', 'Area', 'Title']
    print('ClsId Dept CrsNum Area Title')
    print('----- ---- ------ ---- -----')
    total = 23 
    for x in rows: 
        pstr = ''
        count = 0
        rightJ = 0
        for j in x: 
            rightJ = len(headers[count])
            # pstr += (str(j)).rjust(rightJ)
            if (count == 4): 
                split = str(j).split(' ')
                for word in split:         
                    if (total + len(word) > 72): 
                        print('\n', end = '')
                        total += len(word)
            else: 
                print(str(j).rjust(rightJ), end = ' ')
            count += 1
        # print(pstr)
        print('\n', end = '')


def main(argv):

    DATABASE_NAME = 'reg.sqlite'
    if not path.isfile(DATABASE_NAME):
        raise Exception('Database connection failed')
    commands = parse(argv)
    # print('outside')
    # print(commands)
    values = list(commands.values())
    # print(values)
    check = values.pop(0)
    rows = database(commands, DATABASE_NAME)
    #print(rows)
    if (check == 'YES'):
        readable(rows)
    else: 
        format(rows)
    


#---------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)
