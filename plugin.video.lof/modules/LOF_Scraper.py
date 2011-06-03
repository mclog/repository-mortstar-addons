import os
import sys

import urllib
import re
import time

import LOF_Navigator

class LOF_Scraper:

    def __init__(self):
        # URL's
        self.baseurl = 'http://www.liveonlinefooty.com/'
        self.channelurl = ''.join([self.baseurl, 'watchlive/channel%s.php'])
        self.loginurl = ''.join([self.baseurl, 'amember/login.php'])
        self.memberurl = ''.join([self.baseurl, 'amember/member.php'])
        self.scheduleurl = ''.join([self.baseurl, 'schedule.php'])
        self.swfurl = ' swfUrl=http://www.livesporton.net/player2.swf live=true'
        # Regex Patterns
        self.unapwd_regex = '<h3 align="left">Welcome,<b><i> (.+?)</i>'
        self.sub_regex = '<a href="http://www.liveonlinefooty.com/watchlive/">(.+?)</a>'
        self.rtmp_regex = '\'streamer\',\'(.+?)\'\)'
        self.playpath_regex = '\'file\',\'(.+?)\'\)'
        self.appurl_regex = 'rtmp://(.+?)/(.+?)\'\)'
        self.urlhash_regex = 'hash=(.+?)&updateIt=true'
        self.schedule_regex = '<div id="mycss.">(.+?)</div>'
        self.match_time_regex = '<td width="100" align="center" valign="middle">(.+?):(.+?)</td>'
        self.match_date_regex = '<td width="100" align="center" valign="middle">(.+?) (.+?) (.+?)</td>'
        self.match_comp_regex = '<td align="left" valign="top"><span class="title">(.+?)</span><br/>(.+?)<br />'
        self.match_chan_regex = '<a href="watchlive/\?channel(.+?).php">(.+?)</a>'
        # Regex Statements
        self.unapwd = re.compile(self.unapwd_regex, re.DOTALL|re.M)
        self.sub = re.compile(self.sub_regex, re.DOTALL|re.M)
        self.rtmp = re.compile(self.rtmp_regex, re.DOTALL|re.M)
        self.playpath = re.compile(self.playpath_regex, re.DOTALL|re.M)
        self.appurl = re.compile(self.appurl_regex, re.DOTALL|re.M)
        self.urlhash = re.compile(self.urlhash_regex, re.DOTALL|re.M)
        self.schedule = re.compile(self.schedule_regex, re.DOTALL|re.M)
        self.matchtime = re.compile(self.match_time_regex, re.DOTALL|re.M)
        self.matchcomp = re.compile(self.match_comp_regex, re.DOTALL|re.M)
        self.matchdate = re.compile(self.match_date_regex)
        self.matchchan = re.compile(self.match_chan_regex, re.DOTALL|re.M)
        
    def build_rtmp_url(self, link, channelurl):
        rtmppath = self.rtmp.search(link).group(1)
        playpath = self.playpath.search(link).group(1)
        appurl = self.appurl.search(link).group(2)
        urlhash = self.urlhash.search(link).group(1)
        rtmpurl = ''.join([rtmppath,
                            ' playpath=', playpath,
                            ' app=', appurl,
                            ' pageURL=', channelurl,
                            '?hash=', urlhash,
                            self.swfurl])
        return rtmpurl

    def get_event_info(self, schedule):
	matchhour = (self.matchtime.search(schedule)).group(1)
	matchmin = (self.matchtime.search(schedule)).group(2)
	matchtitle = (self.matchcomp.search(schedule)).group(1)
	matchcomp = (self.matchcomp.search(schedule)).group(2)
	matchday = (self.matchdate.search(schedule)).group(1)
	matchdate = self.date_from_ordinal((self.matchdate.search(schedule)).group(2))
	matchmonth = (self.matchdate.search(schedule)).group(3)
	matchyear = time.strftime("%y")
#	if match_month > time.strftime('%b'):
#		match_year = str(int(match_year + 1))
	convertedtime = self.convert_to_localtime([matchmonth,
                                                    matchdate,
                                                    matchyear,
                                                    matchhour,
                                                    matchmin])
	eventinfo = ''.join([convertedtime, ' | ', matchtitle])
	return eventinfo, matchtitle

    def date_from_ordinal(self, date):
        date = date[0:-2]
        if len(date) == 1:
            date = '0' + date    
        return date
    
    def date_to_ordinal(self, date):
        if 10 <= date % 100 < 20:
            return str(date) + 'th'
        else:
            return  str(date) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(date % 10, "th")

    def convert_to_localtime(self, slist):
        tc1 = time.strptime(''.join(slist), '%b%d%y%H%M')
	tc2 = time.mktime(tc1)
	tc3 = time.ctime(tc2 - time.timezone)
	tc4 = time.strptime(tc3, '%a %b %d %H:%M:00 %Y')
	orddate = self.date_to_ordinal(tc4.tm_mday)
	tc5 = time.strftime('%H:%M | %a ' + orddate +' %b', tc4)
	return tc5

    def schedules(self, schedulePage):
        __navigator__ = LOF_Navigator.LOF_Navigator()
        for each_event in self.schedule.finditer(schedulePage):
		event_info, match_title = self.get_event_info(each_event.group(0))
		if (self.matchchan.search(each_event.group(0)) == None):
		    # No channel stream has been posted
		    slist = [event_info,' | Coming Soon']
                    isPlayable = 'false'
                    chanId = '0'
                    isFolder=False
                    playUrl = 'empty'
                    mode = '2'
		else:
                    slist = [event_info]
                    isPlayable = 'false'
                    chanId = '0'
                    isFolder=True
                    playUrl = match_title
                    mode = '4'
                __navigator__.add_nav_item(slist, isPlayable, chanId, isFolder, playUrl, mode)
        
    def channel_schedule(self, schedulePage, scraperUrl):
        __navigator__ = LOF_Navigator.LOF_Navigator()
        event_regex = '<span class="title">' + scraperUrl + '(.+?)</td>'
        event = re.compile(event_regex, re.DOTALL|re.M)
        value = event.findall(schedulePage)[0]
	for everyListedChannel in self.matchchan.finditer(value):
            slist = [everyListedChannel.group(2)]
            isPlayable = 'true'
            chanId = everyListedChannel.group(1)
            isFolder=False
            playUrl = urllib.quote_plus(self.channelurl %chanId)
            mode = '5'
            __navigator__.add_nav_item(slist, isPlayable, chanId, isFolder, playUrl, mode)

    def account_check(self, link):
        if self.unapwd.search(link)  == None:
            return False
        else:
            return True

    def subscription_check(self, link):
        if self.sub.search(link) == None:
            return False
        else:
            return True
