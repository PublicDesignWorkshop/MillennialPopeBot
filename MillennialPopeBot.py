from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import csv
import datetime

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#dictionary of words to replace
replace = { 
            "bad": "sketchy",
            "Body": "Fam",
            "Blessed": "On Fleek",
            "blessed": "#blessed",
            "blessings": "Netflix and Chill",
            "brothers": "bros",
            "brother": "bro",
            "charity": "aesthetic",
            "Church": "Fam",
            "Church's": "Fam's",
            "condemn": "throw shade at",
            "condemning": "throwing shade at",
            "condemnation": "throwing shade",
            "communion": "Netflix and Chill",
            "compassion": "feels",
            "devil": "hater",
            "Devil": "Hater",
            "died": "slayed",
            "dirty": "ratchet",
            "disciples": "fam",
            "disciple": "bro",
            "exceed": "slay",
            "excell": "slay",
            "excells": "slays",
            "excellent": "on fleek",
            "evil": "haters",
            "faith": "swag",
            "Faith": "Swag",
            "family": "fam",
            "families": "fams",
            "fear": "FOMO",
            "fears": "FOMO",
            "filthy": "ratchet",
            "followers": "fam",
            "forgive": "twerk",
            "forgiveness": "twerking",
            "forgiving": "twerking",
            "friendship": 'swag',
            "gift": "aesthetic",
            "gifts": "aesthetics",
            "Gospel": "Aesthetic",
            "great": "on fleek",
            "greatly": "hella",
            "grave": "ratchet",
            "gravely": "hella",
            "heart": "aesthetic",
            "hearts": "aesthetic",
            "heaven": "aesthetic",
            "ideal": "on fleek",
            "joy": "bae",
            "joys": "baes",
            "life": "goals",
            "love": "swag",
            "Love": "Swag",
            "loving": "dabbing",
            "Mary": "Bae",
            "mercy": "dabbing",
            "peace": "aesthetic",
            "People": "Fam",
            "people": "fam",
            "perfect": "on point",
            "pray": "turn up",
            "prayer": "turning up",
            "prayers": "turning up",
            "Priests": "the Squad",
            "really": "hella",
            "Religious": "Fam",
            "rest": "Netflix and Chill",
            "Saints": "Squad",
            "serve": "slay",
            "sick": "basic girls",
            "sickness": "FOMO",
            "sickly": "ratchet",
            "sin": "FOMO",
            "sinful": "ratchet",
            "sins": "FOMO",
            "sinner" : "hater",
            "sinners": "haters",
            "temptation": "FOMO",
            "thing": "thang",
            "that": "dat",
            "the": "da",
            "though": "doe",
            "value": "aesthetic",
            "values": "aesthetics",
            "very": "hella",
            "vile": "ratchet",
            "voice": "shout out",
            "yes": "YAASSSS",
            "you're": "your"}


#Phrases to use at the end of a tweet
endPhrases = ["#GOALS", "#SorryNotSorry", "#ByeFelicia", "#BLESSED", "#ICantEven",
                "#turnUp", "#justPopeThings", "YAAASSSSSS", "#AMEN"]

#End Phrases of different lengths
vShortEndPhrases = [":)", ":P", ";)", "XD", ":D"]
shortEndPhrases = ["#slay", "lol", "#YOLO", "XOXO", "#AMEN"]
medEndPhrases = ["#BLESSED", "#turnUp", "Amirite?",]

#List of linking verbs the bot can use to know when to use the word "af"
linkingVerbs = ["am", "are", "was", "were", "become", "became", "feel", 
                "felt", "been", "be", "grow", "grown", "grew", "look", "looks",
                "remain", "seem", "seems"]

name = "MillennialPope"

def getFollowers():
    """
    Gets details about followers of the bot
    """

    names = []                  #Name of follower
    usernames = []              #Username of follower
    ids = []                    #User id of follower
    locations = []              #Location of follower(as listed on their profile)
    follower_count = []         #How many followers the follower has
    time_stamp = []             #Date recorded

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")


    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    follower_count.append("# of their Followers")
    time_stamp.append("Time Stamp")

    next_cursor = -1

    #Get follower list (200)
    while(next_cursor):
        get_followers = twitter.get_followers_list(screen_name=name,count=200,cursor=next_cursor)
        for follower in get_followers["users"]:
            try:
                print(follower["name"].encode("utf-8").decode("utf-8"))
                names.append(follower["name"].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't Print")
            usernames.append(follower["screen_name"].encode("utf-8").decode("utf-8"))
            ids.append(follower["id_str"])

            try:
                print(follower["location"].encode("utf-8").decode("utf-8"))
                locations.append(follower["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't Print")

            follower_count.append(follower["followers_count"])
            time_stamp.append(datestamp)
            next_cursor = get_followers["next_cursor"]

    open_csv = open("followers.csv","r",newline='')                         #Read what has already been recorded in the followers file
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))

    rows = zip(names,usernames,ids,locations,follower_count,time_stamp)     #Combine lists

    oldFollowerIDs = []                                                     #Store followers that have already been recorded in the past

    oldFollowers_csv = csv.reader(open_csv)

    for row in oldFollowers_csv:
            oldFollowerIDs.append(row[2])

    open_csv.close()

    open_csv = open("followers.csv","a", newline='')        #Append new followers to the followers file
    followers_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[2] in oldFollowerIDs):                  #if the ID isn't already in the follower list
            followers_csv.writerow(row)

    open_csv.close()

def getMentionsRetweets():
    """
    Gets details of mentions/retweets of the user
    """

    names = []                  #Name of user who retweeted/mentioned
    usernames = []              #Their username
    ids = []                    #Their user id
    locations = []              #Their location (as listed on their profile)
    tweetIDs = []               #ID of the retweet/mention
    tweets = []                 #The retweet/mention text
    time_stamp = []             #Date the retweet/mention was created

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    tweetIDs.append("Tweet ID")
    tweets.append("Tweet Text")
    time_stamp.append("Time Stamp")

    #Get mentions (200)
    mentions_timeline = twitter.get_mentions_timeline(screen_name=name,count=200)
    for mention in mentions_timeline:
        try:
            print(mention['user']['name'].encode("utf-8").decode("utf-8"))
            names.append(mention['user']['name'].encode("utf-8").decode("utf-8"))
        except:
            names.append("Can't print")
        usernames.append(mention["user"]["screen_name"].encode("utf-8").decode("utf-8"))
        ids.append(mention["user"]["id_str"])
        try:
            print(mention["user"]["location"].encode("utf-8").decode("utf-8"))
            locations.append(mention["user"]["location"].encode("utf-8").decode("utf-8"))
        except:
            locations.append("Can't Print")
        tweetIDs.append(mention["id_str"])
        try:
            print(mention['text'].encode("utf-8").decode("utf-8"))
            tweets.append(mention['text'].encode("utf-8").decode("utf-8"))
        except:
            tweets.append("Can't Print")
        time_stamp.append(mention["created_at"].encode("utf-8").decode("utf-8"))

    #Get retweets (200)
    retweetedStatuses = twitter.retweeted_of_me(count = 100)                                    #Get tweets from the user that have recently been retweeted
    for retweetedStatus in retweetedStatuses:
        statusID = retweetedStatus["id_str"]
        retweets = twitter.get_retweets(id=statusID,count=100)                                  #Get the retweets of the tweet
        for retweet in retweets:
            try:
                print(retweet['user']['name'].encode("utf-8").decode("utf-8"))
                names.append(retweet['user']['name'].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't print")
            
            usernames.append(retweet["user"]["screen_name"].encode("utf-8").decode("utf-8"))

            ids.append(retweet["user"]["id_str"])

            try:
                print(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
                locations.append(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't print")
            
            tweetIDs.append(retweet["id_str"])
            
            try:
                print(retweet['text'].encode("utf-8").decode("utf-8"))
                tweets.append(retweet['text'].encode("utf-8").decode("utf-8"))
            except:
                tweets.append("Can't print")
            
            time_stamp.append(retweet["created_at"].encode("utf-8").decode("utf-8"))


    open_csv = open("mentions_retweets.csv","r",newline='')
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))
    # print(len(names))
    rows = zip(names,usernames,ids,locations,tweetIDs, tweets,time_stamp)

    oldMentionsIDs = []                             #Record mentions/retweets that have already been recorded before

    oldMentions_csv = csv.reader(open_csv)

    for row in oldMentions_csv:
            oldMentionsIDs.append(row[4])

    open_csv.close()

    open_csv = open("mentions_retweets.csv","a", newline='') #Append new mentions/retweets to the list
    mentions_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[4] in oldMentionsIDs):          #if the ID isn't already in the mentions list
            # print(row)
            mentions_csv.writerow(row)

    open_csv.close()

def getPopeTweet():
    """
    Saves the pope's most current tweet as a string
    """

    pope_timeline = twitter.get_user_timeline(screen_name="Pontifex",count=1)
    for tweet in pope_timeline:
        #print(tweet['text'].encode('utf8')).decode('utf8')
        return tweet['text'].encode('utf8').decode('utf8')



def makeNewTweet(popeTweetWords):
    """
    Takes a list of words and Millennial Popefies it
    popeTweetWords is a list of words
    """
    numEdits = 0                                #counter of number of changes made to tweet
    newWords = []                               #put new tweet in this list
    index = 0                                   #index of the current word being looked at

    for x in popeTweetWords:                    #For each word in the pope's tweet
        havePunc = False                        #Whether or not it has punctuation
        af = ''
        punc = ''

        #The new tweet's current character count
        currLen = len(' '.join(newWords[:index] + popeTweetWords[index:]))

        #if there is punctuation with the word being checked
        if x[-1] == ',' or x[-1] == '.' or x[-1] == '?' or x[-1] == '!' or x[-1] == ':' or x[-1] == ';':
            havePunc = True                                     #It has punctuation
            punc = x[-1:]                                       #store the punctuation mark for later
            X = x[:-1]                                          #set the word to just the word without punctuation

            if '.' in punc and currLen <= 137:                  #if this word is at the end of a sentence
                for v in linkingVerbs:
                    if index < 3:
                        start = 0
                    else:
                        start = index-3         
                    if v in popeTweetWords[start:index]:        #and if there is a linking verb before it
                        af = " af"                              #Put the "af" at the end of the sentence
                        currLen += index-3                      #Update the character count
                        numEdits += 1                           #and the number of edits done to the tweet
        elif x[-2:].lower() == "'s":        #if the word is possessive
            havePunc = True
            punc = "'s"             #store the 's
        else:   
            X = x                                               #Otherwise make no changes to the word

        if X == '&amp':
            newWords.append('&')
        elif X in replace and len(replace[X] + punc) - len(X + punc) + currLen <= 140:  #if it's a key word and adding it  doesn't put tweet over 140 char
            newWords.append(replace[X] + af + punc)                                     #replace it
            numEdits += 1                                                               #add to the number of edits
        elif X.lower() in replace and len(replace[X.lower()] + punc) - len(X.lower()+ punc) + currLen <= 140:
                
            if X == X.lower().capitalize():                                             #check for capitalization
                newWords.append(replace[X.lower()].capitalize() + punc)
            else:                   
                newWords.append(replace[X.lower()].upper() + punc)                      #Or all caps
            numEdits += 1                                                               #add to the number of edits
        else:                                                                           
            newWords.append(X + af + punc)                                              #else don't change word
        index += 1                                                                      #update current index

    currLen = len(' '.join(newWords))

    #if these key words are in the tweet, add these hashtags at the end
    if 'light' in newWords and len(' '.join(newWords)) <= 135:
        newWords.append('#lit')
        numEdits += 1

    if ("dabbing" in newWords or "twerking" in newWords or "party" in newWords) and len(' '.join(newWords)) <= 133:
        newWords.append("#turnt")
        numEdits += 1

    if "Jesus" in newWords and len(' '.join(newWords)) <= 129:
        newWords.append("#daRealMVP")
        numEdits += 1

    if ("values" in popeTweetWords or "should" in popeTweetWords or "must" in popeTweetWords) and len(' '.join(newWords)) <= 133:
        newWords.append("#GOALS")
        numEdits += 1

    currLen = len(' '.join(newWords))

    #Add a hashtag or phrase at the end after determining
    #how close to the character limit the tweet is
    if currLen <= 137:
        #print("short enough!")
        if currLen <= 124:
            #print("long end")
            newWords.append(endPhrases[randint(0, len(endPhrases)-1)])
        elif currLen <= 131:
            newWords.append(medEndPhrases[randint(0, len(medEndPhrases)-1)])
            #print("med end")
        elif currLen <= 134:
            newWords.append(shortEndPhrases[randint(0, len(shortEndPhrases)-1)])
            #print("short end")
        elif currLen <= 137:
            newWords.append(vShortEndPhrases[randint(0, len(vShortEndPhrases)-1)])
            #print("very short end")
        numEdits += 1

    currLen = len(' '.join(newWords))                   #the character count of the finished tweet
    print("Character Count:",currLen)

    if(numEdits < 1):                                   #If no changes to tweet
        return None                                     #Return None
    return newWords                                     #Else return the new tweet


def tweet(tweet):
    """
    Tweets a string
    """
    twitter.update_status(status = tweet);





lastTweet = None        #to store the last tweet that was edited by the bot

def runBot():
    print("Bot running!")

    try:
        getFollowers()
    except:
        print("Couldn't get Followers")

    try:        
        getMentionsRetweets()
    except:
        print("Couldn't get Mentions/Retweets")

    popeTweet = getPopeTweet()                          #Get the Pope's most current tweet
    #popeTweet = ""

    global lastTweet

    if popeTweet != lastTweet:                          #make sure the bot hasn't edited the tweet before
        popeTweetWords = popeTweet.split()              #turn the tweet into a list of words

        try:
            print(popeTweet)
        except:
            print("Cannot print")

        newTweetWords = makeNewTweet(popeTweetWords)    #Edit the tweet

        if newTweetWords == None:                       #If no changes to tweet
            print("No changes to tweet!")
        else:                                           #Otherwise
            newTweet = ' '.join(newTweetWords)          #Combine the words into one string

            try:
                print(newTweet)
            except:
                print("Cannot print")

            # tweet(newTweet)
            if (not debug):                             #If not in debug mode
                try:
                    tweet(newTweet)                     #Tweet the new tweet
                    print("I just tweeted!")
                except:
                    print("Ran into a problem tweeting!")

        lastTweet = popeTweet                           #Make this the latest tweet
    else:
        print("No new Tweet!")

    # tweet(str(randint(0, 200)))




def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


debug = False
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60*1)        #runs every hour
