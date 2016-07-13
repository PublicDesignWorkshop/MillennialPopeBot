from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#dictionary of words to replace
replace = { 
            "bad": "sketchy",
            "Body": "Fam",
            "Blessed": "On Fleek",
            "blessed": "#blessed",
            "blessings": "Netflix and Chill",
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

            if (not debug):                             #If not in debug mode
                try:
                    tweet(newTweet)                     #Tweet the new tweet
                    print("I just tweeted!")
                except:
                    print("Ran into a problem tweeting!")

        lastTweet = popeTweet                           #Make this the latest tweet
    else:
        print("No new Tweet!")




def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


debug = False
runOnce = True

runBot()
if not runOnce:
    setInterval(runBot, 60*60*5)        #runs every 5 hours