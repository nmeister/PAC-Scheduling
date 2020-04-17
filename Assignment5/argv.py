#!/usr/bin/env python
#---------------------------------------------------------------------
# argv.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

from sys import argv, stderr, exit

# reg: checks for an invalid key for non-human readable (no -h). Valid keys are dept, coursenum,
# area, and title


def invalidKey(length, argv):
    i = 1
    invalid = False
    while (i < length):
        if ((argv[i] != '-dept') and (argv[i] != '-coursenum') and (argv[i] != '-area') and
                (argv[i] != '-title')):
            return True
        i += 2


# reg: checks for an invalid key with -h. Valid keys are dept, coursenum, area, and title
def invalidKeyH(length, argv):
    i = 2
    invalid = False
    while (i <= length):
        if ((argv[i] != '-dept') and (argv[i] != '-coursenum') and (argv[i] != '-area') and
                (argv[i] != '-title')):
            return True
        i += 2

# Parses the arguments given by argv into keys and values. Returns a list commands consisting
# of keys and corresponding values


def regParse(argv):
    i = 1  # tracks number of words parsed from arguments
    commands = {}  # list of parsed commands consisting of key and value

    # if argument is program name, return blank commands list
    if (len(argv) == 1):
        return (commands)

    # parse -h. If NO, put 'NO' into commands and proceed. If YES, put 'YES' into commands and
    # increment i
    commands['-h'] = 'NO'
    if argv[1] == '-h':
        commands['-h'] = 'YES'
        i += 1

    # parse arguments following h
    while i < len(argv):
        # check for duplicate keys entered
        if argv[i] in commands:
            stderr.write('reg: duplicate key\n')
            exit(1)
        # check for missing value and invalid key when -h (if yes, needs even arguments)
        if (len(argv) % 2 != 0) and (commands['-h'] == 'YES'):
            if (invalidKeyH(len(argv), argv)):
                stderr.write('reg: invalid key\n')
            else:
                stderr.write('reg: missing value\n')
            exit(1)
        # check for missing value and invalid key when no -h (if no, needs odd arguments)
        if (len(argv) % 2 == 0) and (commands['-h'] == 'NO'):
            if (invalidKey(len(argv), argv)):
                stderr.write('reg: invalid key\n')
            else:
                stderr.write('reg: missing value\n')
            exit(1)
        # if '_' in word, insert # in front as wildcard handler
        if '_' in argv[i+1]:
            udscr = argv[i+1].find('_')
            oldarg = argv[i+1]
            argv[i+1] = oldarg[0:udscr] + str('#_') + oldarg[udscr+1:]
        # if '%' in word, insert # in front as wildcard handler
        if '%' in argv[i+1]:
            prcnt = argv[i+1].find('%')
            oldarg = argv[i+1]
            argv[i+1] = oldarg[0:prcnt] + str('#%') + oldarg[prcnt+1:]
        # put key value pair into commands followed by '%'
        commands[argv[i]] = '%' + argv[i+1] + '%'
        i += 2  # parse next key
    return(commands)

# checks arguments entered for regdetails program


def checkRegDetailsArgv(argv):
    length = len(argv)
    classId = 0
    # check that a classid was entered for no -h
    if (length == 1):
        stderr.write('regdetails: missing classid\n')
        exit(1)
    # check that a classid was entered for -h
    if (length == 2) and ((argv[1]) == '-h'):
        stderr.write('regdetails: missing classid\n')
        exit(1)
    # check that classid is an integer for no -h
    if (length == 2) and ((argv[1]) != '-h'):
        if (isinstance(int(argv[1]), int) == False):
            stderr.write('regdetails: classid is not an integer')
            exit(1)
        else:
            classId = argv[1]
    # check that classid is an integer for -h
    if (length == 3) and ((argv[1]) == '-h'):
        if (isinstance(int(argv[2]), int) == False):
            stderr.write('regdetails: classid is not an integer')
            exit(1)
        else:
            classId = argv[2]
    # check proper amount of arguments for no -h
    if (length > 2) and ((argv[1]) != '-h'):
        stderr.write('regdetails: too many arguments\n')
        exit(1)
    # check proper amount of arguments for -h
    if (length > 3) and ((argv[1]) == '-h'):
        stderr.write('regdetails: too many arguments\n')
        exit(1)
    return(classId)

