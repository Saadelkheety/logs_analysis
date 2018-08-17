# Logs analysis
this app is designed to analysis the data of a website to answer a question about
different articles views which they are:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## run the app
you just need to run the command:
```
$ python3 logs_analysis.py
```
or
```
$ /.logs_analysis.py
```

## the idea of the code
the app consists of three postgresql quiries each answers a question

### What are the most popular three articles of all time?
by joinig the articles and log tables on slug and path columns as slug is a part from path.

### Who are the most popular article authors of all time?
Count the visits of every article and joining it with author table.

### On which days did more than 1% of requests lead to errors?
find the number of all requests on everyday and find the number of all requests errors and 
compare them.