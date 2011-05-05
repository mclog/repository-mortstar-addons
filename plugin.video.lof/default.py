#XBMC liveonlinefooty.com Plugin
#
#Copyright (C) 2011  mclog and myksterx
#Official Development Thread - http://forum.xbmc.org/showthread.php?t=97494
#Official Release Thread - http://forum.xbmc.org/showthread.php?p=776481#post776481
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import sys

import urllib
import urllib2
import cookielib

import re
import time

import xbmcgui
import xbmcplugin
import xbmcaddon

lof_addon = xbmcaddon.Addon("plugin.video.lof");
artwork = os.path.join([lof_addon.getAddonInfo('path'),'image'])

from modules import LOF_Scraper
from modules import LOF_Navigator

__scraper__ = LOF_Scraper.LOF_Scraper()
__navigator__ = LOF_Navigator.LOF_Navigator()

username=lof_addon.getSetting("username")
password=lof_addon.getSetting("password")

#Define Settings

def settings():
    if lof_addon.getSetting("username") != '' and lof_addon.getSetting("password") != '':
        link = Login()
        # Check Username and Password
        if ((re.search(__scraper__.unapwd_regex, link)) == None):
            # Incorrect UserName and/or Password
            check_settings('-- Your username and/or password is incorrect. --')
        # Check Subscription
        if ((re.search(__scraper__.sub_regex, link)) == None):
            # Invalid Subscription
            check_settings('-- You don\'t have a valid subscription. --')
        else:
            # Valid Subscription
            menu()
    else:
        check_settings('-- Settings not defined or there is a problem.  Please check your settings. --')
  
#Index
def menu():

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

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

def check_settings(error_string):

    u=sys.argv[0]+"?url=Settings&mode=3"
    listfolder = xbmcgui.ListItem(error_string)
    listfolder.setInfo('video', {'Title': 'Settings not defined or there is a problem.  Please check your settings.'})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)

    u=sys.argv[0]+"?url=Settings&mode=3"
    listfolder = xbmcgui.ListItem('Settings')
    listfolder.setInfo('video', {'Title': 'Settings'})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Login():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'amember_login' : username, 'amember_pass' : password})
    opener.open(__scraper__.loginurl, login_data)
    link = opener.open(__scraper__.memberurl).read()
    return link

#main program

params=get_params()
url=None
mode=None
try:
    url=urllib.unquote_plus(params["url"])
    title=urllib.unquote_plus(params["title"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

if mode==None or url==None or len(url)<1:
    settings()
elif mode==1:
    __navigator__.list_channels()
elif mode==2:
    __navigator__.list_schedule()
elif mode==3:
    lof_addon.openSettings(url=sys.argv[0])
elif mode==4:
    __navigator__.list_channel_schedules(url)
elif mode==5:
    __navigator__.play_stream(url)
