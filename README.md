## Full Stack Nanodegree - Logs Analysis Project

### Project Task
This project's task is to build a program in Python, utilizing the psycopg2 module, that queries a rather large PostgreSQL database containing a fictional news website's log data. The analysis should answer three questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Each of the questions should be "answered" using a single SQL query, using SQL views if desired.

### Install a Virtual Machine
A Linux-based virtual machine (VM) is required to run this program. For this project, the VM is built and managed with [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). Download and install both on your computer.

### Download Configuration Files and Database
Once you have installed the VM, download or clone Udacity's [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository and the [database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Download or clone [this](https://github.com/geoffhumphrey/fullstack-nanodegree-logs-analysis) project, unzip, and copy into the vagrant directory. Finally, unzip the database and place the newsdata.sql into the newly created /vagrant/logs_analysis directory.

### Run the Program
Start the virtual machine by opening your terminal, changing directory into the vagrant directory you set up previously. Then:
1. Run ```vagrant up``` to build the VM - this may take several minutes to do the first time. 
2. Run ```vagrant ssh``` to connect. 
3. Change directory (cd) into the vagrant/logs_analysis directory by running the command ```cd /vagrant/logs_analysis```.
4. Run the program by typing the command ```python analysis.py```.

The results of the should print in the terminal window.

### Expected Output
When the program has run, the following output should be printed in the terminal window:
```
-----------> Logs Analysis Results <-----------

--- Question: What are the most popular three articles of all time? ---
"Candidate is jerk, alleges rival" -- 338,647 page views
"Bears love berries, alleges bear" -- 253,801 page views
"Bad things gone, say good people" -- 170,098 page views

--- Question: Who are the most popular article authors of all time? ---
Ursula La Multa -- 507,594 page views
Rudolf von Treppenwitz -- 423,457 page views
Anonymous Contributor -- 170,098 page views
Markoff Chaney -- 84,557 page views

--- Question: On which days did more than one percent of requests lead to errors? ---
Sunday, July 17, 2016 -- 2.26% errors

```

### DB Structure and SQL Queries Used
The supplied database has three tables, each with associated columns:
- articles
	- author
	- title
	- slug
	- lead
	- body
	- time
	- id
- authors
	- name
	- bio
	- id
- logs
	- ip
	- method
	- status
	- time
	- id

The following SQL queries were used to answer each question in the project requirements (note the creation/replacement of two views used to "answer" the third question).

*What are the most popular three articles of all time?*
```
SELECT articles.title, COUNT(*) as views
	FROM articles, log
	WHERE log.path = concat('/article/', articles.slug)
	GROUP BY articles.title
	ORDER BY views DESC LIMIT 3;
```

*Who are the most popular article authors of all time?*
```
SELECT authors.name, COUNT(*) as views
	FROM authors, articles, log
	WHERE authors.id = articles.author
	AND log.path = concat('/article/', articles.slug)
	GROUP BY authors.name
	ORDER BY views DESC;
```

*On which days did more than 1% of requests lead to errors?*
```
CREATE OR REPLACE VIEW total_access AS
	SELECT time::date as date, COUNT(*) as total_req
	FROM log
	GROUP BY date
	ORDER BY date;

CREATE OR REPLACE VIEW error_log AS
	SELECT time::date as date, COUNT(*) as errors
	FROM log
	WHERE status LIKE '%404%'
	GROUP BY date
	ORDER BY date;

SELECT total_access.date, ROUND(((100.0*error_log.errors)/total_access.total_req),2) AS percent
	FROM total_access, error_log
	WHERE total_access.date = error_log.date
	AND (((100.0*error_log.errors)/total_access.total_req) > 1.0)
	ORDER BY percent;
```