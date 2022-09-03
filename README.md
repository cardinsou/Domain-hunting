# Domain hunting

Scripts in this repo retrieve domains from:

- [Certstream](https://certstream.calidog.io/)
- [whoisds.com](https://www.whoisds.com/newly-registered-domains)

Match domain with regex you set and save the results. The main purpose is to find domain that can host phishing or similar activities. 

## Certstream

Certstream is a stream of newly registered certificates. All the certificates have one or more associated domain. Based on the stream format, you need to listen 24h/24h to record all the data.


## whoisds.com

whoisds.com publishes every day a list of domains registered the previous day.

## Usage

- Install Certstream

```
pip3 install certstream
```

- Clone repo

```
git clone https://github.com/cardinsou/Domain-hunting.git
```

- Modify "path" variable content in check_up.sh, you must insert the path where you clone the repo

```
#!/bin/bash

path="/home/<user>/Domain-hunting"

if [ ! -d "$path/downloaded_domains" ]
	then
		mkdir "$path/downloaded_domains"
.........
```

- Customize domain regex (based on what you want to match) in file domain_hunting.py, list "regex_list"

```
.........

debug = 0
log_file = os.path.dirname(os.path.realpath(__file__)) + "/domain_hunting.log"
db_file_path = os.path.dirname(os.path.realpath(__file__)) + "/domain_hunting.sqlite"
output_file_path = os.path.dirname(os.path.realpath(__file__)) + "/today_domains.txt"

today_domains = []
regex_list = [	"regex_1",
                "regex_2"]

.........
```

- Add to crontab the following entry

```
#domain hunting script
0 10 * * * /usr/bin/python3 /home/<user>/Domain-hunting-main/domain_hunting.py

#check if domain hunting utilities are up and purge old log data
0 6 * * * /home/<user>/Domain-hunting-main/check_up.sh
```

We schedule a check at 6:00 AM and domain extraction at 10:00 AM

- Wait for results
	
	Every day at 10:00 AM domain hunting script runs and saves matching domains in "today_domains.txt" file. After script running, in the same folder you can find also a sqlite DB and a log file. Sqlite DB contains domains previously matched, so you will be able to keep track of historical match.
	Every day at 6:00 AM check_up.sh script will run. This script check if certstream daemon is running and purge domains downloaded more that a week ago. 


