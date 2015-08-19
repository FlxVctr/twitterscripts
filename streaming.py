import tweepy

# insert keys and tokens here
ckey2 = ''
csecret2 = ''
atoken2 = ''
asecret2 = ''

trackword = [''] # insert trackwords here

# create "keychain"
auth2 = tweepy.OAuthHandler(ckey2, csecret2)
auth2.set_access_token(atoken2, asecret2)

# create the API "object"

api = tweepy.API(auth2, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        print('@' + status.user.screen_name + ': ' + status.text)
        
    def on_error(self, status_code):
        print('error code = %s' % status_code)
        return False


def main():

    myListener = MyStreamListener()

    print('Printing all tweets about your trackwords.')

    myStream = tweepy.Stream(auth = api.auth, listener=myListener, timeout=None)
    myStream.filter(track = trackwords)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')