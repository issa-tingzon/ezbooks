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
		
		books = []
		command = "SELECT * from ComicBooks WHERE ISBN='" + ISBN + "'"
		cur.execute(command)
		book = cur.fetchone()
		for i in range(len(book)):
			books.append(book[i])

		formats = []
		command = "SELECT Format from BookFormat WHERE ISBN='" + ISBN + "'"
		cur.execute(command)
		format = cur.fetchall()
		for i in range(len(format)):
			formats.append(format[i][0])
		books.append(formats)

		awards = []
		command = "SELECT Award from LiteraryAwards WHERE ISBN='" + ISBN + "'"
		cur.execute(command)
		award = cur.fetchall()
		for i in range(len(award)):
			awards.append(award[i][0])
		books.append(awards)

		command = "SELECT WriterName, WriterId from ComicBooks NATURAL JOIN BookWriter NATURAL JOIN Writers WHERE ISBN ='" + book[0] + "'"
		cur.execute(command)
		writers = cur.fetchall()

		command = "SELECT IllustratorName, IllustratorId from ComicBooks NATURAL JOIN BookIllustrator NATURAL JOIN Illustrators WHERE ISBN ='" + book[0] + "'"
		cur.execute(command)
		illustrators= cur.fetchall()

		command = "SELECT * FROM Users WHERE Email = '" + email + "'";
		cur.execute(command)
		user = cur.fetchone()

		command = "SELECT Genre from ComicBooks NATURAL JOIN BookGenre WHERE ISBN ='" + book[0] + "'"
		cur.execute(command)
		genres = cur.fetchall()

		book_exists = False
		command = "SELECT * FROM UserCart WHERE Email=%s AND ISBN=%s"
		cur = con.cursor()
		cur.execute(command, (email, ISBN))
		book_ = cur.fetchone()
		if (book_ != None):
			book_exists = True
		
		print display("comic-book-item.html").render(book=books,user=user,writers=writers,illustrators=illustrators,genres=genres,book_exists=book_exists)
		
	except mdb.Error, e:
	    if con:
	        con.rollback()
	    print "Location: login.py?error=1"

if __name__ == '__main__':
	main()