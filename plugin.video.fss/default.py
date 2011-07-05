#XBMC flashsportstreams.com Plugin
#
#Copyright (C) 2011  myksterx and mclog
#Official Development Thread - http://forum.xbmc.org/showthread.php?t=100201
#Official Release Thread - http://forum.xbmc.org/showthread.php?t=104820
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

import locale
locale.setlocale(locale.LC_ALL, 'C')

import xbmcgui, urllib, urllib2, cookielib , re, os, xbmcplugin, htmlentitydefs, time, xbmcaddon, md5
fss_addon = xbmcaddon.Addon("plugin.video.fss");

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( fss_addon.getAddonInfo('path'), "resources" ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

from string import split, replace, find
from xml.dom import minidom

#Check Settings
def settings():
  
  if fss_addon.getSetting("username") != '' and fss_addon.getSetting("password") != '':
    
    loginurl='http://www.flashsportstreams.tv/forum/login.php?do=login'
    memberurl='http://www.flashsportstreams.tv/forum/view.php?pg=home&styleid=1'
    login='login'

    username=fss_addon.getSetting("username")
    password=fss_addon.getSetting("password")
    passhash = md5.new(password).hexdigest()
    tempp='b8ca941beeca39c9b47a01e3d700bd34'

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'do' : login, 'url' : memberurl, 'vb_login_md5password' : passhash, 'vb_login_md5password_utf' : passhash, 's' : tempp, 'vb_login_username' : username, 'vb_login_password' : 0})
    opener.open(loginurl, login_data)

    resp = opener.open(memberurl)
    link = resp.read()

    # Define the regex pattern that the username should be found in
    pattern = '<strong>Welcome, (.+?).</strong><br />'
        
    # Write the found username to a parameter
    # perform regex and check if user is logged in
    returnusername = (re.search(pattern, link))
    if (returnusername == None):
      # Username not found
      u=sys.argv[0]+"?url=Settings&mode=3"
      listfolder = xbmcgui.ListItem('-- Your username or password is incorrect. --')
      listfolder.setInfo('video', {'Title': 'Settings not defined or there is a problem.  Please check your settings.'})
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)
      u=sys.argv[0]+"?url=Settings&mode=3"
      listfolder = xbmcgui.ListItem('Settings')
      listfolder.setInfo('video', {'Title': 'Settings'})
      xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, listfolder, isFolder=1)
      xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
    else:
      # Valid Subscription
      menu()
  
#Index
def menu():

  u=sys.argv[0]+"?url=Channels&mode=1"
  listfolder = xbmcgui.ListItem('Channels')
  listfolder.setInfo('video', {'Title': 'Channels'})
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

def listchannels(url):
  channelurl='http://www.flashsportstreams.tv/forum/view.php?pg=vip%s'
  loginurl='http://www.flashsportstreams.tv/forum/login.php?do=login'
  memberurl='http://www.flashsportstreams.tv/forum/view.php?pg=home'
  login='login'

  username=fss_addon.getSetting("username")
  password=fss_addon.getSetting("password")
  passhash = md5.new(password).hexdigest()
  tempp='b8ca941beeca39c9b47a01e3d700bd34'

  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  login_data = urllib.urlencode({'do' : login, 'url' : memberurl, 'vb_login_md5password' : passhash, 'vb_login_md5password_utf' : passhash, 's' : tempp, 'vb_login_username' : username, 'vb_login_password' : 0})
  opener.open(loginurl, login_data)

  for i in range (1,9):
    useurl = channelurl %i
    resp = opener.open(useurl)
    link = resp.read()
    #channelpattern_regex = '<strong>(.+?) - (.+?)</strong>'
    #channelpattern = re.compile(channelpattern_regex, re.DOTALL|re.M)
    #returnchannelinfo = channelpattern.search(link)
    returnchannelinfo = re.search('ViP.+? -? ?(.*)</title>', link).group(1)
    
    embedstring = (re.search('<embed(.+?)</span></span></p>', link)).group(0)
    rtmp_url = (re.search('streamer=(.+?)&amp;type=video',embedstring)).group(1)
    app_url = (re.search('rtmp://(.+?)/(.+?)&amp;type=video',embedstring)).group(2)
    swf_url= (re.search('<embed type="application/x-shockwave-flash" src="(.+?)" width',embedstring)).group(1)
    play_url = (re.search('flashvars="file=(.+?)&amp;streamer',embedstring)).group(1)

    if (returnchannelinfo == None):
      label = 'ViP ' + str(i) + ' - No Schedule Information'
      listitem = xbmcgui.ListItem(label=label, iconImage="DefaultVideo.png")
      listitem.setInfo('video' , {'title': label})
      rtmp_url = rtmp_url + ' ' + 'playpath=' + play_url + ' ' + 'app=' + app_url + ' ' + 'pageURL=' + channelurl + ' swfVfy=true live=true'
      xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=rtmp_url,listitem=listitem)
      rtmp_url = ''
    else:
      label = returnchannelinfo
      listitem = xbmcgui.ListItem(label=label, iconImage="DefaultVideo.png")
      listitem.setInfo('video' , {'title': 'Channel X'})
      rtmp_url = rtmp_url + ' ' + 'playpath=' + play_url + ' ' + 'app=' + app_url + ' ' + 'pageURL=' + channelurl + ' swfVfy=true live=true'
      xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=rtmp_url,listitem=listitem)
      rtmp_url = ''
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
  return url
  
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
        listchannels(url)
elif mode==3:
        fss_addon.openSettings(url=sys.argv[0])
