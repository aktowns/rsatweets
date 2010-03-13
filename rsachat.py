#!/usr/bin/env python
#
#   RSA Encrypted communications over twitter by ikex <ashleyis@me.com>
#   
#
#
import rsa, pickle, os, math, twitter, datetime, feedparser, re, binascii, sys
from optparse import OptionParser

def get_twitter(url, limit=10):
    twitter_entries = []
    for entry in feedparser.parse(url)['entries'][:limit]:
        text = entry['title']
        #print entry['author']
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
    
def readTweet((tag, author, pubkey)):
    key = getKey(pubkey)
    print "Retrieving tweets.."
    if (tag[0:1] == "#"): tag = tag[1:]
    a = get_twitter("http://search.twitter.com/search.atom?q=%s%%20%s" % (tag, author))
    posts = {}
    for b in a:
        count, data = b.split('[')[1].split(']')
        posts[count.split('/')[0]] = data.strip()
    posts = sortedDictValues1(posts)
    print "Decrypting.."
    outputencr = ""
    for neworder in posts:
        outputencr = outputencr + neworder
    decrypted = rsa.decrypt(outputencr.replace("\n", ""), key).strip()
    if decrypted[0:5].strip() == "FILE:":
        print "Tweet is a file, decrypting.."
        a = pickle.loads(binascii.a2b_base64(decrypted[5:]))
        filename = a['filename'].replace("/", "")
        fp = open(filename, "w")
        fp.write(binascii.a2b_base64(a['data']))
        print "Saved: %s" % a['filename']
    else:
        print "==========================="
        print "@%s: %s" % (author, decrypted)
        print "==========================="
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

def fileThis((tag, filename)):
    print "Encoding %s" % filename
    fp = open(filename, 'rb')
    encoded = binascii.b2a_base64(fp.read())
    fp.close()
    sendme = {'filename': filename, 'data':encoded}
    data = pickle.dumps(sendme)
    keys = getPubPriv()
    login = getLogin()
    if keys == -1:
        print "You have not created the proper keys, try ./%s -h" % (sys.argv[0])
        exit(-1)
    if login == -1:
        print "You have not specified your twitter details, try ./%s -h" % (sys.argv[0])
        exit (-1)
    # All seems g2g
    etweet = "FILE: %s" % binascii.b2a_base64(data)
    htag = tag
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



if __name__ == "__main__":
    print "RSA Encrypted tweets by ikex <ashleyis@me.com>"
    parser = OptionParser(version="%prog 0.1")
    parser.add_option("-g", dest="genkey", help="Generate a private/public key for use", action="store_true")
    parser.add_option("-a", dest="twitter", help="Your twitter login specified as <user> <pass>", metavar="login", nargs=2)
    parser.add_option("-t", dest="tweet", help="Post a tweet starting with the hashtag eg, \"#RSAToMyFriends Hi guys!\"", metavar="#tag tweet")
    parser.add_option("-f", dest="tweetfile", help="Post a file encrypted as tweets eg, \"#tag <filename>\"", metavar="#tag filename.txt", nargs=2)
    parser.add_option("-r", dest="readtweet", help="Reads a tweet with the specified tag author pubkey", metavar="tag author pubkey", nargs=3)
    (options, args) = parser.parse_args()
    if options.genkey: genKey()
    elif options.twitter: twitterInfo(options.twitter)
    elif options.tweet: tweetThis(options.tweet)
    elif options.readtweet: readTweet(options.readtweet)
    elif options.tweetfile: fileThis(options.tweetfile)