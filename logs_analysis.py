#!/usr/bin/python3
import psycopg2
from calendar import month_name

# file object to write on it
fout = open('output.txt', 'w')
# Connect to the news database
conn = psycopg2.connect("dbname=news")
# Open a cursor to perform database operations
cur = conn.cursor()
# the most popular three articles of all time
# joining the articles and log tables using path, slug and counting title
cur.execute("""
SELECT title, count(*) AS visits
FROM articles JOIN log
ON log.path = '/article/' || articles.slug
GROUP BY title
ORDER BY visits DESC
LIMIT 3
;""")
popular_article = cur.fetchall()
# write on the file
fout.write("the most popular three articles of all time:\n")
for title, views in popular_article:
    fout.write("\"{}\" __ {} views \n".format(title, views))
# most popular article authors
# Count the visits of every article
# Count the visits of every article and mention the author id
# Sum the views for every author
cur.execute("""
-- Sum the views for every author
SELECT name, sum(visits) as views
FROM
-- Count the visits of every article and mention the author id
(SELECT articles.author, popular_article.visits
FROM
-- Count the visits of every article
(SELECT title, count(*) AS visits
FROM articles LEFT JOIN log
ON log.path = '/article/' || articles.slug
GROUP BY title) as popular_article
-----
JOIN articles ON articles.title = popular_article.title) as individual_authors
JOIN authors
ON authors.id = individual_authors.author
GROUP BY name
ORDER BY views DESC
;""")

popular_authors = cur.fetchall()
# write in the file
fout.write("\n\nthe most popular article authors of all time:\n")
for author, views in popular_authors:
    fout.write("\"{}\" __ {} views \n".format(author, views))
# which days did more than 1% of requests lead to errors?
cur.execute("""
-- compare the requests and the errors
SELECT logs_t.logs_num, error_t.error_num, error_t.year,
error_t.month, error_t.day
FROM
-- find the number of all requests
(SELECT COUNT(status) AS logs_num,
    EXTRACT(YEAR FROM time) AS year,
    EXTRACT(MONTH FROM time) AS month,
    EXTRACT(DAY FROM time) AS day
FROM log
GROUP BY year, month, day) AS logs_t
JOIN
-- find the number of all requests errors
(SELECT COUNT(status) AS error_num,
    EXTRACT(YEAR FROM time) AS year,
    EXTRACT(MONTH FROM time) AS month,
    EXTRACT(DAY FROM time) AS day
FROM log
WHERE log.status LIKE '4%' OR log.status LIKE '5%'
GROUP BY year, month, day
ORDER BY error_num DESC) as error_t
ON (logs_t.year = error_t.year AND logs_t.month = error_t.month
AND logs_t.day = error_t.day)
WHERE logs_num <= (100 * error_num)
;
""")
error_day = cur.fetchall()
# write in the file
fout.write("\nOn which days did more than 1% of requests lead to errors?\n")
for logs, error, year, month, day in error_day:
    fout.write("on {}-{}-{} __ {}%\n".format(
                                            month_name[int(month)],
                                            int(day), int(year),
                                            (error*100/logs)))
# Close communication with the database
cur.close()
conn.close()
