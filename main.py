# -*- coding: utf-8 -*-
import pycurl
import json
from bs4 import BeautifulSoup
import urllib2
import datetime
import sys
import ConfigParser

#settings

configParser = ConfigParser.RawConfigParser();

configParser.read('./settings.cfg')

slack_url = configParser.get('settings', 'url')
channel = configParser.get('settings', 'channel')
username = configParser.get('settings', 'username')


def get_meal(url):
	f = urllib2.urlopen(url)
	soup = BeautifulSoup(f.read().decode('utf-8'), "lxml")
	foods = soup.find_all('div', 'col-xs-10 text-left')
	return '- ' + '\n- '.join(food.string.strip() for food in foods)

url = 'http://www.hors.se/restaurang/bistro-j/'
meal = get_meal(url)

data = json.dumps({"channel": channel, "username": username, "text":meal})

c = pycurl.Curl()
c.setopt(pycurl.URL, slack_url)
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, data)
c.perform()
