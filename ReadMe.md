# CS 270 Final Project
## Requirements
* Linux OS: Ubuntu 14.0
* Apache2 
* MySQL Ver 14.14 
* Python 2.7.6

To install and connect MYSQL to Python,

	sudo apt-get install mysql-server
	sudo apt-get install python-mysqldb

	To access MySQL: 

	mysql -u root -p password

## Checking apache if running:

	sudo service apache2 status
	sudo service apache2 start
	sudo service apache2 restart

Download and save repo in directory /var/www

## Configuring Python CGI to Apache  

1. Enable cgi using the command: sudo a2enmod cgi
	
	optional: install python support: 
		sudo apt-get install libapache2-mod-python

2. Add the following lines to /etc/apache2/apache2.conf
	
	```
	ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
	<Directory "/var/www/cgi-bin">
	   AllowOverride None
	   Options ExecCGI
	   AddHandler cgi-script .cgi .py
	   Order allow,deny
	   Allow from all
	</Directory>

	<Directory "/var/www/cgi-bin">
	Options All
	</Directory>
	```

In the file /etc/apache2/sites-available/000-default.conf, set the default page as follows:
	
	```
	DirectoryIndex index.py
	DocumentRoot /var/www/cgi-bin
	```

3. In  /var/www/ create folder 'cgi-bin'. This is where all cgi files will be stored. 
Go to http://localhost/cgi-bin/<cgi_file.py>
