*THIS IS REALLY BUGGY/HACKED TOGETHER*

h1. Changelog

09/1/11 - Remote code could be executed via the rsa libraries decrypt method (using pickle). rsa has been upgraded to the mercurial head which doesnt use pickle. 
 Refactored the rsachat.py code to not use pickle either, this also means you will need to re-authenticate to twitter, and regenerte keys (sorry!) with the bonus
 that you're now safe from pickle related vulnerabilities (now using yaml, which is alot safer) thanks [@dbph](https://twitter.com/dbph)

08/1/11 - Updated with twitter OAUTH login support(and latest supporting libraries as of 8/1/11), thanks to [@mpesce](http://twitter.com/mpesce)



h1. RSATweets in action!

![Alt text](http://img696.imageshack.us/img696/7217/screenshot20100314at954.png "In action")

Basically you create a new keypair with:  
``./rsachat -g``  
  
Receive a twitter login token with(and follow the prompts):  
``./rsachat -o``  
  
Give your friends the file private_key  
and start tweeting with  
``./rsachat -t thiswasatriumph "Huge Success" ``  
  
and reading tweets like  
``./rsachat -r thiswasatriumph some_user their_key``  
  
ikebook:rsatweets ashleyis$ ./rsachat.py -h  
RSA Encrypted tweets by ikex <ashleyis@me.com>
Usage: rsachat.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -g                    Generate a private/public key for use
  -o                    Authorize access to your Twitter account
  -t #tag tweet         Post a tweet starting with the hashtag eg,
                        "#RSAToMyFriends Hi guys!"
  -r tag author pubkey  Reads a tweet with the specified tag author pubkey
  
