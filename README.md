Project Name
SQL REPORTING TOOL

TODO:
Solve 3 questions!
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

Prerequisites

* Python 3.7.3
* PostgreSQL 9.5.18
* psycopg2

SETUP
TODO: Setup process.
Usage

* Once the DB is is installed. Load the database using the following command.
  #psql -d news -f newsdata.sql

* Connect to database
  #psql news

* Format queries as required.

* Run python script
  #python reporting_tool.py

Solution 1

DB column views has been replaced and updated by removing /article.

update log set path = replace(path, '/article/', '') where path is not null;

create view highest_views as select title,count(*) as views
    from articles,log
    where articles.slug = log.path
    group by title
order by views desc limit 3;

Solution 2

View 1:
Create a view for storing authors name & slug between authors & articles table.

create view auth_name as select name,slug
    from authors,articles
 where authors.id = articles.author;

View 2:
Create a view for storing path from log & slug from articles column. 
This will be matched against view above to find the owner for the articles.

create view auth_path as select path as views
    from log,articles
where articles.slug=log.path;

View 3.
Matching above two queries to find authors and views.

 create view pop_auth as select name, count(*) as num
       from auth_name
       join auth_path on auth_name.slug = auth_path.views
       group by name
   order by num desc;

Solution 3

View 1:
Create a view to collect total errors based on date.

create view error_view as
    select date(time), count(*) as err
    from log where status = '404 NOT FOUND'
group by date order by date;

View 2:
Create a view to collect total number of views based on date.

create view overall_view as
    select date(time), count(*) as
    views from log group by date(time)
order by date(time);

View 3:
Find the avg (%) of errors on a given date.

select * from (select overall_view.date, (100 * error_view.err/overall_view.views) as percentage
from overall_view,error_view
where overall_view.date = error_view.date
order by overall_view.date) as max
where percentage >= 1 ;
