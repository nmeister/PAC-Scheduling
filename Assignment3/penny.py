#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv, exit
from common import getHeader, getFooter
from database import Database
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
    html += '<title>Penny.com</title>'
    html += '</head>'
    html += '<body>'
    html += getHeader()
    html += '<br>'
    html += 'Click here to <a href="searchform">begin</a>.<br>'
    html += '<br>'
    html += getFooter()
    html += '</body>'
    html += '</html>'
    
    response = make_response(html)
    return response
    
#-----------------------------------------------------------------------

@app.route('/searchform', methods=['GET'])
def searchForm():

    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''
    
    prevAuthor = request.cookies.get('prevAuthor')
    if prevAuthor is None:
        prevAuthor = '(None)'
    
    html = ''
    html += '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += '<title>Penny.com</title>'
    html += '</head>'
    html += '<body>'
    html += getHeader()
    html += '<h1>Author Search</h1>'
    html += '<form action="searchresults" method="get">'
    html += 'Please enter an author name:'
    html += '<input type="text" name="author">'
    html += '<input type="submit" value="Go">'
    html += '</form>'
    html += '<br>'
    
    if errorMsg:
       html += '<strong>' + errorMsg + '</strong>'
       
    html += '<br>'
    html += '<br>'
    html += '<strong>Previous author search:</strong> '
    html += prevAuthor 
    html += '<br>'
    html += '<br>'
    html += getFooter()
    html += '</body>'
    html += '</html>'
    
    response = make_response(html)
    return response
    
#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def searchResults():
    
    author = request.args.get('author')
    if (author is None) or (author.strip() == ''):
        errorMsg = 'Please type an author name.'
        return redirect(url_for('searchForm', errorMsg=errorMsg))
  
    database = Database()
    database.connect()
    books = database.search(author)
    database.disconnect()
    
    html = ''
    html += '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += '<title>Penny.com</title>'
    html += '</head>'
    html += '<body>'
    html += getHeader()
    html += '<h1>Author Search Results</h1>'
    html += '<h2>Books by ' + author + ':</h2>'

    if len(books) == 0:
        html += '(None)<br>'
    else:
        for book in books:
            html += book.getAuthor() + ', ' + book.getTitle() + \
            ' ($' + str(book.getPrice()) + ')<br>'

    html += '<br>'
    html += '<br>'
    html += 'Click here to do another '
    html += '<a href="searchform">author search</a>.'
    html += '<br>'
    html += '<br>'
    html += '<br>'
    html += '<br>'
    html += getFooter()
    html += '</body>'
    html += '</html>' 

    response = make_response(html)
    response.set_cookie('prevAuthor', author)
    return response
     
#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
