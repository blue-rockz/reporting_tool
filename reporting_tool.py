import psycopg2 as ps
from psycopg2 import Error

query1 = """select * from highest_views"""

query2 = """select * from pop_auth"""

query3 = """select * from highest_errors"""


def db_connect(query):
    try:
        # connect to a DB
        connection = ps.connect("dbname=news")
        cursor = connection.cursor()

        # Execute queries
        cursor.execute(query)

        # Fetch results
        results = cursor.fetchall()

    except (Exception, ps.DatabaseError) as error:
        print("Error while accessing database NEWS", error)
    finally:
        # closing database connection & return
        if(connection):
            cursor.close()
            return results

# Returns days where error percentage was more than 1%


def error_aggregate(query):
    try:
        results = db_connect(query)
        print("\t Highest errors on a particular day\n")
        print("-" * 50)
        print("\tDate\t\tPercentage")
        print("\t{}\t   {}%".format(results[0][0], results[0][1]))
    except Exception as error:
        print("Incorrect Query")
    finally:
        if(results):
            print("<" + "-" * 17 + "End of output" + "-" * 17 + ">")

# Returns Authors popularity by views against their articles.


def popular_author(query):
    try:
        results = db_connect(query)
        print("\t\tMost popular Authors")
        print("-" * 50)
        for i in results:
            print(
                "'{}' (author) ---- {} (no of views)".format(str(i[0]), i[1]))

    except Exception as error:
        print("Incorrect Query")
    finally:
        if(results):
            print("<" + "-" * 17 + "End of output" + "-" * 17 + ">")

# Returns most viewed articles.


def title_views(query):
    try:
        results = db_connect(query)
        print("\t\tMost popular titles")
        print("-" * 50)
        for i in results:
            print("'{}' (title) ---- {} (no of views)".format(str(i[0]), i[1]))

    except Exception as error:
        print("Incorrect Query")
    finally:
        if(results):
            print("<" + "-" * 17 + "End of output" + "-" * 17 + ">")


title_views(query1)
popular_author(query2)
error_aggregate(query3)
