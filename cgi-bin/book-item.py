#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()
import MySQLdb as mdb
from template import display
from model.database import con
from passlib.hash import sha512_crypt
import os, time, sys, session, Cookie, json

def main():
	form = cgi.FieldStorage()
	
	ISBN = form.getvalue('ISBN')
	email = form.getvalue('email')
	try:
		cur = con.cursor()
		
		command = "SELECT * from Books WHERE ISBN='" + ISBN + "'"
		
		cur.execute(command)
		book = cur.fetchone()

		command = "SELECT AuthorName, AuthorId from Books NATURAL JOIN BookAuthor NATURAL JOIN Authors WHERE ISBN ='" + book[0] + "'"
		cur.execute(command)
		authors = cur.fetchall()

		command = "SELECT * FROM Users WHERE Email = '" + email + "'";
		cur.execute(command)
		user = cur.fetchone()

		command = "SELECT Genre from Books NATURAL JOIN Genres WHERE ISBN ='" + book[0] + "'"
		cur.execute(command)
		genres = cur.fetchall()
		
		print display("book-item.html").render(book=book,user=user,authors=authors,genres=genres)
		print genres

	except mdb.Error, e:
	    if con:
	        con.rollback()
	    print "Location: login.py?error=1"

if __name__ == '__main__':
	main()