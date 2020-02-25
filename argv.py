#!/usr/bin/env python
#---------------------------------------------------------------------
# argv.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------

def regParse(argv):
    i = 1
    commands = {}
#    if (len(argv) == 1) or (len(argv) == 2 and argv[1] == '-h'):
    if (len(argv) == 1):
        return (commands)

    commands['-h'] = 'NO'
    if argv[1] == '-h':
        commands['-h'] = 'YES'
        i+=1

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
            argv[i+1] = oldarg[0:udscr] + '\_' + oldarg[udscr+1:]
        if '%' in argv[i+1]:
            udscr = argv[i+1].find('%')
            oldarg = argv[i+1]
            argv[i+1] = oldarg[0:udscr] + '\%' + oldarg[udscr+1:]
        commands[argv[i]] = '%' + argv[i+1] + '%'
        i += 2
    return(commands)


def checkRegDetailsArgv(argv): 
	length = len(argv)
	classId = 0
	if length == 1:
		print('regdetails: missing classid')
		exit(1)
	if length == 2: 
		if (isinstance(int(argv[1]), int) == False):
			print('regdetails: classid is not an integer 1')
			exit(1)
		else: 
			classId = argv[1]
	if length >= 3: 
		if (argv[1].isnumeric() and argv[2].isnumeric()): 
			print('regdetails: too many arguments')
			exit(1)
		if not (argv[2].isnumeric()): 
			print('regdetails: classid is not an integer 2')
			exit(1)
		if (argv[1] == '-h' and argv[2].isnumeric()): 
			classId = argv[2]
	return(classId)