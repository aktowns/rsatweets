#!/usr/bin/env python
#
#   RSA Encrypted communications over twitter by ikex <ashleyis@me.com>
#   
#
#
import rsa, os, math, twitter, datetime, feedparser, re, binascii, sys, urllib2, base64, struct, yaml
from yaml import Loader, Dumper
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
    fp = open(file, "wb")
    fp.writelines(yaml.dump(content))
    fp.close()

def genKey():
    print "Generating your keypair, this may take a while.."
    keypair = rsa.newkeys(1024)
    writeFile(keypair[0], "public_key")
    writeFile(keypair[1], "private_key")
    print "Done!"

def authorize():
	result = get_access_token()
	fp = open(".twittercredentials", "wb")
	fp.writelines(yaml.dump(result))
	fp.close()
	
def getPubPriv():
    if (os.path.isfile("public_key") and os.path.isfile("private_key")):
        fp = open("public_key", "rb")
        pubkey = yaml.load(fp)
        fp = open("private_key", "rb")
        privkey = yaml.load(fp)
        fp.close()
        return {'priv': privkey, 'pub': pubkey}
    else:
        return -1

def getLogin():
    if (os.path.isfile(".twittercredentials")):
        fp = open(".twittercredentials", "r")
        a = yaml.load(fp)
        fp.close()
        return a
    else:
        return -1
    
def tweetThis((htag, etweet)):
    keys = getPubPriv()
    if keys == -1:
        print "You have not created the proper keys, try ./%s -h" % (sys.argv[0])
        exit(-1)
    credentials = getLogin()  
    if credentials == -1:
    	print "You have not authorized Twitter access from this application, try ./%s -h" % (sys.argv[0])
    	exit(-1)
    # All seems g2g
    if htag[0:1] != "#": htag = "#%s" % htag
    print "Tweeting: %s [%s]" % (etweet, htag)
    enctweet = rsa.encrypt(str(etweet), keys["pub"])
    splits = int(math.ceil(len(enctweet) / 120.00))
    tweets = {}
    for i in range(0,splits):
        tweets[i] = "%s" % (enctweet[(i*120):(i+1)*120])
    header = "[%s/%s] %s" % ("%s", len(tweets), htag)
    #posttweets = {}
    #api = twitter.Api(username=login[0], password=login[1])
    api = twitter.Api(consumer_key="LPIi3EFUT0LM7plWL2ZO3w", consumer_secret="hv44nSmJSsiNeWkhy9FNcb5qH0vmCSAZv2GyI2JqYdc",
    	access_token_key=credentials['oauth_token'], access_token_secret=credentials['oauth_token_secret'])
    try:
        for i in range(0, len(tweets)):
            api.PostUpdate("%s %s" % ((header % (i+1)), tweets[i]))
            #posttweets[i+1] = "%s %s" % ((header % (i+1)), tweets[i])
    except urllib2.HTTPError:
        print "Server suffered a random fuckup (its the feds man!) [Internal Server Error: 500] try again soon"
        exit(-1)
    print "Done!"
    
def readTweet((tag, author, pubkey)):
    key = getKey(pubkey)
    print "Retrieving tweets.."
    if (tag[0:1] == "#"): tag = tag[1:]
    a = get_twitter("http://search.twitter.com/search.atom?q=%s%%20%s" % (tag, author))
    if len(a) == 0:
        print "No tweets found with the tag %s for the user %s." % (tag, author)
        exit(-1)
    posts = {}
    for b in a:
        count, data = b.split('[')[1].split(']')
        posts[count.split('/')[0]] = data.strip()
    posts = sortedDictValues1(posts)
    print "Decrypting.."
    outputencr = ""
    for neworder in posts:
        outputencr = outputencr + neworder
    try:
        decrypted = rsa.decrypt(str(outputencr.replace("\n", "")), key).strip()
    except OverflowError:
        print "Overflow error: Wrong key?"
        exit(-1)
    #if decrypted[0:5].strip() == "FILE:":
    #    print "Tweet is a file, decrypting.."
    #    a = pickle.loads(binascii.a2b_base64(decrypted[5:]))
    #    filename = a['filename'].replace("/", "")
    #    fp = open(filename, "w")
    #    fp.write(binascii.a2b_base64(a['data']))
    #    print "Saved: %s" % a['filename']
    #else:
    print "==========================="
    print "@%s: %s" % (author, decrypted)
    print "==========================="
    print "Done!"
    
def getKey(filepath):
    fp = open(filepath, "rb")
    privkey = yaml.load(fp)
    fp.close()
    return privkey

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
    print "Done!"

def get_access_token():
	import os
	import sys
	
	# parse_qsl moved to urlparse module in v2.6
	try:
	  from urlparse import parse_qsl
	except:
	  from cgi import parse_qsl
	
	import oauth2 as oauth
	
	REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
	ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
	AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
	SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'
	
	consumer_key    = "LPIi3EFUT0LM7plWL2ZO3w"
	consumer_secret = "hv44nSmJSsiNeWkhy9FNcb5qH0vmCSAZv2GyI2JqYdc"
	
	if consumer_key is None or consumer_secret is None:
	  print 'You need to edit this script and provide values for the'
	  print 'consumer_key and also consumer_secret.'
	  print ''
	  print 'The values you need come from Twitter - you need to register'
	  print 'as a developer your "application".  This is needed only until'
	  print 'Twitter finishes the idea they have of a way to allow open-source'
	  print 'based libraries to have a token that can be used to generate a'
	  print 'one-time use key that will allow the library to make the request'
	  print 'on your behalf.'
	  print ''
	  sys.exit(1)
	
	signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
	oauth_consumer             = oauth.Consumer(key=consumer_key, secret=consumer_secret)
	oauth_client               = oauth.Client(oauth_consumer)
	
	print 'Requesting temp token from Twitter'
	
	resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')
	
	if resp['status'] != '200':
	  print 'Invalid respond from Twitter requesting temp token: %s' % resp['status']
	else:
	  request_token = dict(parse_qsl(content))
	
	  print ''
	  print 'Please visit this Twitter page and retrieve the pincode to be used'
	  print 'in the next step to obtaining an Authentication Token:'
	  print ''
	  print '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token['oauth_token'])
	  print ''
	
	  pincode = raw_input('Pincode? ')
	
	  token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
	  token.set_verifier(pincode)
	
	  print ''
	  print 'Generating and signing request for an access token'
	  print ''
	
	  oauth_client  = oauth.Client(oauth_consumer, token)
	  resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % pincode)
	  access_token  = dict(parse_qsl(content))
	
	  if resp['status'] != '200':
		print 'The request for a Token did not succeed: %s' % resp['status']
		print access_token
	  else:
		print 'Your Twitter Access Token key: %s' % access_token['oauth_token']
		print '          Access Token secret: %s' % access_token['oauth_token_secret']
		print ''
		return access_token
	
if __name__ == "__main__":
	print "RSA Encrypted tweets by ikex <ashleyis@me.com>"
	parser = OptionParser(version="%prog 0.2")
	parser.add_option("-g", dest="genkey", help="Generate a private/public key for use", action="store_true")
	parser.add_option("-o", dest="oauth", help="Authorize access to your Twitter account", action="store_true")
	parser.add_option("-t", dest="tweet", help="Post a tweet starting with the hashtag eg, \"#RSAToMyFriends Hi guys!\"", metavar="#tag tweet", nargs=2)
	#parser.add_option("-f", dest="tweetfile", help="Post a file encrypted as tweets eg, \"#tag <filename>\"", metavar="#tag filename.txt", nargs=2)
	parser.add_option("-r", dest="readtweet", help="Reads a tweet with the specified tag author pubkey", metavar="tag author pubkey", nargs=3)
	(options, args) = parser.parse_args()
	if options.genkey: genKey()
	elif options.oauth: authorize()
	elif options.tweet: tweetThis(options.tweet)
	elif options.readtweet: readTweet(options.readtweet)
	#elif options.tweetfile: fileThis(options.tweetfile)
	else: parser.print_help()
		