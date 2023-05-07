# Notifoot
_Get match results with notifications while you are working._

## What does it do?
Run this script and you will have updates on the matches today, thanks to this amazing [API](https://worldcupjson.net) ([repo](https://github.com/estiens/world_cup_json)).  
Now, you can work and get frequent updates on what's goiing on without refreshing endlessly your news feed!

## How to run it?
You will need Python3 and a few libs that you can get with pip:
```
pip install plyer
pip install requests
```
After this, simply do `python notifoot.py` and let it go!  

You can enable SMS notification: if you have Free Mobile, follow the instructions [here](https://www.prodigemobile.com/tutoriel/service-notification-sms-free-mobile/) and copy the link in the `key` file (or create one such file): it should look like `https://smsapi.free-mobile.fr/sendmsg?user=12345678&pass=xxxxxxxxxxxxxx&msg=` (erase what's after `msg=`).  
The link you have is personal and should not be shared to the Internet!  

⚠️ **NOTE**: if you are not in Europe (France), you may want to adjust `timeZone_sec` in line 14.  
For example, if you are in the USA (EST), set this variable to -18000 (UTC-5). If you are in UAE (GST), set it to 14400 (UTC+4). 

## Why this project?
Because I wanted to follow the matches without being noticed (and to be more productive).  
Note: I did this in thirty minutes during a half-time break so the script may (and will) contain bugs: feel free to do issues so I can fix it!  

And now, you have my super-power!
