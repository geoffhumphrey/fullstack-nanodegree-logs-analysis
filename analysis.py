#!/usr/bin/env python

# Import psycopg2 - a python postgresql library
import psycopg2


# Import datetime.date module - allows for customized date display
from datetime import date


# Store the database name in a variable
db_name = 'news'


def query_db(query):
    """
    Connect to the database and execute the sql query
    Returns rows as a list of tuples
    """

    try:
        connect = psycopg2.connect('dbname=' + db_name)
        cur = connect.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        connect.close()
        return rows

    except psycopg2.Error as err:
        print("Unable to connect to the database")
        print(err.pgerror)
        print(err.diag.message_detail)
        sys.exit(1)

def top_three_articles():

    """
    Query DB to find top three articles of all time and include
    the page view counts for each
    """

    query = """
        SELECT articles.title, COUNT(*) as views
        FROM articles, log
        WHERE log.path = concat('/article/', articles.slug)
        GROUP BY articles.title
        ORDER BY views DESC LIMIT 3;
        """
    execute_query = query_db(query)

    print('--- What are the most popular three articles of all time? ---')

    for articles in execute_query:
        article_views = "{:,}".format(articles[1])
        print('"' + articles[0] + '" -- ' + str(article_views) + ' page views')

    print(' \n')


def top_three_authors():

    """
    Query the DB to find the most popular article authors and
    return the number of article views for each in descending
    order
    """

    query = """
        SELECT authors.name, COUNT(*) as views
        FROM authors, articles, log
        WHERE authors.id = articles.author
        AND log.path = concat('/article/', articles.slug)
        GROUP BY authors.name
        ORDER BY views DESC;
        """
    execute_query = query_db(query)

    print('--- Who are the most popular article authors of all time? ---')

    for author in execute_query:
        author_views = "{:,}".format(author[1])
        print (author[0] + ' -- ' + str(author_views) + ' page views')

    print(' \n')


def days_with_errors():

    """
    Create two views to house results prior to executing final query
    to get the desired outcome
    """

    query = """
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

        SELECT total_access.date,
        ROUND(((100.0*error_log.errors)/total_access.total_req),2)
        AS percent
        FROM total_access, error_log
        WHERE total_access.date = error_log.date
        AND (((100.0*error_log.errors)/total_access.total_req) > 1.0)
        ORDER BY percent;
        """
    execute_query = query_db(query)

    print('--- On which days did more than one percent'),
    print('of requests lead to errors? ---')

    for error in execute_query:
        print (error[0].strftime('%A, %B %e, %Y')),
        print ('-- ' + str(error[1]) + '%' + ' errors')

    print(' \n')


if __name__ == '__main__':
    print(" \n")
    print("-----------> Logs Analysis Results <-----------")
    print(" \n")
    top_three_articles()
    top_three_authors()
    days_with_errors()
