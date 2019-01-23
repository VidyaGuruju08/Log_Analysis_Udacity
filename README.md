# Log_Analysis_Udacity

## A. Softwares required by the log analysis project: ##
	1. Python
	2. psycopg2
	3. PostgreSQL 
 A vagrant managed virtual machine(VM) is used to run the log analysis project which includes the above softwares. This will need Vagrant and VirtualBox software installed on your system.

## B. Setup Project and Installation: ##
	1. Install Vagrant and VirtualBox
	2. Download or Clone fullstack-nanodegree-vm repository.
	3. Copy the newsdata.sql file and content of this current repository, by downloading.
	

## C. Launching the Virtual Machine: ##
	1. To run the Vagrant VM in Vagrant sub-directory in the downloaded fullstack-nanodegree-vm repository using command:
 		 *$ vagrant up
	2. Then Log into VM using command:
  		*$ vagrant ssh
	3. Change directory to /vagrant and check for the files using ls.
	4. Load the data from the database using the command:
  		*$ psql -d news -f newsdata.sql
	    (i )  use \c to connect to database="news"
	    (ii)  use \dt to see the tables in database
	    (iii) use \dv to see the views in database
	    (iv) use \q to quit the database

## D. The database includes three tables: ##
	1. The Authors table
	2. The Articles table
	3. The Log table

## E. PSQL Command Used To create views on these tables: ##
	1.The authors table includes information about the authors of articles.
	Create view pop1_articles using:
	create view pop1_articles as select title,count(title) as views from articles,log where log.path = concat('/article/',articles.slug) group by title order by views desc limit 3;

	2.The articles table includes the articles themselves.
	Create view pop1_authors using:
	create view pop1_authors as select name,count(name) as views from articles,authors,log where log.path = concat('/article/',articles.slug) and articles.author=authors.id group by name order by views desc limit 3;

	3.The log table includes one entry for each time a user has accessed the site.
	Create view pop_errors using:
	create view pop_errors as select date(time),round(100.0*sum(case log.status when '200 OK' then 0 else 1 end)/count(log.status),2) as percent_error from log group by date(time) order by percent_error;

## F. Running the queries: ##
	1. From the vagrant directory inside the virtual machine,run newsdata.py using:
		  *$ python newsdata.py
## G. Calculating Results:(Output) ##
	1.TOP THREE ARTICLES BY PAGE VIEWS:
    		 Candidate is jerk, alleges rival -- 338647 views
   		 Bears love berries, alleges bear -- 253801 views
    		 Bad things gone, say good people -- 170098 views
	2. TOP THREE AUTHORS BY VIEWS:	
		Ursula La Multa        -- 507594 views
    		Rudolf von Treppenwitz -- 423457 views
    		Anonymous Contributor  -- 170098 views
	3. DAYS WITH MORE THAN 1% ERRORS:
		2016-07-17  --2.26% errors
