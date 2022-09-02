#!/usr/bin/python3

import os
import logging
import certstream
from logging.handlers import TimedRotatingFileHandler

def print_callback(message, context):
	if message['message_type'] == "heartbeat":
		return
	if message['message_type'] == "certificate_update":
		all_domains = message['data']['leaf_cert']['all_domains']
		if len(all_domains) == 0:
			domain = "NULL"
		else:
			domain = all_domains[0]
		logger.error(domain)
		for element in message['data']['leaf_cert']['all_domains']:
			logger.error(element)
		logger.handlers[0].flush()


def main():
	global logger
	logging.basicConfig(handlers=[TimedRotatingFileHandler(os.path.dirname(os.path.realpath(__file__)) + "/downloaded_domains/certstream_domain.txt",
						when="D",
						interval=1)],
						level=logging.DEBUG,format="%(message)s")
	logger = logging.getLogger()
	certstream.listen_for_events(print_callback, url='wss://certstream.calidog.io/')


if __name__ == "__main__":
    main()
