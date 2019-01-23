#!/usr/bin/env python3
import psycopg2

#The most popular three articles of all time
query_articles = ("""create view pop1_articles as select title,
                    count(title) as views from articles,
                    log where log.path = concat('/article/',articles.slug)
                    group by title order by views desc limit 3""")
#The most popular three article authors of all time
query_authors = ("""create view pop1_authors as select name,
                    count(name) as views from articles,authors,
                    log where log.path = concat('/article/',articles.slug)
                    and articles.author=authors.id group by name order by
                    views desc limit 3""")
#On which days did more than 1% of requests lead to errors
query_errors = ("""create view pop_errors as select date(time),
                    round(100.0*sum(case log.status when '200 OK'
                    then 0 else 1 end)/count(log.status),2)as percent_error
                    from log group by date(time) order by percent_error""")

#def for popular articles
def popular_articles_inDB(query_articles):
    db = psycopg2.connect(dbname="news")
    cur = db.cursor()
    # cur.execute(query_articles)
    cur.execute("select* from pop1_articles")
    db.commit()
    art_result = cur.fetchall()
    db.close()
    for i in art_result:
        print(str(i[0])+"  --"+str(i[1])+"views")
    return

#def for popular articles authors
def popular_authors_inDB(query_authors):
    db = psycopg2.connect(dbname="news")
    cur = db.cursor()
    # cur.execute(query_authors)
    cur.execute("select* from pop1_authors")
    db.commit()
    auth_result = cur.fetchall()
    db.close()
    for i in auth_result:
        print(str(i[0])+" \t--"+str(i[1])+"views")
    return

#def for errors more than 1%
def error_percent_inDB(query_errors):
    db = psycopg2.connect(dbname="news")
    cur = db.cursor()
    # cur.execute(query_errors)
    cur.execute("""select date,percent_error
                    from pop_errors where percent_error > 1.0""")
    db.commit()
    err_result = cur.fetchall()
    db.close()
    for i in err_result:
        print(str(i[0])+"\t --"+str(i[1])+"% errors")
    return


if __name__ == "__main__":
    print("1.What are the most popular three articles of all time?")
    popular_articles_inDB(query_articles)
    print("2.Who are the most popular article authors of all time?")
    popular_authors_inDB(query_authors)
    print("3.On which days did more than 1% of requests lead to errors?")
    error_percent_inDB(query_errors)
