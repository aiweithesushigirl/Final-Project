# Final-Project for SI206
API Mashup OMdb and Tweepy
README 

Option2: API mash up
File name: 206_data_access.py

This program helps to identify movie lovers on Twitter by searching the director of certain movies and calculating the percentage of “true” lovers. The “true movie lover” is defined as users who have “movie”, “film” and “cinema” in his or her description.

Since the program will give the percentage of users who have some knowledge about film, it can be used to study user behavior regarding films. For example, what is the percentage of users who post film-related tweets for the trend? What is the percentage of users who contribute constructive information regarding a film?

For this program, the input has to be a list of films (not restricted in the number of films). The output is the number of films the user searches for, the number of users who mention the director of each film, number of “true movie lovers” and the percentage of “true movie lovers” over users.

Three databases are created in this program, namely Movies, Tweets and Users.

Instructions:

To run this program, the user has to input a list of movies (line 168). After running it, a csv file named movie_lover_rate will be generated in the same directory and it will contain the results.

To run this program, the user does not have to install anything. Files needed are as following:
1.	twitter_info.py

Files included:
2.	SI206_cache.json

Functions and classes
The program also includes the following functions:
def getWithCaching(url, params):
input: url of the website, parameters needed
return: response text depending on the user’s search parameters

def canonical_order(d):
input: a dictionary
return: a sorted dictionary by alphabetical orders
def requestURL(baseurl, params={}):
input: base url and the parameters:
return: the full url needed

def get_movie_info(movie):
input: name of a movie
return: a dictionary of the movie information from OMdb

def sort_lst():
No input required
Return: a sorted list of all the movie information according to the rating, from high to low

def get_director_tweets(input):
input: name of a director
return: a dictionary of the tweet related to the director from Twitter

def get_user(input):
input: name of the user
return: a dictionary of the user information from Twitter
 
The program includes the following classes:

class Movie(object):
One instance of the class represents a movie object. The constructor needs an input of a dictionary of the movie information. The Movie class has the following methods:
__str__(): it will format the movie title to recommended + movie title if the rating of the movie if above 7.5.

load_movie_data(): It will load all the movie data into the database set up in the beginning and also return a list of director names of the movies.

class Tweet(object):
One instance of the class represents a tweet about a certain director. The constructor needs an input of a dictionary of the tweet information. The Tweet class has the following methods:
load_tweet_data(): It will load all the tweet data into the database set up in the beginning. No return value for this method.

class User:
One instance of the class represents a user who is related to the tweet. The constructor needs an input of a dictionary of the user information. The User class has the following methods:
load_user_data(): It will load all the user data into the database set up in the beginning. No return value for this method.

Database creation

The database has three tables, namely Movies, Tweets and Users

Movies:
Imdb_id: the id of the film
Title: the title of the film
Director: the director of the film
Num_lang: number of languages in the film
Imdb_rating: the imdb_rating of the film

Tweets:
Tweet_id: the id of the tweet
Retweet_count: the number of retweets of the tweet
Text: the content of the tweet
Screen_name: the screen_name of the user who posts the tweet
User_id: the id of the user
Favorite_count: the number of favorites of the tweet

Users:
User_id: the id of the user
Favorite_count: the number of favorites of the user
Description: the self-description of the user
Screen_name: screen name of the user
Follower_count: the number of followers of the user

Data manipulation code
	
The program will show the percentage of “true movie lovers” for any movie, regardless of the number of movies. No matter how many movies input, a number will be generated. This can be very useful in finding the trend/taste of movie lovers. For example: we can identify the percentage of movie lovers who give comments on different genres of movies (blockbuster movies, cult movies, classics) or movie of different ratings (especially recent movies). Our prediction is that the higher the rating, the higher the percentage.

The program will also return all the movie information in a sorted manner (from high to low according to imdb_rating)

Purpose of the project

I want to study the popularity/quality of a recent movie not only by its rating but by the percentage of movie lovers who comment on the movie/director. In fact, if there is a relationship between the rating and percentage, we can establish a new rating system for movies based on its social media popularity.



