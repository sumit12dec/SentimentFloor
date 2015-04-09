import urllib
import urllib2
import json
import datetime
import random
import pickle
from datetime import timedelta
import twitter as TWEET

class TwitterData:
    #start __init__
    def __init__(self):
        self.currDate = datetime.datetime.now()
        self.weekDates = []
        self.weekDates.append(self.currDate.strftime("%Y-%m-%d"))
        for i in range(1,7):
            dateDiff = timedelta(days=-i)
            newDate = self.currDate + dateDiff
            self.weekDates.append(newDate.strftime("%Y-%m-%d"))
        #end loop
    #end

    #start getWeeksData
    def getTwitterData(self, keyword, time,CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
        #print keyword,time,"000000000000000000000"
        self.weekTweets = {}
        if(time == 'lastweek'):
            for i in range(0,6):
                params = {'since': self.weekDates[i+1], 'until': self.weekDates[i]}
                self.weekTweets[i] = self.getData(keyword,CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,params)
            #end loop
            
            #Write data to a pickle file
            filename = 'data/weekTweets/weekTweets_'+urllib.unquote(keyword.replace("+", " "))+'_'+str(int(random.random()*10000))+'.txt'
            outfile = open(filename, 'wb')        
            pickle.dump(self.weekTweets, outfile)        
            outfile.close()
        elif(time == 'today'):
            for i in range(0,1):
                params = {'since': self.weekDates[i+1], 'until': self.weekDates[i]}
                self.weekTweets[i] = self.getData(keyword,CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,params)
            #end loop
        #print self.weekTweets,"+++++++++++++"
        return self.weekTweets
    '''
        inpfile = open('data/weekTweets/weekTweets_obama_7303.txt')
        self.weekTweets = pickle.load(inpfile)
        inpfile.close()
        return self.weekTweets
    '''
    #end

    #start getTwitterData   


    def getData(self, keyword, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, params = {}):
        #maxTweets = 50
        #url = 'http://search.twitter.com/search.json'    
        #data = {'q': keyword, 'lang': 'en', 'page': '1', 'result_type': 'recent', 'rpp': maxTweets, 'include_entities': 0}

        #Add if additional params are passed
        api = TWEET.Api(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
        tweets = api.GetSearch(term=keyword,count=100,since=params['since'],until=params['until'])
        #print tweets,'\n\n'
        if len(tweets)>0:
            tweets = tweets
        else:
            flash('Unable to load tweets from Twitter. Maybe out of '
                  'API calls or Twitter is overloaded.')    
        try:            
            tweets_lst = []
            for item in tweets:
                tweets_lst.append(item.text)            
            return tweets_lst
        except e:
            self.handleError(e)         
    #end    

    #start handleError
    def handleError(self, e):
        print e.code
        print e.read()
        return -1
    #end
#end class
