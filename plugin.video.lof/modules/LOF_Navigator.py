import os
import sys

import urllib
import urllib2
import cookielib

import xbmcplugin
import xbmcgui
import xbmcaddon

import LOF_Scraper

lof_addon = xbmcaddon.Addon("plugin.video.lof");
__scraper__ = LOF_Scraper.LOF_Scraper()


class LOF_Navigator:

    def __init__(self):
        self.artwork = os.path.join(lof_addon.getAddonInfo('path'),'image')
        self.username=lof_addon.getSetting("username")
        self.password=lof_addon.getSetting("password")
        self.loginData = urllib.urlencode({'amember_login' : self.username,
                                           'amember_pass' : self.password})

    def list_channels(self):
        for i in range (1,17):
            slist = ['Channel ', str(i)]
            isPlayable = 'true'
            chanId = str(i)
            isFolder=False
            playUrl = urllib.quote_plus(__scraper__.channelurl %chanId)
            mode = '5'
            self.add_nav_item(slist, isPlayable, chanId, isFolder, playUrl, mode)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def list_schedule(self):
       	schedulepage = (urllib2.urlopen(__scraper__.scheduleurl)).read()
       	__scraper__.schedules(schedulepage)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def list_channel_schedules(self, url):
       	schedulePage = (urllib2.urlopen(__scraper__.scheduleurl)).read()
       	__scraper__.channel_schedule(schedulePage, url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def play_stream(self, url):
        link = self.login(url)
	rtmpUrl = __scraper__.build_rtmp_url(link, url)
	item = xbmcgui.ListItem(path=rtmpUrl)
        return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    def add_nav_item(self, slist, isPlayable, chanId, isfolder, playUrl, mode):
        label = ''.join(slist)
        listitem = xbmcgui.ListItem(label=label)
        listitem.setInfo('video' , {'title': label})
        listitem.setProperty('IsPlayable', isPlayable)
        listitem.setIconImage(os.path.join(self.artwork, 'ch%s.png' %chanId))
        u=sys.argv[0]+"?url="+ playUrl + "&mode=%s" %mode + "&name="+urllib.quote_plus(label)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=listitem, isFolder=isfolder)

    def login(self, openurl):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.open(__scraper__.loginurl, self.loginData)
        link = opener.open(openurl).read()
        return link

    def settings(self):
        if self.username != '' and self.password != '':
            link = self.login(__scraper__.memberurl)
            if (__scraper__.account_check(link) == False):
                self.check_settings('-- Your username and/or password is incorrect. --')
            if (__scraper__.subscription_check(link) == False):
                self.check_settings('-- You don\'t have a valid subscription. --')
            else:
                self.menu()
        else:
            self.check_settings('-- Settings not defined or there is a problem.  Please check your settings. --')

    def check_settings(self, error_string):
	u=sys.argv[0]+"?url=Settings&mode=3"
	listfolder = xbmcgui.ListItem(error_string)
	listfolder.setInfo('video', {'Title': 'Settings not defined or there is a problem.  Please check your settings.'})
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def menu(self):
	u=sys.argv[0]+"?url=Channels&mode=1"
	listfolder = xbmcgui.ListItem('Channels')
	listfolder.setInfo('video', {'Title': 'Channels'})
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)

	u=sys.argv[0]+"?url=Schedule&mode=2"
	listfolder = xbmcgui.ListItem('Schedule')
	listfolder.setInfo('video', {'Title': 'Schedule'})
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)
  
	u=sys.argv[0]+"?url=Settings&mode=3"
	listfolder = xbmcgui.ListItem('Settings')
	listfolder.setInfo('video', {'Title': 'Settings'})
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)

	xbmcplugin.endOfDirectory(int(sys.argv[1]))
