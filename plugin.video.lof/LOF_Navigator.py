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
        self.cookie = []
        self.username = lof_addon.getSetting('username')
        self.password=lof_addon.getSetting('password')
        self.artwork = os.path.join(lof_addon.getAddonInfo('path'),'image')
        self.match_chan_regex = __scraper__.match_chan_regex
        self.matchchan = re.compile(self.match_chan_regex, re.DOTALL|re.M)


    def list_channels(self):
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'amember_login' : self.username, 'amember_pass' : self.password})
	opener.open(__scraper__.loginurl, login_data)
	for i in range (1,17):
		resp = opener.open(__scraper__.channelurl %(i))
		link = resp.read()
		rtmp_url = __scraper__.build_rtmp_url(link, __scraper__.channelurl %(i))
		slist = ['Channel ', str(i)]
		label = ''.join(slist)
		listitem = xbmcgui.ListItem(label=label)
		listitem.setInfo('video' , {'title': label})
		listitem.setIconImage(os.path.join(self.artwork, 'ch%s.png' %i))
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=rtmp_url,listitem=listitem)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def list_schedule(self):
	schedulepage = (urllib2.urlopen(__scraper__.scheduleurl)).read()
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'amember_login' : self.username, 'amember_pass' : self.password})
	opener.open(__scraper__.loginurl, login_data)
	
	for each_event in __scraper__.schedule.finditer(schedulepage):
		event_info = __scraper__.get_event_info(each_event.group(0))
		if (__scraper__.matchchan.search(each_event.group(0)) == None):
			# No channel stream has been posted
			slist = [event_info,' [N/A]']
			label = ''.join(slist)
			listitem = xbmcgui.ListItem(label=label)
			listitem.setInfo('video' , {'title': label})
			listitem.setIconImage(os.path.join(self.artwork, 'ch0.png'))
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url='z', listitem=listitem)
		else:
			for every_listed_channel in __scraper__.matchchan.finditer(each_event.group(0)):
				chanid = every_listed_channel.group(1)
				chanlbl = every_listed_channel.group(2)
				link = (opener.open(__scraper__.channelurl %(chanid))).read()
				rtmp_url = __scraper__.build_rtmp_url(link, __scraper__.channelurl %(chanid))
				slist = [event_info,'  [CH',chanid,']']
				label = ''.join(slist)
				listitem = xbmcgui.ListItem(label=label)
				listitem.setInfo('video' , {'title': label})
				listitem.setIconImage(os.path.join(self.artwork, 'ch%s.png' %(chanid)))
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=rtmp_url, listitem=listitem)

	xbmcplugin.endOfDirectory(int(sys.argv[1]))
