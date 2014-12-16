#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, re, string, random
from tweepy import Cursor

#Constants
CONSUMER_KEY = 'cfXIieakwAlNGRq1x60oVb05c'
CONSUMER_SECRET = 'sIzLofT62RNpZEKDcc6cRwZFtkiiyngKzXBgyNxutfE8LIWszm'
ACCESS_KEY = '2648673991-BJyAcIKs9XJp9CNjDWsnlEYSGpb0Yeno2LHdzss'
ACCESS_SECRET = 'p4xtAW31nvVtLZ1quvO5pjoR9R09MG3StoZDcfwQagnd2'
NUMBER_OF_TWEETS = 2000
TWEET_FILE = 'test_tweets_2'
fake_tweets = ["I don't even know", "Dark lord cthulhu", "I love moderaterna, they are awesome", "http://wat.com", "lol, why are we doing this"]
#setup stuff
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def write_test_file(tweets):
	with open(TWEET_FILE, 'w') as f:
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
	print len (tweets)
	write_test_file(tweets)

def get_file_tweets():
	with open(TWEET_FILE, 'r') as f:
		tweets = f.readlines()
	return tweets

def get_file_wordlists():
	tweets = get_file_tweets()
	wordlists = get_words(tweets)
	return wordlists

def get_twitter_wordlists():
	tweets = get_filtered_tweets()
	wordlists = get_words(tweets)
	return wordlists

def modify_statuses(wordLists):
	comp = re.compile("[\"\']", re.UNICODE)
	res_list = []
	for tweet_list in wordLists:
		this_list = []
		for word in tweet_list:
			if word.startswith('http'):
				this_list.append(word)
			else:
				this_list.append(comp.sub('', word))
		res_list.append(this_list)
	return res_list

def contains_special_character(ngram):
	comp = re.compile("[\.!?,;:](?!\d,;)", re.UNICODE)
	for word in ngram[0]:
		if re.search(comp, word):
			return True
	return False

def get_bigrams(wordlist):
	return zip(zip(wordlist, wordlist[1:]), wordlist[2:])

def get_trigrams(wordlist):
	return zip(zip(wordlist, wordlist[1:], wordlist[2:]), wordlist[3:])

def remove_ngrams_with_dots(ngram_lists):
	new_ngram_lists = []
	for ngram_list in ngram_lists:
		new_ngram_lists.append([ngram for ngram in ngram_list if not contains_special_character(ngram)])
	return new_ngram_lists

def remove_special_characters_from_ngrams(ngram_lists):
	comp = re.compile("[\.!?,;:](?!\d,;)", re.UNICODE)
	new_ngram_lists = []
	for n_gram_list in ngram_lists:
		new_ngram_list = []
		for a, b in n_gram_list:
			tuple_list = []
			for word in a:
				tuple_list.append(comp.sub('', word))
			new_ngram_list.append((tuple([tuple(tuple_list), comp.sub('', b)])))
		new_ngram_lists.append(new_ngram_list)
	return new_ngram_lists

def get_ngram_dict(ngram_lists):
	ngram_dict = {}
	for ngram_list in ngram_lists:
		for key, value in ngram_list:
			ngram_dict.setdefault(key, []).append(value)
	return ngram_dict

if __name__ == '__main__':
	ngram_func = get_bigrams # Choose which type of ngram to use
	wordlists = get_file_wordlists()
	mod_wordlists = modify_statuses(wordlists)
	ngram_lists = []
	for wordlist in mod_wordlists:
		ngram_lists.append(ngram_func(wordlist))
	ngram_lists = remove_ngrams_with_dots(ngram_lists)
	ngram_lists = remove_special_characters_from_ngrams(ngram_lists)
	ngram_dict = get_ngram_dict(ngram_lists)
	for key in ngram_dict:
		print key, ngram_dict[key]
