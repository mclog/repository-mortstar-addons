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
import xbmcaddon
from modules import FSS_Navigator

fss_addon = xbmcaddon.Addon("plugin.video.fss");
__navigator__ = FSS_Navigator.FSS_Navigator()


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
    __navigator__.settings()
elif mode==1:
    __navigator__.list_channels()
elif mode==2:
    __navigator__.list_schedule()
elif mode==3:
    fss_addon.openSettings(url=sys.argv[0])
elif mode==4:
    __navigator__.list_channel_schedules(url)
elif mode==5:
    __navigator__.play_stream(url)
