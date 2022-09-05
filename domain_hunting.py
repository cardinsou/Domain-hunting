#/usr/bin/python3

import os
import io
import re
import sys
import base64
import shutil
import sqlite3
import zipfile
import requests
import datetime 


debug = 0
log_file = os.path.dirname(os.path.realpath(__file__)) + "/domain_hunting.log"
db_file_path = os.path.dirname(os.path.realpath(__file__)) + "/domain_hunting.sqlite"
output_file_path = os.path.dirname(os.path.realpath(__file__)) + "/today_domains.txt"


today_domains = []
regex_list = [	"regex_1",
		"regex_2"]


#Feed 1
#https://certstream.calidog.io/
#feed from certstream_daemon.py output

def get_feed_1():
	log_message("Feed 1 START")
	yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
	replace_word_list = ["www.","*.","cpanel.","webmail.","webdisk.","mail.","autodiscover.","api.","storage.","portal.", "cpcalendars.", "cpcontacts."]
	try:
		with open(os.path.dirname(os.path.realpath(__file__)) + "/downloaded_domains/certstream_domain.txt." + yesterday,"r") as file_in:
			for domain in file_in.readlines():
				clean_domain = domain.strip()
				for replace_word in replace_word_list:
					clean_domain = clean_domain.replace(replace_word,"")	
				match_domain(clean_domain)
		log_message("Feed 1 END OK")
	except KeyboardInterrupt:
		log_message("Feed 1 END FAIL - User interrupt")
		exit(1)
	except:
		log_message("Feed 1 END FAIL")
		log_message(sys.exc_info())
	return


#Feed 2
#https://www.whoisds.com/newly-registered-domains

def get_feed_2():
	log_message("Feed 2 START")
	yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
	to_encode_name = yesterday + '.zip'
	encoded_name = base64.b64encode(to_encode_name.encode('utf-8'))
	url= "https://whoisds.com/whois-database/newly-registered-domains/" + str(encoded_name, "utf-8") + "/nrd"
	if debug == 1:
		log_message("Download domain list from: " + url)
	try:
		r = requests.get(url)
		z = zipfile.ZipFile(io.BytesIO(r.content)).extractall(path=os.path.dirname(os.path.realpath(__file__)) + "/downloaded_domains/")
		shutil.move(os.path.dirname(os.path.realpath(__file__)) + "/downloaded_domains/domain-names.txt", os.path.dirname(os.path.realpath(__file__)) + "/downloaded_domains/domain-names.txt." + yesterday)
		with open(os.path.dirname(os.path.realpath(__file__)) + "/downloaded_domains/domain-names.txt." + yesterday,"r") as file_in:
			for domain in file_in.readlines():
				clean_domain = domain.strip()
				match_domain(clean_domain)		
		log_message("Feed 2 END OK")
	except KeyboardInterrupt:
		log_message("Feed 2 END FAIL - User interrupt")
		exit(1)
	except:
		log_message("Feed 2 END FAIL")
		log_message(sys.exc_info())	
	return


def match_domain(domain):
	for regex in regex_list:
		if re.search(regex, domain):
			if debug == 1:
				log_message(domain + " MATCH")
			if (domain not in today_domains):
				today_domains.append(domain)
				if debug == 1:
					log_message(domain + " INSERTED")	
			break
	return 


def check_db():
	try:
		db_connection = sqlite3.connect(db_file_path)
		db_cursor = db_connection.cursor()
		db_cursor.execute("CREATE TABLE IF NOT EXISTS domain_table(domain_name TEXT PRIMARY KEY, domain_date TEXT NOT NULL);")
		db_connection.commit()
		log_message("Check DB OK")
		return db_connection,db_cursor
	except KeyboardInterrupt:
		log_message("Check DB FAIL - User interrupt")
		exit(1)
	except:
		log_message("Check DB FAIL")
		log_message(sys.exc_info())
		exit(1)
			

def insert_domain(db_connection,db_cursor):
	matching_domains = []
	for domain in today_domains:
		if domain not in matching_domains:
			matching_domains.append((domain.encode("latin1"),datetime.date.today().strftime('%Y%m%d')))
	try:
		db_cursor.executemany("INSERT OR IGNORE INTO domain_table VALUES (?,?)",matching_domains)
		db_connection.commit()
		log_message("Insert domain in DB OK")
	except KeyboardInterrupt:
		log_message("Insert domain in DB FAIL - User interrupt")
		exit(1)
	except:
		log_message("Insert domain in DB FAIL")
		log_message(sys.exc_info())
		exit(1)
	

def get_today_domains(db_connection,db_cursor):
	domain_string = ""
	try:
		db_cursor.execute("SELECT domain_name FROM domain_table WHERE domain_date==" + datetime.date.today().strftime('%Y%m%d') + " ORDER BY domain_name ASC")
		rows = db_cursor.fetchall()
		for row in rows:
			domain_string += str(row[0], "utf-8") + "\n"
		db_connection.close()
		if debug == 1:
			log_message("Today domains: " + domain_string.replace("\n",",")[:-1])
		log_message("Extract domain from DB OK")
		return domain_string
	except KeyboardInterrupt:
		log_message("Extract domain from DB FAIL - User interrupt")
		exit(1)
	except:
		log_message("Extract domain from DB FAIL")
		log_message(sys.exc_info())
		exit(1)	
	
	
def print_domains(db_connection,db_cursor):
	domain_string = get_today_domains(db_connection,db_cursor)
	if domain_string:
		try:
			with open(output_file_path, "w") as file_out:
				file_out.write(domain_string)
			log_message("Printing domains OK")
		except KeyboardInterrupt:
			log_message("Printing domains FAIL - User interrupt")
			exit(1)
		except:
			log_message("Printing domains FAIL")
			log_message(sys.exc_info())
			exit(1)


def log_message(message):
	with open(log_file, "a") as file_log:
		file_log.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - " + str(message) + "\n")
		
	
def main():
	log_message("Domain hunting START")
	if debug == 1:
		log_message("regex_list: " + str(regex_list))
	db_connection,db_cursor = check_db()
	get_feed_1()
	get_feed_2()
	insert_domain(db_connection,db_cursor)
	print_domains(db_connection,db_cursor)
	log_message("Domain hunting END")


if __name__ == "__main__":
    main()
