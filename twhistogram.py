#!/usr/bin/python
try:
	import json
except ImportError:
	import simplejson as json
import os, sys
from datetime import datetime

def usage():
    print "Usage:\n./twhistogram.py username password\n"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        quit(0)

    user, password = sys.argv[1], sys.argv[2]

    cmd = "curl -u %s:%s http://twitter.com/statuses/friends_timeline.json?count=100" % (user, password)
    os.system("%s > tmpfile.json" % (cmd))
    file = open("tmpfile.json", 'r')
    tweets = json.load(file)

    histogram = []
    for i in range(24):
        histogram.append({'count':0})

    for tweet in tweets:
        tweettime = datetime.strptime( tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y" )
        histogram[tweettime.hour]['count'] += 1
        histogram[tweettime.hour]['time'] = tweettime.hour

    for i,hour in enumerate(histogram):
        if 'time' not in hour:
            hour['time'], hour['count'] = i,0
        print "%s %s" % ( hour['time'], (hour['count'] * '#'))
