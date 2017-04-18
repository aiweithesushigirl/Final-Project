## Your name: Aiwei Wu
## The option you've chosen: 2

# Put import statements you expect to need here!
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

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_FNAME = "SI206_twitter_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

CACHE_FNAME_U = "SI206_user_cache.json"
try:
	cache_file_u = open(CACHE_FNAME_U,'r')
	cache_contents_u = cache_file_u.read()
	cache_file_u.close()
	CACHE_DICTION_U = json.loads(cache_contents_u)
except:
	CACHE_DICTION_U = {}

CACHE_FNAME_M = "SI206_movie_cache.json"
try:
	cache_file_m = open(CACHE_FNAME_M,'r')
	cache_contents_m = cache_file_m.read()
	cache_file_m.close()
	CACHE_DICTION_M = json.loads(cache_contents_m)
except:
	CACHE_DICTION_M = {}

def getWithCaching(url, params):
    full_url = requestURL(url, params)
    #print 'Test'
    if full_url in CACHE_DICTION:
        #print 'using cache'
        response_text = CACHE_DICTION[full_url]

    else:
        #print 'fetching'
        response = requests.get(full_url)
        CACHE_DICTION[full_url] = response.text
        response_text = response.text

        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()

    return response_text



class Movie(object):
    def __init__(self, movie_dict, title, director, actor_list, lang):
        self.movie = movie_dict
        self.title = title
        self.director = director
        self.actor = actor_list
        self.lang = lang

    def get_imdbRating(self):
        omdb_url = "http://www.omdbapi.com/?"
        omdb_params = {}
        imdb_rating = {}
        metascore = {}
        for movie in self.movie:
            omdb_params['t'] = a
            omdb_params['r'] = 'Json'
            omdb_data = getWithCaching(omdb_url,omdb_params)
            omdb_data = json.loads(omdb_data)
            for key1 in omdb_data.keys():
                if key1 == 'Title':
                    imdb_rating[omdb_data['Title']] = omdb_data['imdbRating']
        imdb_rating = sorted(imdb_rating.items(), key=lambda x:x[1], reverse=True)
        return imdb_rating

Class Twitter(object):
    def __init__(self, ):
        self.movie = movie_dict
        self.director = director
        self.media = media

    def get_user_tweets(self,input)
        unique_identifier = "twitter_{}".format (input)
        if unique_identifier in CACHE_DICTION:
            print('using cached data for', input)
            twitter_result = CACHE_DICTION[unique_identifier]
        else:
            print('getting data from internet for', input)
            twitter_result = api.user_timeline (id=input, count=20)
            CACHE_DICTION[unique_identifier] = twitter_result
            f = open (CACHE_FNAME, 'w')
            f.write (json.dumps (CACHE_DICTION))

        # print (len(twitter_result[0]))
        return twitter_result

    def get_user(input: object) -> object:
	    unique_identifier = "twitter_{}".format(input)
	    if unique_identifier in CACHE_DICTION_U:
		# print('using cached data for', input)
		    twitter_result = CACHE_DICTION_U[unique_identifier]
	    else:
		# print('getting data from internet for', input)
		    twitter_result = api.get_user(input)
		    CACHE_DICTION_U[unique_identifier] = twitter_result
		    f = open(CACHE_FNAME_U, 'w')
		    f.write(json.dumps(CACHE_DICTION_U))


	# print (len(twitter_result[0]))
	    return twitter_result

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Users ")

table_spec_2 = "CREATE TABLE IF NOT EXISTS "
table_spec_2 += 'Users (user_id TEXT PRIMARY KEY, '
table_spec_2 += 'screen_name TEXT, num_favs INTEGER, description TEXT)'
cur.execute(table_spec_2)

# print ("gggggg")
statement = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)'
for tweet in umich_tweets:
    input = tweet["entities"]["user_mentions"]
    # print (input)
    for i in input:
        user_id = i["id_str"]
        # print (user_id)
        users = get_user (user_id)

        cur.execute(statement, [users["id_str"], users["screen_name"], users["status"]["favorite_count"], users["description"]])
conn.commit()

cur.execute("DROP TABLE IF EXISTS Tweets ")

table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += 'Tweets (tweet_id INTEGER PRIMARY KEY, '
table_spec += 'text TEXT, user_id TEXT REFERENCES Users(user_id) ON UPDATE SET NULL, time_posted TIMESTAMP, retweets INTEGER)'
cur.execute(table_spec)


statement = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?)'
for t in umich_tweets:
    cur.execute(statement, [t["id_str"], t["text"], t["user"]["id_str"], t["created_at"],  t["retweet_count"]])
conn.commit()

query = "SELECT * FROM Users";
cur.execute(query)

result = cur.fetchall()











# Write your test cases here.

def test1(self):
    fpt = open ("SI206_twitter_cache.json", "r")
    fpt_str = fpt.read ()
    fpt.close ()
    obj = json.loads (fpt_str)
    self.assertEqual (type (obj), type ({"hi": "bye"}))

def test2(self):
    self.assertEqual (type (Movie.get_imdbRating ()), type ([]), "testing type of imdb_rating")

def test3(self):
    self.assertEqual (type (movie1.actor_movie_list ()), type ([]), "testing type of movie_list")

def test4(self):
    self.assertEqual (type (movie1.get_imdbRating ()[0]), type (()), "testing type of the element in imdb_rating")

def test5(self):
    conn = sqlite3.connect ('final_project.db')
    cur = conn.cursor ()
    cur.execute ('SELECT * FROM Tweets');
    result = cur.fetchall ()
    self.assertTrue (len (result[1]) == 6, "Testing that there are 6 columns in the Tweets table")
    conn.close ()

def test6(self):
    conn = sqlite3.connect ('final_project.db')
    cur = conn.cursor ()
    cur.execute ('SELECT * FROM Users');
    result = cur.fetchall ()
    self.assertTrue (len (result[1]) == 3, "Testing that there are 3 columns in the Users table")
    conn.close ()

def test7(self):
    conn = sqlite3.connect ('final_project.db')
    cur = conn.cursor ()
    cur.execute ('SELECT * FROM Movies');
    result = cur.fetchall ()
    self.assertTrue (len (result[1]) == 6, "Testing that there are 6 columns in the Movie table")
    conn.close ()

def test8(self):
    conn = sqlite3.connect ('final_project.db')
    cur = conn.cursor ()
    cur.execute ('SELECT user_id FROM Tweets');
    result = cur.fetchall ()
    self.assertTrue (len (result[1][0]) >= 2, "Testing that a tweet user_id value fulfills a requirement of being a Twitter user id rather than an integer, etc")
    conn.close ()


def test9(self):
    conn = sqlite3.connect ('final_project.db')
    cur = conn.cursor ()
    cur.execute ('SELECT * FROM Users');
    result = cur.fetchall ()
    self.assertTrue (len (result) >= 2, "Testing that there are at least 2 distinct users in the Users table")
    conn.close ()

unittest.main (verbosity=2)


## Remember to invoke all your tests...