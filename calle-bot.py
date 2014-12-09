#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, re, string, random
from tweepy import Cursor

#Constants
CONSUMER_KEY = 'cfXIieakwAlNGRq1x60oVb05c'
CONSUMER_SECRET = 'sIzLofT62RNpZEKDcc6cRwZFtkiiyngKzXBgyNxutfE8LIWszm'
ACCESS_KEY = '2648673991-BJyAcIKs9XJp9CNjDWsnlEYSGpb0Yeno2LHdzss'
ACCESS_SECRET = 'p4xtAW31nvVtLZ1quvO5pjoR9R09MG3StoZDcfwQagnd2'
NUMBER_OF_TWEETS = 300
fake_tweets = ["I don't even know", "Dark lord cthulhu", "I love moderaterna, they are awesome", "http://wat.com", "lol, why are we doing this"]
#setup stuff
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def write_test_file(tweets):
	with open('test_tweets', 'r+a') as f:
		for tweet in tweets:
			f.write(tweet.strip('\n').encode('utf8'))
			f.write('\n')

def get_filtered_tweets():
	tweets = []
	for update in Cursor(api.user_timeline, id='carlbildt').items():
		if len(tweets) == NUMBER_OF_TWEETS:
			break
		tweet = update.text
		if not tweet.startswith('@') and not tweet.startswith('RT'):
			tweets.append(tweet)
	return tweets

def get_words(tweets):
	all_words = []
	finder = re.compile(r'[\S]+', re.UNICODE)
	for tweet in tweets:
		words = finder.findall(tweet)
		all_words.append(words)
	return all_words

def generate_test_file_from_tweets():
	tweets = get_filtered_tweets()
	write_test_file(tweets)

def get_file_tweets():
	with open('test_tweets', 'r') as f:
		tweets = f.readlines()
	return tweets

def get_file_wordlists():
	tweets = get_file_tweets()
	worldlists = get_words(tweets)
	return worldlists

def get_twitter_wordlists():
	tweets = get_filtered_tweets()
	worldlists = get_words(tweets)
	return worldlists

if __name__ == '__main__':
	worldlists = get_file_wordlists()
	print worldlists
