from os import environ
from sys import argv
from tweepy import OAuthHandler
from tweepy import API
import csv
import pandas as pd

# CONFIG THIS!!!################################
# replace with your keys or tokens or set environment variables (via export or
# bash_profile or bashrc)
ckey = environ.get('TWITTERCKEY')
csecret = environ.get('TWITTERCSECRET')
atoken = environ.get('TWITTERATOKEN')
asecret = environ.get('TWITTERASECRET')
# set path of inputfile here or give to script in first parameter
input_file = argv[1]
# set path of outputfile here or give to script in second parameter
output_file = argv[2]
# might increase or decrease performance if changed, but bottleneck here is the Twitter API,
# so it won't change a lot. If changed it must be multiples of 100.
retweets_per_batch = 100
# separator used in input csv as regular expression (TAB = '\t')
separator = '\t'
# last collected batch in case the script stops
last_batch = int(argv[3])
#################################################


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


tweettable = pd.read_csv(input_file, sep=separator)


cut_off_rt_index = tweettable[(
    tweettable['text'].str.startswith("RT @") == True) &
    (tweettable['text'].str.endswith('…') == True)].index.values


truncated_number = len(cut_off_rt_index)
untruncated_number = 0

i = 0
id_lists = []

while i < len(cut_off_rt_index):
    id_lists.append(tweettable.loc[cut_off_rt_index[i: i + 100], 'id'])
    i += 100

n = last_batch

if n != 0:
    max_index = cut_off_rt_index[(retweets_per_batch * n) - 1]
else:
    max_index = -1

while n < len(id_lists):

    m = 0
    start_index = max_index + 1

    while m < retweets_per_batch / 100:

        tweets = api.statuses_lookup(id_lists[n].values.tolist())

        for tweet in tweets:

            index = tweettable[(tweettable['id'] == tweet.id)].index.values[0]
            # print(index)

            if hasattr(tweet, 'retweeted_status'):
                tweettable.loc[index, 'text'] = (
                    'RT @' + tweet.retweeted_status.user.screen_name + ': ' +
                    tweet.retweeted_status.text)

                untruncated_number += 1

            # find out whether this tweet has the highest index so far
            # (order was not preserved in the process),
            # if so store in max_index
            if max_index <= index:
                max_index = index
                # print(max_index)

        m += 1
        n += 1

    if start_index == 0:
        tweettable.loc[start_index:max_index].to_csv(path_or_buf=output_file,
                                                     index=False,
                                                     encoding='utf-8',
                                                     quoting=csv.QUOTE_NONNUMERIC)
    else:
        tweettable.loc[start_index:max_index].to_csv(path_or_buf=output_file,
                                                     index=False, header=False,
                                                     encoding='utf-8',
                                                     quoting=csv.QUOTE_NONNUMERIC,
                                                     mode='a')
    print(start_index, max_index)
    print(str(n) +
          ' batches of max. 100 truncated retweets processed and written to' +
          ' csv-file.')

tweettable.loc[max_index + 1:].to_csv(path_or_buf=output_file,
                                      index=False, header=False,
                                      encoding='utf-8', mode='a')

print('Last lines written.')

print('%d out of %d truncated retweets untruncated. Still truncated tweets have \
most likely been deleted by their author, or the account has been \
deleted in the meantime.' % (untruncated_number, truncated_number))
