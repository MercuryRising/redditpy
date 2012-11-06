#! /usr/bin/env python2
import json, urllib
url = "http://www.reddit.com/r/all.json"
all = urllib.urlopen(url).read()
content = json.loads(all.decode("utf8"))
y = 1
stories = {}

for x in content['data']['children']:
	print "[%d] " % y + x['data']['title']
	if x['data']['selftext'] != "":
		print "[Self Text]"
		selftext = x['data']['selftext']
		stories[y] = selftext
	y += 1
while(1):
	st = raw_input("Which selfpost would you like to view? > ")
	if st == "exit":
		exit()
	try:
		print stories[int(st)]
	except (KeyError, ValueError):
		print "Sorry, that post does not contain self-text"
