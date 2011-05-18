#########################################XBMC mFlow plugin by Sam Price##########################

import sys

import xbmcplugin, xbmcgui, xbmc, os, simplejson, urllib
def makeitems(listing):
	items=[]
	for item in listing:
		listItem = xbmcgui.ListItem(item[0], iconImage=item[5], thumbnailImage=item[5])
		listItem.setProperty('mimetype', 'audio/ogg')
		listItem.setProperty('title', item[2])
		listItem.setProperty('artist', item[3])
		listItem.setProperty('album', item[4])
		if len(item)==9:
			listItem.setProperty('tracknumber', str(item[7]))
		if len(item)==9:
			listItem.setInfo( type="music", infoLabels={ "title": item[2], "album": item[4], "artist": 
item[3],"tracknumber": item[7], "duration": int(item[6])})
		elif len(item)==8:
			listItem.setInfo( type="music", infoLabels={ "title": item[2], "album": item[4], "artist": 
item[3], "duration": int(item[6])})
		else:
			listItem.setInfo( type="music", infoLabels={ "title": item[2], "album": item[4], "artist": 
item[3]})
		items.append(listItem)
	return items



sessionid=""
userid=""
cancel=0
_id='plugin.audio.mflow'
doinguserfolders=0
dialog=xbmcgui.Dialog()
baseDir = os.getcwd()
resDir = xbmc.translatePath(os.path.join(baseDir, 'resources'))
urlJarfile=xbmc.translatePath(os.path.join(resDir,"urljar"))
itemsJarfile=xbmc.translatePath(os.path.join(resDir,"itemsjar"))
useridJar=xbmc.translatePath(os.path.join(resDir,"useridjar"))
sessionidJar=xbmc.translatePath(os.path.join(resDir,"sessionidjar"))	

#import worker class - code based on xbmc tutorial script

from resources.lib import mflowworker as worker

_thisPlugin = int(sys.argv[1])

creator = worker.creator(_thisPlugin, _id)

sender = worker.sender(_thisPlugin)

def get_keyboard(default="", heading="", hidden=False):
    kb = xbmc.Keyboard(default, heading, hidden)
    kb.doModal()
    if (kb.isConfirmed()):
       return unicode(kb.getText(), "utf-8")
    return ''
def getparams():


	        """
	        Pick up parameters sent in via command line
	        @return dict list of parameters
	        @thanks Team XBM  & XBMC example code
	        """
	        param=[]
		try:
	        	paramstring=sys.argv[2]
	        except: 
			paramstring=""
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

#

# Step 3 - run the program

#
params=getparams()
try:
  action = params["action"]
except:
  action = None
if action==None:
  try:
	os.remove(useridJar)
	os.remove(sessionidJar)
  except:
	pass
  sender.userfolders()
elif action=="Search Albums":
  query=get_keyboard(default="", heading="Search for Albums")
  #print "Userid:"+userid + " " + sessionid
  if query!='':
       results=creator.mflowalbumsearch(query)
       if results!='':
      	sender.sendalbums(results)
       else: 
	dialog.ok("Error", "No results found")
	cancel=1
  else:
       
       cancel=1

elif action=="Search Artists":
  query=get_keyboard(default="", heading="Search for Artists")
  if query!='':
       results=creator.mflowartistsearch(query)
       if results!='':
	artists=creator.mflowartist(results)
       	sender.sendartists(artists)
       else: 
	dialog.ok("Error", "No results found")
	cancel=1
  else:
       cancel=1

elif action=="Search Tracks":
  query=get_keyboard(default="", heading="Search for tracks")
  if query!='':
       results=creator.mflowtracksearch(query)
       if results!='':
       	sender.send(creator.mflowtrack(results, query))
       else: 
	dialog.ok("Error", "No results found")
	cancel=1
  else:
       cancel=1


elif action=="Playlists":
  sender.send(creator.get())
elif action=="Latest Albums":
	results=creator.mflowalbumlatest()
	if results!="":
	 sender.sendalbums(results)
	else:
	 dialog.ok("Error", "No results found")
	 cancel=1
elif action=="Most Flowed Albums":
	results=creator.mflowalbumpopular()
	if results!="":
	 sender.sendalbums(results)
	else:
	 dialog = xbmcgui.Dialog()
         dialog.ok("Error", "No results found")
	 cancel=1

elif action=="Latest Track Flows":
	results=creator.mflowtracklatest()
	if results!="":
	 sender.send(creator.mflowflow(results))
	else:
	 dialog = xbmcgui.Dialog()
         dialog.ok("Error", "No results found")
	 cancel=1

elif action=="Trending Tags":
	results=creator.mflowtagsget()
	sender.sendartists(creator.mflowtags(results))

elif action=="Login":
	username=xbmcplugin.getSetting(int(sys.argv[1]),"username")
	password=xbmcplugin.getSetting(int(sys.argv[1]),"password")
	if username!="" and password!="":
		auth=creator.mflowlogin(username,password)
	else: 
		dialog.ok("Error", "Username and/or Password not configured")
		auth=""
	if len(auth)==2:
	 userid=auth[0]
	 sessionid=auth[1]
	 print userid
	 print sessionid
	 sender.userfolders(sessionid,userid)
	 doinguserfolders=1
	 
	else:
	 sender.userfolders()

elif "flowsong" in action:
	auth=action.rsplit(":",2)
	userid=auth[1]	
	sessionid=auth[2]
	urn=auth[0].split(":",1)[1]	
	print "urn:"+urn
	print "userid:"+userid
	print "sessionid:"+sessionid
	flowcomment=get_keyboard(default="", heading="Enter comment for flow (optional)")
	flowcomment=flowcomment+" - sent from the mflow xbmc plugin."
	URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/CreateFlowPost?Caption="+urllib.quote_plus(flowcomment.encode('utf-8','ignore'))+"&ContentUrn="+urn+"&UserId="+userid+"&SessionId="+sessionid
	result=simplejson.load(urllib.urlopen(URL))
	if result["ResponseStatus"]["ErrorCode"]==None:
		dialog.ok("XBMC", "Track successfully flowed")
	else:
		dialog.ok("XBMC", "Error flowing track")
		
	
  	

elif "Your Playlists" in action:
	auth=action.split(":",2)
	results=creator.mflowplaylistsget(auth[1],auth[2])
	if results!=0: 
	 sender.sendartists(creator.mflowplaylists(results,auth[1],auth[2]))
	else:
	 cancel=1

elif "Your Flows" in action:
	auth=action.split(":",2)
	results=creator.mflowuserflows(auth[1],auth[2])
	if results!=0: 
	 sender.send(creator.mflowflow(results))
	else:
	 cancel=1

elif "Favourite Tag Flows" in action:
	auth=action.split(":",2)
	results=creator.mflowfavouritehashflows(auth[1],auth[2])
	if results!=0: 
	 sender.send(creator.mflowflow(results))
	else:
	 cancel=1

elif "Favourite User Flows" in action:
	auth=action.split(":",2)
	results=creator.mflowfavouriteuserflows(auth[1],auth[2])
	if results!=0: 
	 sender.send(creator.mflowflow(results))
	else:
	 cancel=1

elif "playplaylist" in action:
	playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
	elements=action.split(":",4)
	offset=int(elements[1])
	existing=int(elements[2])
	new=int(elements[3])
	url=elements[4]
	flag=0
	print elements
	print "playlist size: " +str(playlist.size())
	print "offset: " +str(offset)
	print "existing: "+ str(existing)
	print "new: "+ str(new)
	#change conditional - if files
	if existing>0:
		urljar=""
		itemsjar=""
		try:
			urljar = open(urlJarfile, 'r')
			itemsjar=open(itemsJarfile, 'r')
		except:
			pass
		if urljar!="" and itemsjar!="":
			urls = simplejson.load(urljar)
			listing=simplejson.load(itemsjar)
			items=makeitems(listing)
			urljar.close()
			itemsjar.close()
			os.remove(urlJarfile)
			os.remove(itemsJarfile)
			playlist.clear()
			for url, item in zip(urls, items):
				playlist.add(url,item)	
			
	xbmc.Player().playselected(offset)
	cancel=1

elif "viewtag" in action:
  tag=action.split(":",1)[1]
  results=creator.mflowtracktag(tag)
  if results!="":
   sender.send(creator.mflowflow(results))
  else:
   dialog = xbmcgui.Dialog()
   dialog.ok("Error", "No results found")
   cancel=1

	
elif "artistview" in action:
  artistname=action.split(":",1)[1]
  results=creator.mflowartistview(artistname)
  sender.sendalbums(results[0])
  sender.send(results[1])

elif "albumsongs" in action:
  albumurn=action.split(":",1)[1]
  results=creator.albumtracks(albumurn)
  query="xalbumsongsx"
  sender.send(creator.mflowtrack(results, query))

elif "viewplaylist" in action:
  print "firing"
  id=action.split(":")
  results=creator.playlistflows(id[1],id[2],id[3])
  if results!="":
   sender.send(creator.mflowflow(results))
  else:
   sender.userfolders(id[2],id[3])
   doinguserfolders=1

elif "Enter a Tag" in action: 
	query=get_keyboard(default="", heading="Enter a Tag (including the #)")
  	if query!='':
       	 results=creator.mflowtracktag(query)
         if results!='':
	  sender.send(creator.mflowflow(results))
       	 else: 
	  dialog.ok("Error", "No results found")
	  cancel=1
  	else:
         cancel=1

	
if cancel!=1:
	if doinguserfolders==0:
		xbmcplugin.endOfDirectory(_thisPlugin)
	if doinguserfolders==1:
		xbmcplugin.endOfDirectory(_thisPlugin,updateListing=True)
	doinguserfolders=0

