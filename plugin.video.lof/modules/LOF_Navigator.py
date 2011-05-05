import os
import sys

import urllib
import urllib2
import cookielib
import re

import xbmcplugin
import xbmcgui
import xbmcaddon

lof_addon = xbmcaddon.Addon("plugin.video.lof");

import LOF_Scraper

__scraper__ = LOF_Scraper.LOF_Scraper()

class LOF_Navigator:


    def __init__(self):
        self.artwork = os.path.join(lof_addon.getAddonInfo('path'),'image')
        self.match_chan_regex = __scraper__.match_chan_regex
        self.matchchan = re.compile(self.match_chan_regex, re.DOTALL|re.M)
        self.username=lof_addon.getSetting("username")
        self.password=lof_addon.getSetting("password")

    def list_channels(self):
        for i in range (1,17):
		slist = ['Channel ', str(i)]
		label = ''.join(slist)
		listitem = xbmcgui.ListItem(label=label)
		listitem.setInfo('video' , {'title': label})
		listitem.setProperty('IsPlayable', 'true')
		listitem.setIconImage(os.path.join(self.artwork, 'ch%s.png' %i))
                u=sys.argv[0]+"?url="+urllib.quote_plus(__scraper__.channelurl %i)+"&mode=5"+"&name="+urllib.quote_plus(label)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=listitem)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def list_schedule(self):
       	schedulepage = (urllib2.urlopen(__scraper__.scheduleurl)).read()
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'amember_login' : self.username, 'amember_pass' : self.password})
	opener.open(__scraper__.loginurl, login_data)
	for each_event in __scraper__.schedule.finditer(schedulepage):
		event_info, match_title = __scraper__.get_event_info(each_event.group(0))
		if (__scraper__.matchchan.search(each_event.group(0)) == None):
			# No channel stream has been posted
			slist = [event_info,' | Coming Soon']
			label = ''.join(slist)
			listitem = xbmcgui.ListItem(label=label)
			listitem.setInfo('video' , {'title': label})
			listitem.setIconImage(os.path.join(self.artwork, 'ch0.png'))
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url='', listitem=listitem)
		else:
			label = event_info
			listitem = xbmcgui.ListItem(label=label)
			listitem.setInfo('video' , {'title': label})
			listitem.setIconImage(os.path.join(self.artwork, 'ch0.png'))
	                u=sys.argv[0]+"?url="+match_title+"&mode=4"+"&name="+urllib.quote_plus(label)
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=listitem, isFolder=True)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def list_channel_schedules(self, url):
       	schedulepage = (urllib2.urlopen(__scraper__.scheduleurl)).read()
        regex = '<span class="title">' + url + '(.+?)</td>'
        value = re.findall(regex, schedulepage)[0]
	for every_listed_channel in __scraper__.matchchan.finditer(value):
	    chanid = every_listed_channel.group(1)
	    chanlbl = every_listed_channel.group(2)
	    slist = ['CH',chanid]
#	    label = ''.join(slist)
            label = chanlbl
	    listitem = xbmcgui.ListItem(label=label)
	    listitem.setInfo('video' , {'title': label})
	    listitem.setIconImage(os.path.join(self.artwork, 'ch%s.png' %chanid))
	    listitem.setProperty('IsPlayable', 'true')
            u=sys.argv[0]+"?url="+urllib.quote_plus(__scraper__.channelurl %(chanid))+"&mode=5"+"&name="+urllib.quote_plus(label)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=listitem)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def play_stream(self,url):
      	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'amember_login' : self.username, 'amember_pass' : self.password})
	opener.open(__scraper__.loginurl, login_data)
        link = opener.open(url).read()
	rtmp_url = __scraper__.build_rtmp_url(link, url)
	item = xbmcgui.ListItem(path=rtmp_url)
        return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
