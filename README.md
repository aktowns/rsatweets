*THIS IS REALLY BUGGY/HACKED TOGETHER*

![Alt text](http://img696.imageshack.us/img696/7217/screenshot20100314at954.png "In action")


Basically you create a new keypair with  
``./rsachat -g``  
  
enter your twitter login information with  
``./rsachat -a User Pass``  
  
give your friends the file Private_key (dont ask.. -.-)  
and start tweeting with  
``./rsachat -t thiswasatriumph "Huge Success" ``  
  
and reading tweets like  
``./rsachat -r thiswasatriumph someUser their_key``  
  
You can also now SEND FILES over twitter!  
``./rsachat -f "#sometextFile" blah.txt``  
  
ikebook:rsatweets ashleyis$ ./rsachat.py -h  
RSA Encrypted tweets by ikex <ashleyis@me.com>  
Usage: rsachat.py [options]  
  
Options:  
  --version             show program's version number and exit  
  -h, --help            show this help message and exit  
  -g                    Generate a private/public key for use  
  -a login              Your twitter login specified as <user> <pass>  
  -t #tag tweet         Post a tweet starting with the hashtag eg, "#RSAToMyFriends Hi guys!"  
  -f #tag filename.txt  Post a file encrypted as tweets eg, "#tag <filename>"  
  -r tag author pubkey  Reads a tweet with the specified tag author pubkey  
ikebook:rsatweets ashleyis$   
  
