# Domain hunting

Retrieve domains from:

- [Certstream](https://certstream.calidog.io/)
- [whoisds.com](https://www.whoisds.com/newly-registered-domains)

Check if 

## Certstream



## whoisds.com


## Usage

- Install Certstream

```
pip3 install certstream
```

- Download repo and unzip the package

```
unzip Domain-hunting-main.zip
```

- Modify "path" variable content in check_up.sh, you must insert the path where you uncompress the archive

```
#!/bin/bash

path="/home/<user>/Domain-hunting-main"

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

- Start collection
  
  Following command verify 
  
```
/home/<user>/Domain-hunting-main/check_up.sh
```

- Add to crontab the following entry

```
#domain hunting script
0 10 * * * /usr/bin/python3 /home/<user>/Domain-hunting-main/domain_hunting.py

#check if domain hunting utilities are up and purge old log data
0 6 * * * /home/<user>/Domain-hunting-main/check_up.sh
```

We schedule a running check at 6:00 AM and domain extraction at 10:00 AM




