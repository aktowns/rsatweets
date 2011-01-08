*THIS IS REALLY BUGGY/HACKED TOGETHER*

Updated with twitter OAUTH login support(and latest supporting libraries as of 8/1/11), thanks to [@mpesce](http://twitter.com/mpesce)

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
  
You can also now SEND FILES over twitter!  
``./rsachat -f "#sometextFile" blah.txt``  
  
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
  -f #tag filename.txt  Post a file encrypted as tweets eg, "#tag <filename>"
  -r tag author pubkey  Reads a tweet with the specified tag author pubkey
  
