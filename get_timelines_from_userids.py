
# Usage: 
# insert consumer and app keys as well as filepaths below
# run (eg in Terminal): python3 scriptname.py
# inputfile is a list of userids
# cc-by-nc Felix Victor Muench (fvmuench@gmail.com)

ckey = ''
csecret = ''
atoken = ''
asecret = ''
tweets_per_user = 42 # max 3200, rate limit adds 1 call per 200 tweets, rate limit is 180 calls every 15 minutes
inputs = '/path/file.csv'
outputs = '/path/file.csv'

import tweepy
import io
import csv

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)


def get_user_timeline(user):
    
    n=0
    timeline = []
    
    try:
        for tweet in tweepy.Cursor(api.user_timeline, user_id = user).items(tweets_per_user):
            if hasattr(tweet, 'retweeted_status'):
                timeline.append('RT @'+ tweet.retweeted_status.user.screen_name + ' ' + tweet.retweeted_status.text)
                n = n + 1
            else:
                timeline.append(tweet.text)
                n = n + 1
    except tweepy.TweepError as e:
        timeline.append(e.reason)
        print(e.reason + ' (for %s)'  %(user))
    
    print('%d Tweets collected for %s' %(n,user))
    
    return timeline

def write_tweets(readpath,writepath):
    
    n = 0
    
    with io.open(readpath,
                 encoding='utf_8', newline='') as userlist, io.open(writepath,encoding='utf_8', mode='w', newline='') as tweetlist:
        users = csv.reader(userlist)
        tweets = csv.writer(tweetlist, delimiter = '\t', lineterminator = '\n')
        
        tweets.writerow(['user_id','Tweet'])
        
        for user in users:
            print('Timelines of %d users gathered so far. Goin on.' %(n))
            timeline = get_user_timeline(user[0])
            for tweet in timeline:
                tweets.writerow([user[0],tweet.replace('\n','\\n')])
            n += 1
        
    print('Tweets of %d users gathered. Pew. That was exciting.' %(n))

write_tweets(inputs, outputs)
