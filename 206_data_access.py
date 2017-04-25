###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project.
# You should specify variable names and processes to use. For example,
# "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts,
# where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you,
# as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources,
# and an invocation of each of those functions to show that they work
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains,
# such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import requests
import json
import pickle
import webbrowser
import unittest
import csv
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info
from pprint import pprint

# Begin filling in instructions....
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## CACHE THE DATA FROM THE INTERNET INTO A CACHE FILE

CACHE_FNAME = "SI206_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

## SET UP DATABASE SO THAT WE CAN APPEND DATA TO THE TABLE LATER. THE DATABASE INCLUDES THREE TABLES, NAMELY MOVIES, TWEETS AND USERS

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Movies ")

table_spec_1 = "CREATE TABLE IF NOT EXISTS "
table_spec_1 += 'Movies (imdb_id TEXT PRIMARY KEY, '
table_spec_1 += 'title TEXT, director TEXT, num_lang INTEGER, imdb_rating TEXT, top_billed_actor TEXT)'
cur.execute(table_spec_1)


cur.execute("DROP TABLE IF EXISTS Tweets ")

table_spec_2 = "CREATE TABLE IF NOT EXISTS "
table_spec_2 += 'Tweets (tweet_id TEXT PRIMARY KEY, '
table_spec_2 += 'retweet_count INTEGER, text TEXT, screen_name TEXT, user_id TEXT, favorite_count INTEGER)'
cur.execute(table_spec_2)


cur.execute("DROP TABLE IF EXISTS Users ")

table_spec_3 = "CREATE TABLE IF NOT EXISTS "
table_spec_3 += 'Users (user_id TEXT REFERENCES Tweets(user_id) ON UPDATE SET NULL, '
table_spec_3 += 'favourites_count INTEGER, description TEXT, screen_name TEXT REFERENCES Tweets(screen_name) ON UPDATE SET NULL, followers_count INTEGER)'
cur.execute(table_spec_3)

## FUNCTIONS SET UP TO CACHE THE DATA FROM OMDB
def getWithCaching(url, params):
    full_url = requestURL(url, params)
    # print 'Test'
    if full_url in CACHE_DICTION:
        # print 'using cache'
        response_text = CACHE_DICTION[full_url]

    else:
        # print 'fetching'
        response = requests.get(full_url)
        CACHE_DICTION[full_url] = response.text
        response_text = response.text

        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()

    return response_text


def canonical_order(d):
    alphabetized_keys = sorted(d.keys())
    res = []
    for k in alphabetized_keys:
        res.append((k, d[k]))
    return res

def requestURL(baseurl, params={}):
    req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
    prepped = req.prepare()
    return prepped.url

## Make request to OMdb to get information of a movie and return a dictionary including the information

def get_movie_info(movie):
    omdb_url = "http://www.omdbapi.com/?"
    omdb_params = {}


    omdb_params['t'] = movie
    omdb_params['r'] = 'Json'
    omdb_data = getWithCaching(omdb_url, omdb_params)
    omdb_data = json.loads(omdb_data)

    return omdb_data

## A Movies class that saves the datas of a movie

class Movie(object):

## Constructor, SAVE THE DATA INTO DIFFERENT INSTANCE VARIABLES

    def __init__(self, movie_dict):
        self.movie = movie_dict
        self.id = movie_dict["imdbID"]
        self.title = movie_dict["Title"]
        self.director = movie_dict["Director"]
        self.num_lang = len(movie_dict["Language"].split(","))
        self.rating = movie_dict["imdbRating"]
        self.top_billed_actor = movie_dict["Actors"].split(",")[0]

## The load_movie_data() method will load all the movie date into THE DATABASE SET UP IN THE BEGINNING

    def load_table_data(self, conn, cur):
        statement = 'INSERT OR IGNORE INTO Movies VALUES (?, ?, ?, ?, ?, ?)'
        cur.execute(statement, [self.id, self.title, self.director, self.num_lang, self.rating, self.top_billed_actor])
        conn.commit()

## The method will also return a list of director names of the movies

        query = "SELECT director FROM Movies;"
        cur.execute(query)
        names_lst = []
        for name in cur:
            names_lst.append(name[0])
        return names_lst

## A LIST OF MOVIE NAMES TO BE USED

movie_lst = ["Godfather", "Logan", "harry potter", "fast and furious", "inherent vice", "get out", "raw", "forrest gump", "moana", "frozen"]
movie_info_lst = []
movie_ob_lst = []

## Invoke the get_movie_function() and save the movie dictionaries to a list
for movie in movie_lst:
    movie_info_lst.append(get_movie_info(movie))

# print (movie_info_lst)

## Pass in the list of dictionaries to create a list of Movie objects

for movie_dict in movie_info_lst:
    movie_ob_lst.append(Movie(movie_dict))
# print (movie_ob_lst)
director_lst = []

## User the movie objects to call method load_table_data() to load the data into the database
for movie in movie_ob_lst:
    print (movie.load_table_data(conn, cur))
    director_lst.append(movie.load_table_data(conn, cur))

## Make requests to Tweepy to get tweet information of the directors, cache every request. The function will return a dictionary

def get_director_tweets(input: object) -> object:
	unique_identifier = "twitter_{}".format(input)
	if unique_identifier in CACHE_DICTION:
		print('using cached data for', input)
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting data from internet for', input)
		twitter_results = api.search(q=input,rpp=200,lang="en")
		CACHE_DICTION[unique_identifier] = twitter_results
		f = open(CACHE_FNAME,'w')
		f.write(json.dumps(CACHE_DICTION))
	return twitter_results


## CREATE A CLASS TWEET TO SAVE THE TWEET INFORMATION
class Tweet(object):
## CONSTRCTOR
    def __init__(self, tweet_dict):
        self.tweet_dict = tweet_dict
        self.director = director_lst
## LOAD THE TWEETS ABOUT THE DIRECTOR INTO A DATABASE
    def load_tweet_data(self):

        statement = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
        for item in self.tweet_dict["statuses"]:
            cur.execute(statement, [item["id_str"], item["retweet_count"], item["text"], item["user"]["screen_name"], item["user"]["id_str"], item["favorite_count"]])
        conn.commit()




## Invoke the get_director_tweet() and save the tweet dictionaries to a list


## Pass in the list of dictionaries to create a list of Tweet objects



good_director =[]

query = "SELECT director FROM Movies WHERE imdb_rating >= 7.5;"

# query = "SELECT director FROM Movies ;"
cur.execute(query)
for row in cur:
    good_director.append(row[0])
print (good_director)
object_lst = []
for director in good_director:
    object = Tweet(get_director_tweets(director))
    object_lst.append(object)
for object in object_lst:
    object.load_tweet_data()

# Make invocations to your Twitter functions.
# Use your Twitter search function to search for (your choice): either each of the directors of those three movies, or one star actor
# in each of those three movies, or each of the titles of those three movies.
# NOTE: It may be useful to have a class Tweet for this reason, because you can make a list of instances of the Tweet class each time you get data,
#  and then concatenate (squish) the lists together…
# Save either a list of instances of class Tweet, or a list of Tweet dictionaries, or a list of Tweet info tuples, in a variable to use later.
# Then, use your function to access data about a Twitter user to get information about each of the Users in the "neighborhood",
# as it's called in social network studies -- every user who posted any of the tweets you retrieved and every user who is mentioned in them.
# It may be useful to have a class TwitterUser for this reason, as you can then create lists of user instances instead of lists of dictionaries!
# But you can manage the data in dictionaries as well, if you like.
# Save either a resulting list of instances of your class TwitterUser or a list of User-representative dictionaries in a variable.
# Make sure your code accesses the whole neighborhood -- every tweet poster and



user_lst =[]
query = "SELECT user_id FROM Tweets WHERE retweet_count >= 8;"
cur.execute(query)
for row in cur:
    user_lst.append(row[0])
print (user_lst)

def get_user(input: object) -> object:
	unique_identifier = "twitter_{}".format(input)
	if unique_identifier in CACHE_DICTION:
		# print('using cached data for', input)
		twitter_result = CACHE_DICTION[unique_identifier]
	else:
		# print('getting data from internet for', input)
		twitter_result = api.get_user(input)
		CACHE_DICTION[unique_identifier] = twitter_result
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))


	# print (len(twitter_result[0]))
	return twitter_result

user_info_lst = []
for user in user_lst:
    user_info_lst.append(get_user(user))
print (user_info_lst)




class User:

## CONSTRCTOR
    def __init__(self, user_dict):
        self.user_dict = user_dict


## LOAD THE TWEETS ABOUT THE DIRECTOR INTO A DATABASE
    def load_user_data(self):

        statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?, ?)'
        cur.execute(statement, [self.user_dict["id_str"], self.user_dict["favourites_count"], self.user_dict["description"], self.user_dict["screen_name"], self.user_dict["followers_count"]])
        conn.commit()

for user in user_info_lst:
    print (user)
    item = User(user)
    item.load_user_data()

## CREATE A TUPLE OF THE SCREEN NAME WHOSE TWEETS HAVE BEEN RETWEETED MORE THAN 8 TIMES OF THE USER AND HIS/HER DESCRIPTION
joined_result =[]
query = "SELECT Tweets.screen_name, Users.description FROM Tweets INNER JOIN Users on Tweets.user_id = Users.user_id WHERE retweet_count >=8";
cur.execute(query)
for row in cur:
    if row:
        joined_result.append(row)
print (joined_result)

## CREATE A WORDLIST OF KEYWORDS "MOVIE" "FILM" AND CHECK WHETHER ANY OF THE DESCRIPTIONS CONTAIN EITHER OF THOSE TWO WORDS

word_lst = ["movie", "film"]
movie_lover_lst =[]
for tup in joined_result:
    if any(word in tup[1] for word in word_lst):
        movie_lover_lst.append(tup[0])

cur.execute('SELECT * FROM Users');
result = cur.fetchall()
print (len(result))
print (movie_lover_lst)
rate = ((len(movie_lover_lst)/len(result)*100))

fname = open("movie_lover_rate.csv", 'w')
fname.write("num_movies, num_users, rate")
# for a in post_insts:
#     emo_scores = a.emo_score()
#     comment_counts = len(a.comments)
#     like_counts = len(a.likes)
#     data = (emo_scores, comment_counts, like_counts)
#     fname.write("{},{},{}".format(*data)+"\n")


            # Put your tests here, with any edits you now need from when you turned them in with your project plan.
class Tests(unittest.TestCase):
    def test1(self):
        fpt = open ("SI206_cache.json", "r")
        fpt_str = fpt.read ()
        fpt.close ()
        obj = json.loads (fpt_str)
        self.assertEqual (type (obj), type ({"hi": "bye"}))

    def test2(self):
        for movie in movie_ob_lst:
            self.assertEqual(type (movie.load_table_data(conn, cur)), type ([]), "testing the method load_movie_data() returns a list")

    # def test3(self):
    #     self.assertEqual(len(movie_lst), 6)


    def test4(self):
        conn = sqlite3.connect ('final_project.db')
        cur = conn.cursor ()
        cur.execute ('SELECT top_billed_actor FROM Movies');
        result = cur.fetchall ()
        self.assertTrue (type(result), (""))
        conn.close ()

    def test5(self):
        conn = sqlite3.connect ('final_project.db')
        cur = conn.cursor ()
        cur.execute ('SELECT * FROM Movies');
        result = cur.fetchall ()
        self.assertTrue (len (result[1]) == 6, "Testing that there are 3 columns in the Movies table")
        conn.close ()

    def test6(self):
        conn = sqlite3.connect ('final_project.db')
        cur = conn.cursor ()
        cur.execute ('SELECT * FROM Tweets');
        result = cur.fetchall ()
        self.assertTrue (len (result[1]) == 6, "Testing that there are 6 columns in the Tweets table")
        conn.close ()

    def test7(self):
        conn = sqlite3.connect ('final_project.db')
        cur = conn.cursor ()
        cur.execute ('SELECT user_id FROM Tweets');
        result = cur.fetchall ()
        self.assertTrue (len (result[1][0]) >= 2, "Testing that a tweet user_id value fulfills a requirement of being a Twitter user id rather than an integer, etc")
        conn.close ()


    def test8(self):
        conn = sqlite3.connect ('final_project.db')
        cur = conn.cursor ()
        cur.execute ('SELECT director FROM Movies');
        result = cur.fetchall ()
        self.assertTrue (type(result), type(""))
        conn.close ()

    def test9(self):
        conn = sqlite3.connect ('final_project.db')
        cur = conn.cursor ()
        cur.execute ('SELECT * FROM Users');
        result = cur.fetchall ()
        self.assertTrue (len(result[1])== 5, "Testing that there are 5 columns in the Users table")
        conn.close ()

    def test10(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Movies');
        result = cur.fetchall()
        self.assertTrue(len(result) == len(movie_lst))
        conn.close()
unittest.main (verbosity=2)


            # Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
