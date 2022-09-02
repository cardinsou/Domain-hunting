#!/bin/bash

path="/home/<user>/domain-hunting"

#check if download folder is present

if [ ! -d "$path/downloaded_domains" ]
	then
		mkdir "$path/downloaded_domains"
fi

#check if certstream daemon process is up and running

process_up=`ps -ef | grep "certstream_daemon.py" | grep -v grep | wc -l`

if [ $process_up -lt 1 ]
	then
		nohup /usr/bin/python3 $path/certstream_daemon.py >/dev/null 2>&1 &
fi

#remove downloaded domains older than one week

remove_date=`date --date='-1 week' +'%Y-%m-%d'`
rm -f "$path/downloaded_domains/certstream_domain.txt."$remove_date >/dev/null 2>&1
rm -f "$path/downloaded_domains/domain-names.txt."$remove_date >/dev/null 2>&1
