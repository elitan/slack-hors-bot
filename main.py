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
	foods = soup.find_all('td')
	dn = datetime.datetime.today().weekday()
	days = [u'måndag', u'tisdag', u'onsdag', u'torsdag', u'fredag']

	if foods[dn * 3].string == "":
		return False

	s = u"*%s*\n" % (days[dn])
	s += u"-: %s\n" % foods[dn * 3].get_text().strip()
	s += u"-: %s\n" % foods[dn * 3 + 1].get_text().strip()
	s += u"-: %s\n" % foods[dn * 3 + 2].get_text().strip()
	return s

url = "http://www.hors.se/veckans-meny/?week_for=%s&rest=183" % (datetime.date.today())
url2 = "http://www.hors.se/veckans-meny/?week_for=%s" % (datetime.date.today())

meal = get_meal(url)

if not meal or '--' in meal:
	print('url2')
	meal = get_meal(url2)
data = json.dumps({"channel": channel, "username": username, "text":meal})

c = pycurl.Curl()
c.setopt(pycurl.URL, slack_url)
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, data)
c.perform()
