#!/usr/bin/env python

#-----------------------------------------------------------------------
# regweb.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, exit
from common import getHeader, getFooter
from database import regdatabase
from format import read
from flask import Flask, request, make_response, redirect, url_for

#-----------------------------------------------------------------------

app = Flask(__name__)
   
#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    
    html = ''
    html += '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += '<title>Registrar\'s Office Class Search </title>'
    html += '<style>'
    html += 'th {text-align:left; font-weight: normal}'
    html += '</style>'
    html += '</head>'
    html += '<body>'
    html += '<h1>Registrar\'s Office</h1>'
    html += '<h2>Class Search</h2>'
    html += '<hr>'
    html += '<form action="searchresults" method="get">'
    html += '<table style= "width:1%">'
    html += '<tr><th style = "text-align:right">Dept: </th>'
    html += '<th><input type="text" name="dept"></th></tr>'
    html += '<tr><th style = "text-align:right">Number: </th>'
    html += '<th><input type="text" name="num"></th>'
    html += '<tr><th style = "text-align:right">Area: </th>'
    html += '<th><input type="text" name="area"></th></tr>'
    html += '<tr><th style = "text-align:right">Title: </th>'
    html += '<th><input type="text" name="title"></th></tr>'
    html += '<tr><th><input type="submit" value="Submit Query"></th></tr>'
    html += '</table>'
    html += '</form>'
    html += '<hr>'
    commands = {}
    rows = regdatabase(commands)
    html += '<table style= "width:100%">'
    html += '<tr>'
    html += '<th style = "font-weight: bold">ClassId</th>'
    html += '<th style = "font-weight: bold">Dept</th>'
    html += '<th style = "font-weight: bold">Num</th>'
    html += '<th style = "font-weight: bold">Area</th>'
    html += '<th style = "font-weight: bold">Title</th>'
    html += '</tr>'
    for row in rows: 
        html += '<tr>'
        html += '<th><a href="details">'+ str(row[0]) + '</a></th>' 
        html += '<th>' + str(row[1]) + '</th>'
        html += '<th>' + str(row[2]) + '</th>'
        html += '<th>' + str(row[3]) + '</th>'
        html += '<th> ' + row[4] + '</th>'  
        html += '</tr>'
    html += '</table>'
    html += '</body>'
    html += '</html>'
    response = make_response(html)
    return response
    
#-----------------------------------------------------------------------

@app.route('/details', methods=['GET'])
def details():

    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''

    html = ''
    html += '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += '<title>Details</title>'
    html += '</head>'
    html += '<body>'
    html += '<br>'
    html += '<br>'
    html += '<br>'
    html += '<br>'
    html += '<br>'
    html += '</body>'
    html += '</html>'
    
    response = make_response(html)
    return response


#-----------------------------------------------------------------------
if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)