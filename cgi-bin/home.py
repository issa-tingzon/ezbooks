#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()
import MySQLdb as mdb
from template import display
from model.database import con
from passlib.hash import sha512_crypt
import os, time, sys, session, Cookie, json
import utilities

def invaidPageError():
	print "<script type='text/javascript'> \
	          alert('Error occurred. Please try again.');\
	          </script>" 

def main():
	form = cgi.FieldStorage()
	
	email = form.getvalue('email')
	genre = form.getvalue('genre')
	publisher = form.getvalue('publisher')

	#TODO: For fname, lname == None redirect to login page
	#TODO: Implement sessions using Cookies

	try:
		cur = con.cursor()

		command = "SELECT * FROM Users WHERE Email = '" + email + "'";
		cur.execute(command)
		user= cur.fetchone()

		if(genre != None):
			command = "SELECT * from ComicBooks NATURAL JOIN BookGenre WHERE Genre='" + genre + "'"
		elif (publisher != None) :
			command = "SELECT * from ComicBooks WHERE Publisher='" + publisher + "'"
		else:
			command = "SELECT * from ComicBooks"
			
		cur.execute(command)
		rows = cur.fetchall()
		titles = []
		for row in rows:
			titles.append(row)

		genre_ = [None, None]
		if (genre != None):
			command = "SELECT * FROM Genres WHERE Genre = '" + genre + "'";
			cur.execute(command)
			genre_ = cur.fetchone()

		sidebar = utilities.getSideBar(email, user[9], cur)
		print display("home.html").render(user=user,titles=titles,sidebar=sidebar,genre=genre_[0],genredesc=genre_[1],search=' ',publisher=publisher)

	except mdb.Error, e:
	    if con:
	        con.rollback()
	    print "Location: login.py?error=1"

if __name__ == '__main__':
	main()
