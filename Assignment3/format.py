#!/usr/bin/env python
#---------------------------------------------------------------------
# format.py
# Authors: Helen Chen & Angela Li
#---------------------------------------------------------------------


def regform(rows):
	final = ''
	for x in rows: 
		pstr = ''
		for j in x: 
			pstr += str(j) + '\t'
		final += pstr + '\n'
	return final


def regformat(rows):
	for x in rows: 
		pstr = ''
		for j in x: 
			pstr += str(j) + '\t'
			print(pstr)


def regdformat(results): 
	coursenum = str(results['coursenum'][0])
	for x in results.keys(): 
		for y in results.get(x): 
			if (x == 'dept'):
				print(str(y), end='')
				print(coursenum)
			elif (x == 'coursenum'):
				continue
			else: 
				print(y)

def read(row):
        pstr = ''
        pstr += str(row[0]).rjust(5) 
        pstr += str(row[1]).rjust(4)
        pstr += str(row[2]).rjust(5)
        pstr += str(row[3]).rjust(4)
        pstr += ' ' + row[4]
        return pstr
                                

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
                        print('%-23s' % ' ', end = '')
                        total = len(headers[0]) + len(headers[1]) + len(headers[2]) + len(headers[3])
                        line = word + ' '
                        lineCount += 1
                    else:   
                        line += word + ' '
                        total += len(word) + 1
                if (line != '' and lineCount > 0): 
                    print(line.ljust(49), end = '')
                # for the first line to be printed out 
                else: 
                	print(line.ljust(49), end = '')
       
            else: 
                print(str(col).rjust(rightJ), end = ' ')
            count += 1
        print('\n', end = '')



def pregdformat(results): 
	coursenum = str(results['coursenum'][0])
	deptcount = 0
	for label in results.keys():
		for entry in results.get(label):
			if (label == 'courseid'):
				print('Course Id: ', end='')
			if (label == 'days'):
				print('Days: ', end='')
			if (label == 'starttime'):
				print('Start time: ', end='')
			if (label == 'endtime'):
				print('End time: ', end='')
			if (label == 'bldg'):
				print('Building: ', end='')
			if (label == 'roomnum'):
				print('Room: ', end='')
			if (label == 'dept'):
				print('Dept and Number: ', end='')
				print(str(entry), end=' ')
				if (len(results['coursenum']) != 1):
					print(results['coursenum'][deptcount])
					deptcount += 1
				else: 
					print(coursenum)
			if (label == 'area'):
				print('Area: ', end='')
			if (label == 'title'):
				print('Title: ', end='')
			if (label == 'descrip'):
				print('Description: ', end='')
			if (label == 'prereqs'):
				print('Prerequisites: ', end='')
			if (label == 'profname'):
				print('Professor: ', end='')
				print(entry)
			elif (label == 'coursenum'):
				continue
			if (label == 'days'
				or label == 'starttime' or label == 'endtime'
				or label == 'bldg' or label == 'room'):
				print(entry, end='')
			elif (label == 'descrip' or label == 'title' or label == 'prereqs'):
				charcount = len(label)
				phrase = str(entry).split(' ')
				lenline = len(entry)
				line = ''
				for word in phrase:
					if (charcount + len(word) + 1 > 72):
						print(line)
						charcount = len(word)
						line = word + ' '
					else:
						line += word + ' '
						charcount += len(word) + 1
				if (line != ''):
					print(line)
			elif (label != 'dept' and label != 'profname'):
				print(entry)
		print('\n', end='')






def readableTruncate(row, label):
    charcount = len(label)
    phrase = str(row[0]).split(' ')
    line = ''
    for word in phrase:
        if (charcount + len(word) + 1 > 72):
            print(line)
            charcount = len(word)
            line = word + ' '
        else:
            line += word + ' '
            charcount += len(word) + 1
    if (line != ''):
        print(line + '\n')


def readableRegResults(row, col):  # prints human readable form for single column query
    if col == 'courseid':
        print('Course Id: ' + str(row[0]) + '\n')
    if col == 'days':
        print('Days: ' + row[0])
    if col == 'starttime':
        print('Start time: ' + row[0])
    if col == 'endtime':
        print('End time: ' + row[0])
    if col == 'bldg':
        print('Building: ' + row[0])
    if col == 'roomnum':
        print('Room: ' + row[0] + '\n')
    if col == 'area':
        print('Area: ' + row[0] + '\n')
    if col == 'title':
        print('Title: ', end='')
        readableTruncate(row, 'Title: ')
    if col == 'descrip':
        print('Description: ', end='')
        readableTruncate(row, 'Description: ')
    if col == 'prereqs':
        print('Prerequisites: ', end='')
        readableTruncate(row, 'Prerequisites: ')