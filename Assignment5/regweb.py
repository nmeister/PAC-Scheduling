#!/usr/bin/env python

# -----------------------------------------------------------------------
# regweb.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sys import argv, exit, stderr
from argv import regParse
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from databaseClass import Database
# -----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

# -----------------------------------------------------------------------


def argMake(dept, num, area, title):
    args = []
    args.append('regweb.py')
    if (dept != ''):
        args.append('-dept')
        args.append(dept)
    if (num != ''):
        args.append('-coursenum')
        args.append(num)
    if (area != ''):
        args.append('-area')
        args.append(area)
    if (title != ''):
        args.append('-title')
        args.append(title)
    return args


def queryMake(dept, num, area, title):
    query = []
    if dept == None:
        query.append('')
    else:
        query.append(dept)
    if num == None:
        query.append('')
    else:
        query.append(num)
    if area == None:
        query.append('')
    else:
        query.append(area)
    if title == None:
        query.append('')
    else:
        query.append(title)
    return query

# -----------------------------------------------------------------------


@app.route('/', methods=['GET'])
@app.route('/reg', methods=['GET'])
def reg():
    dept = request.args.get('dept')
    num = request.args.get('num')
    area = request.args.get('area')
    title = request.args.get('title')
    query = queryMake(dept, num, area, title)
    if ''.join(query) == '':
        commands = {}
    else:
        args = argMake(dept, num, area, title)
        commands = regParse(args)

    database = Database()
    error = database.connect()
    # if unavailable to connect to database because does not exist
    if (error is not None):
        html = render_template(error)
    else:
        courses = database.regDB(commands)
        # if database is corrupt 
        if courses == -100: 
            html = render_template('dberror.html',
                error="corrupt")
        else: 
            # renders this html with given fields 
            html = render_template('reg.html',
                               query=query,
                               courses=courses)
        database.disconnect()
    response = make_response(html)
    response.set_cookie('deptc', query[0])
    response.set_cookie('numc', query[1])
    response.set_cookie('areac', query[2])
    response.set_cookie('titlec', query[3])
    return response


def outputHtml(courses):
    html = ''
    for course in courses:
        html += '<tr><th>'
        html += '<a method="get"' 
        html += 'href="{{ url_for("regdetail", classid='
        html += str(course.getClassId())+ '}}"'
        html += 'id=' + str(course.getClassId())+ '}}">'
        html += str(course.getClassId()) + '</a></th>'
        html += '<th>' + course.getDept() + '</th>'
        html += '<th>' + str(course.getNum()) + '</th>'
        html += '<th>' + course.getArea() + '</th>'
        html += '<th>' + course.getTitle() + '</th>'
        html += '</tr>'
    print(html)
    return html 


@app.route('/results', methods=['GET'])
def results(): 
    dept = request.args.get('dept')
    print(dept)
    num = request.args.get('num')
    area = request.args.get('area')
    title = request.args.get('title')
    query = queryMake(dept, num, area, title)
    if ''.join(query) == '':
        commands = {}
    else:
        args = argMake(dept, num, area, title)
        print(args)
        commands = regParse(args)
        print(commands)
    database = Database()
    error = database.connect()
    # if unavailable to connect to database because does not exist
    if (error is not None):
        html = render_template(error)
    else:
        courses = database.regDB(commands)
        print(courses)
        # if database is corrupt 
        if courses == -100: 
            html = render_template('dberror.html',
                error="corrupt")
        else: 
            # renders this html with given fields 
            html = render_template('form.html', query=query, courses=courses)
            #html = outputHtml(courses)
        database.disconnect()
    response = make_response(html)
    response.set_cookie('deptc', query[0])
    response.set_cookie('numc', query[1])
    response.set_cookie('areac', query[2])
    response.set_cookie('titlec', query[3])
    # returns the html as the response 
    return response

# -----------------------------------------------------------------------


@app.route('/regdetail', methods=['GET'])
def regdetail():
    dept = request.cookies.get('deptc')
    num = request.cookies.get('numc')
    area = request.cookies.get('areac')
    title = request.cookies.get('titlec')
    query = queryMake(dept, num, area, title)
    classid = request.args.get("classid")
    # if empty or not given 
    if classid.strip() == '' or classid.strip() == ' ' or classid == None:
        html = render_template('invalidclassid.html')
        response = make_response(html)
        return response
    # if it is not a numeric number 
    if not classid.isnumeric():
        html = render_template('invalidclassid.html',
            error="NaN")
        response = make_response(html)
        return response
    database = Database()
    error = database.connect()
    # if database not found 
    if (error is not None):
        html = render_template(error)
    else:
        # if it does exist, make a search 
        details = database.regDDB(classid)
        # error handling for non-existing class 
        if details == None:
            html = render_template('classiderror.html',
                classid=classid)
        # if database is corrupt 
        elif details == -100: 
            html = render_template('dberror.html',
                error="corrupt")
        # if all is well, do this 
        else:
            html = render_template('regdetail.html', 
                classid=classid, details=details, query=query)
        database.disconnect()
    response = make_response(html)
   # response.set_cookie('deptc', query[0])
    #response.set_cookie('numc', query[1])
    #response.set_cookie('areac', query[2])
    #response.set_cookie('titlec', query[3])
    return response


# -----------------------------------------------------------------------
if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    if (argv[1].isnumeric() == False):
        stderr.write('regweb: port number is not an integer')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
