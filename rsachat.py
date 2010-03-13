#!/usr/bin/env python
#
#   RSA Encrypted communications over twitter by ikex <ashleyis@me.com>
#   
#
#
import rsa, pickle, os, math, twitter, datetime, feedparser, re
from optparse import OptionParser

def get_twitter(url, limit=10):
    twitter_entries = []
    for entry in feedparser.parse(url)['entries'][:limit]:
        text = entry['title']
        text = re.sub(r'#(\w+)', "", text)
        twitter_entries.append(text)
    return twitter_entries

def writeFile(content, file):
    fp = open(file, "w")
    pickle.dump(content, fp)
    #fp.writelines(content)
    fp.close()

def genKey():
    print "Generating your keypair, this may take a while.."
    keypair = rsa.gen_pubpriv_keys(1024)
    writeFile(keypair[0], "public_key")
    writeFile(keypair[1], "private_key")
    print "Done!"

def twitterInfo(userpassarr):
    print "Storing your twitter information as .twitterlogin"
    print "THIS /IS/ IN CLEAR TEXT!"
    fp = open(".twitterlogin", "w")
    pickle.dump(userpassarr, fp)
    fp.close()

def getPubPriv():
    if (os.path.isfile("public_key") and os.path.isfile("private_key")):
        fp = open("public_key", "r")
        pubkey = pickle.load(fp)
        fp.close()
        fp = open("private_key", "r")
        privkey = pickle.load(fp)
        fp.close()
        return {'priv': privkey, 'pub': pubkey}
    else:
        return -1

def getLogin():
    if (os.path.isfile(".twitterlogin")):
        fp = open(".twitterlogin", "r")
        a = pickle.load(fp)
        fp.close()
        return a
    else:
        return -1
    
def tweetThis(tweet):
    keys = getPubPriv()
    login = getLogin()
    if keys == -1:
        print "You have not created the proper keys, try ./%s -h" % (sys.argv[0])
        exit(-1)
    if login == -1:
        print "You have not specified your twitter details, try ./%s -h" % (sys.argv[0])
        exit (-1)
    # All seems g2g
    etweet = tweet[len(tweet.split(' ')[0]):]
    htag = tweet[:len(tweet.split(' ')[0])]
    print "Tweeting: %s [%s]" % (etweet, htag)
    enctweet = rsa.encrypt(etweet, keys["pub"])
    splits = int(math.ceil(len(enctweet) / 120.00))
    tweets = {}
    for i in range(0,splits):
        tweets[i] = "%s" % (enctweet[(i*120):(i+1)*120])
    header = "[%s/%s] %s" % ("%s", len(tweets), htag)
    #posttweets = {}
    api = twitter.Api(username=login[0], password=login[1])
    for i in range(0, len(tweets)):
        api.PostUpdate("%s %s" % ((header % (i+1)), tweets[i]))
        #posttweets[i+1] = "%s %s" % ((header % (i+1)), tweets[i])
    print "Done!"
    
def readTweet((tag, pubkey)):
    key = getKey(pubkey)
    print "Retrieving tweets.."
    a = get_twitter("http://search.twitter.com/search.atom?q=%s" % tag)
    posts = {}
    for b in a:
        count, data = b.split('[')[1].split(']')
        posts[count.split('/')[0]] = data.strip()
    posts = sortedDictValues1(posts)
    print "Decrypting.."
    outputencr = ""
    for neworder in posts:
        outputencr = outputencr + neworder
    print rsa.decrypt(outputencr.replace("\n", ""), key).strip()
    print "Done!"
    
def getKey(filepath):
    fp = open(filepath)
    a = pickle.load(fp)
    fp.close()
    return a

def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]


if __name__ == "__main__":
    print "RSA Encrypted tweets by ikex <ashleyis@me.com>"
    parser = OptionParser(version="%prog 0.1")
    parser.add_option("-g", dest="genkey", help="Generate a private/public key for use", action="store_true")
    parser.add_option("-a", "--twitter", dest="twitter", help="Your twitter login specified as <user> <pass>", metavar="login", nargs=2)
    parser.add_option("-t", dest="tweet", help="Post a tweet starting with the hashtag eg, \"#RSAToMyFriends Hi guys!\"", metavar="#tag tweet")
    parser.add_option("-r", dest="readtweet", help="Reads a tweet with the specified tag pubkey", metavar="tag pubkey", nargs=2)
    (options, args) = parser.parse_args()
    if options.genkey: genKey()
    elif options.twitter: twitterInfo(options.twitter)
    elif options.tweet: tweetThis(options.tweet)
    elif options.readtweet: readTweet(options.readtweet)