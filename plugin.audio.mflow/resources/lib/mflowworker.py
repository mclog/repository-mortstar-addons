#by Sam Price
import xbmc
import xbmcplugin
import xbmcgui
import dircache
import fnmatch
import urllib
import simplejson
import sys


import os

class creator:
	_pluginId = 0
	_pluginName = ''


	
	def __init__(self, pluginId, pluginName):
		self._pluginId = pluginId
		self._pluginName = pluginName
		self.userid=""
		self.sessionid=""
		self.take=str(xbmcplugin.getSetting(int(sys.argv[1]),"itemlimit"))
		baseDir = os.getcwd()
		resDir = xbmc.translatePath(os.path.join(baseDir, 'resources'))
		self.discImg=xbmc.translatePath(os.path.join(resDir,"disc.png"))
		self.hashImg=xbmc.translatePath(os.path.join(resDir, "hashtag.png"))
		self.noteImg=xbmc.translatePath(os.path.join(resDir, "mflow.png"))
		self.searchImg=xbmc.translatePath(os.path.join(resDir,"search.png"))
		self.urlJar=xbmc.translatePath(os.path.join(resDir,"urljar"))
		self.itemsJar=xbmc.translatePath(os.path.join(resDir,"itemsjar"))
		self.useridJar=xbmc.translatePath(os.path.join(resDir,"useridjar"))
		self.sessionidJar=xbmc.translatePath(os.path.join(resDir,"sessionidjar"))
		
		


	

	def albumtracks(self,albumurn):
		URL=u"http://ws.mflow.com/DigitalDistribution.ContentCatalogue.Host.WebService/Public/Json/SyncReply/GetContent?ContentUrns="+albumurn
		result=simplejson.load(urllib.urlopen(URL))
		return result['Albums'][0]['Tracks']
	
	def mflowartistsearch(self,query):
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/JSON/SyncReply/SearchArtistsAndLabels?Query="+urllib.quote_plus(query.encode('utf-8','ignore'))+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		if result['ArtistsTotalCount']>0:
			return result['Artists']
		else:
			return ''

	def mflow(self): 
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/GetRecentUserFlows"
		result=simplejson.load(urllib.urlopen(URL))
		return result["Flows"]

	def mflowhashflows(self,query):
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/SearchFlows?HashTags="+query+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		if result["FlowPostsTotalCount"]>0:
			return result["FlowPosts"]
		else:
			return ''
		
	def mflowuserflows(self,sessionid,userid):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/SearchFlowPosts?UserId="+userid+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		return result["Posts"]


	def mflowfavouriteuserflows(self,sessionid,userid):
		if int(self.take)>100:
			take="100"
		else: 
			take=str(self.take)
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetFavouriteUserFlows?UserId="+userid+"&PreviewUserId="+userid+"&Take="+take
		result=simplejson.load(urllib.urlopen(URL))
		return result["Flows"]

	def mflowfavouritehashflows(self,sessionid,userid):

		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetFavouriteHashTagsPage?UserId="+userid+"&PreviewUserId="+userid+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		return result["Flows"]





	def mflowtracksearch(self,query):
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/Search?&SearchProfileType=Track&Query="+urllib.quote_plus(query.encode('utf-8','ignore'))+"&TakeTracks="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		if result['TracksTotalCount']>0:
			return result['Tracks']
		else:
			return ''

	def mflowalbumsearch(self,query):
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/SearchAlbums?Query="+urllib.quote_plus(query.encode('utf-8','ignore'))+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		if result['AlbumsTotalCount']>0:
			return result['Albums']
		else:
			return ''

	def mflowlogin(self, username, password):
		self.userid=""
		self.sessionid=""
		URL=u"https://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetLoginAuth?UserName="+username+"&Password="+password
		result=simplejson.load(urllib.urlopen(URL))
		if result["PublicSessionId"]!="00000000-0000-0000-0000-000000000000":
		 self.userid=result["UserId"]
		 self.sessionid=result["PublicSessionId"]
		 dialog = xbmcgui.Dialog()
                 dialog.ok("Success", "Logged in to Mflow")
		 sessionidjar = open(self.sessionidJar, 'w')
		 useridjar=open(self.useridJar, 'w')
		 simplejson.dump(self.userid, useridjar)
		 simplejson.dump(self.sessionid,sessionidjar) 
		 return [self.userid,self.sessionid]
		else:
		 dialog=xbmcgui.Dialog()
	         dialog.ok("Failed", "Couldn't log in to Mflow")
                 return 0

	def mflowtagsget(self):
		import datetime
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/GetTrendingHashTags?Take=50&OnOrBefore="+datetime.date.isoformat(datetime.datetime.now())
		result=simplejson.load(urllib.urlopen(URL))
		return result["TrendingHashTags"]

	def mflowalbumlatest(self):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/JSON/SyncReply/GetHomePage"
		result=simplejson.load(urllib.urlopen(URL))
		return result['LatestContent']['Albums']

	def mflowtracktag(self, tag):
		import datetime
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/SearchFlows?HashTags="+tag+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		if result["FlowPostsTotalCount"]>0:
			return result['FlowPosts']
		else:
			return ""

	def mflowtrackhash(self):
		import datetime
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/SearchFlows?After="+datetime.date.isoformat(datetime.datetime.now())+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		return result['FlowPosts']


	def mflowplaylistsget(self,sessionid,userid):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetUserPlaylists?SessionId="+sessionid+"&UserId="+userid+"&PlaylistUserId="+userid
		result=simplejson.load(urllib.urlopen(URL))
		if result["TotalCount"]>0:
			return result["UserPlaylists"]
		else:
			return 0

	def mflowtracklatest(self):
		import datetime
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/SearchFlows?After="+datetime.date.isoformat(datetime.datetime.now())+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		return result['FlowPosts']	

	def mflowalbumpopular(self):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/JSON/SyncReply/GetHomePage?Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		return result['MostFlowedContent']['Albums']


	def mflowtags(self, results):
		listing=[]
		for res in results:
			label=res['Name']
			uri=u"plugin://plugin.audio.mflow?action=viewtag:"+urllib.quote_plus(label.encode('utf-8','ignore'))
			#art="http://fs.mflow.com/"+res["RelativeArtistArtPath"]
			listing.append([label,uri])
		return listing

	def mflowplaylists(self, results, sessionid, userid):
		listing=[]
		for res in results:
			label=res['Name']
			uri=u"plugin://plugin.audio.mflow?action=viewplaylist:"+str(res["Id"])+":"+str(sessionid)+":"+str(userid)
			#art="http://fs.mflow.com/"+res["RelativeArtistArtPath"]
			listing.append([label,uri])
		return listing

	def playlistflows(self, id, sessionid,userid):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetUserPlaylistFlows?UserPlaylistId="+str(id)+"&SessionId="+str(sessionid)+"&UserId="+str(userid)
		result=simplejson.load(urllib.urlopen(URL))
		listing=[]	
		for res in result["PlaylistFlows"]:
			listing.append(res["Flow"])
		return listing
		

	def mflowartist(self,results):
		listing=[]
		for res in results:
			label=res['ArtistName']
			uri=u"plugin://plugin.audio.mflow?action=artistview:"+urllib.quote_plus(label.encode('utf-8','ignore'))
			listing.append([label,uri])
		return listing

	def mflowartistget(self,name):
		URL=u"http://ws.mflow.com/DigitalDistribution.ContentCatalogue.Host.WebService/Public/Json/SyncReply/GetArtistView?ArtistName="+name
		result=simplejson.load(urllib.urlopen(URL))
		return result

	def mflowartistgetalbums(self,name):
		URL=u"http://ws.mflow.com/DigitalDistribution.ContentCatalogue.Host.WebService/Public/Json/SyncReply/GetArtistView?ArtistName="+name
		result=simplejson.load(urllib.urlopen(URL))
		if result['Artist']["AlbumsTotal"]>0:
			return result['Artist']["Albums"]
		else:
			return ''


	def mflowartistview(self,name):
		result=self.mflowartistget(name)
		albums=[]
		tracks=[]
		if result['Artist']["AlbumsTotal"]>0:
			albums=result['Artist']["Albums"]
		if result['Artist']["TracksTotal"]>0:
			tracks=result["Artist"]["Tracks"]
		
		count=1
		toppath=u"http://fs.mflow.com/"
		listing=[]
		albumlisting=[]
		for track in tracks:
				unavailable=0
				res=track
				try:
					uri=toppath+res['RelativePreviewPath']
				except:
					unavailable=1
				title=res['Title']
				artist=res['ArtistName']
				album=res['AlbumName']
				urn=res['TrackUrn']
				try:
					art=toppath+res['RelativeCoverArtPath']
				except:
					art=self.noteImg
				label=title+" - " +album+ " - "+artist
				duration = res["DurationMs"]
				duration=duration/1000
				if unavailable==0:
					listing.append([label,uri, title, artist,album, art, duration, urn])
		return [albums,listing]

	def mflowflow(self, results):
		toppath="http://fs.mflow.com/"
		listing=[]
		filteredresults=self.removeDuplicates(results)
		for flow in filteredresults:
                        if "RelativeOggPreviewPath" in flow:
				uri=toppath+flow["RelativeOggPreviewPath"]
			else: 
				uri=toppath+flow["PreviewAssetPath"]
			
			title=flow["TrackName"]
			album=flow["AlbumName"]
			artist=flow["ArtistName"]
			urn=flow["TrackUrn"]
			if "RelativeAlbumImagePath" in flow:
				flowimg=toppath+flow["RelativeAlbumImagePath"]

			else:
				try:
					flowimg=toppath+flow["ImageAssetPath"]
					
				except:
					art=self.noteImg
			label=title+" - " + album+ " - " + artist
			listing.append([label,uri, title, artist,album,flowimg, urn])
		return listing
	
	def mflowtrack(self,results, query):
		toppath="http://fs.mflow.com/"
		filteredresults=self.removeDuplicates(results)
		listing=[]
		for res in filteredresults:
				uri=toppath+res['RelativePreviewPath']	
				title=res['Title']
				artist=res['ArtistName']
				album=res['AlbumName']
				try:
					art=toppath+res['RelativeCoverArtPath']
				except:
					art=self.noteImg

				label=title+" - " +album+ " - "+artist
				trackno=res["SequenceNumber"]
				urn=res["TrackUrn"]
				duration = res["DurationMs"]
				duration=duration/1000

				if query=="xalbumsongsx":
					listing.append([label,uri, title, artist,album,art,duration, trackno, urn])
				else:
					listing.append([label,uri, title, artist,album, art, duration, urn])
		
		return listing

	def removeDuplicates(self,trackList):
		urns = []
		newTrackList = []
		for track in trackList:
			if(not (track["TrackUrn"] in urns)):
				urns.append(track["TrackUrn"])
				newTrackList.append(track)
		return newTrackList
	
class sender:
	_pluginId = 0
	def __init__(self, pluginId):
		self._pluginId = pluginId
		#self.thumbDirName = 'thumb'
		#self.thumbDir = os.path.join('special://masterprofile/addon_data/', os.path.basename(os.getcwd()), self.thumbDirName)
		_id='plugin.audio.mflow'
		baseDir = os.getcwd()
		resDir = xbmc.translatePath(os.path.join(baseDir, 'resources'))
		self.discImg=xbmc.translatePath(os.path.join(resDir,"disc.png"))
		self.hashImg=xbmc.translatePath(os.path.join(resDir, "hashtag.png"))
		self.noteImg=xbmc.translatePath(os.path.join(resDir, "mflow.png"))
		self.searchImg=xbmc.translatePath(os.path.join(resDir,"search.png"))
		self.urlJar=xbmc.translatePath(os.path.join(resDir,"urljar"))
		self.itemsJar=xbmc.translatePath(os.path.join(resDir,"itemsjar"))
		self.useridJar=xbmc.translatePath(os.path.join(resDir,"useridjar"))
		self.sessionidJar=xbmc.translatePath(os.path.join(resDir,"sessionidjar"))
		
		
	def artistoptions(self,artist):
		for item in ["Albums", "Tracks"]:
			listItem=xbmcgui.ListItem(item)
			listItem.setInfo( type="music", infoLabels={ "Title": item } )
			xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action=Artist"+item+":"+artist,listItem, isFolder=True)
			
	

	def userfolders(self, sessionid="", userid=""):

		if sessionid!="":
			for item in ["Your Playlists", "Your Flows", "Favourite User Flows", "Favourite Tag Flows"]:
				listItem=xbmcgui.ListItem(item,iconImage=self.noteImg, thumbnailImage=self.noteImg)
				listItem.setInfo( type="music", infoLabels={ "Title": item } )
				xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action="+item+":"+sessionid+":"+userid,listItem, isFolder=True)
		else:
			listItem=xbmcgui.ListItem("Login",iconImage=self.noteImg, thumbnailImage=self.noteImg)
			xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action=Login",listItem, isFolder=True)

		for item in ["Search Artists", "Search Albums", "Search Tracks"]:
			listItem=xbmcgui.ListItem(item,iconImage=self.searchImg, thumbnailImage=self.searchImg)
			listItem.setInfo( type="music", infoLabels={ "Title": item } )
			xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action="+item,listItem, isFolder=True)
		for item in ["Latest Albums","Most Flowed Albums"]:
			listItem=xbmcgui.ListItem(item,iconImage=self.discImg, thumbnailImage=self.discImg)
			listItem.setInfo( type="music", infoLabels={ "Title": item } )
			xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action="+item,listItem, isFolder=True)
		for item in ["Latest Track Flows", "Trending Tags", "Enter a Tag"]:
			listItem=xbmcgui.ListItem(item,iconImage=self.hashImg, thumbnailImage=self.hashImg)
			listItem.setInfo( type="music", infoLabels={ "Title": item } )
			xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action="+item,listItem, isFolder=True)
				
			

	def sendartists(self,listing): 
		for artist in listing: 
			listItem=xbmcgui.ListItem(artist[0])
			xbmcplugin.addDirectoryItem(self._pluginId, artist[1], listItem, isFolder=True)


	def sendplaylists(self,listing,userid,sessionid):
		for playlist in listing:
			listItem=xbmcgui.ListItem(listing["Name"])
			xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action=playlistflows:"+str(listing["Id"])+":"+sessionid+":"+userid,listItem, isFolder=True)

	def sendalbums(self,listing):
		for album in listing:
			title = album["AlbumName"]+" - "+album["ArtistName"]
			art="http://fs.mflow.com/"+album["RelativeCoverArtPath"]
			albumUrn=album["AlbumUrn"]
			listItem=xbmcgui.ListItem(title, iconImage=art, thumbnailImage=art)
			xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action=albumsongs:"+str(albumUrn),listItem, isFolder=True)
	

		
	def send(self,listing):
#create listing items
		saveitems=[]
		urls=[]
		playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
		existinglength=playlist.size()
		newlength=len(listing)
                #playlist.clear()
		offset=0
		for item in listing:
			listItem = xbmcgui.ListItem(item[0], iconImage=item[5], thumbnailImage=item[5])
			url="plugin://plugin.audio.mflow?action=playplaylist:"+str(offset)+":"+str(existinglength)+":"+str(newlength)+":"+item[1]
			listItem.setProperty('mimetype', 'audio/ogg')
			listItem.setProperty('title', item[2])
			listItem.setProperty('artist', item[3])
			listItem.setProperty('album', item[4])
			#duration
			#listItem.setProperty('IsPlayable', 'true')
			if len(item)==9:
				listItem.setProperty('tracknumber', str(item[7]))
			#if item[5]!="":
			#	if self.getcover(item[5])==1:	
			#		listItem.setThumbnailImage(self.tmppath)
			if len(item)==9:
				listItem.setInfo( type="music", infoLabels={ "title": item[2], "album": item[4], "artist": 
item[3],"tracknumber": item[7], "duration": int(item[6])})
				urn=item[8]
			elif len(item)==8:
				listItem.setInfo( type="music", infoLabels={ "title": item[2], "album": item[4], "artist": 
item[3], "duration": int(item[6])})
				urn=item[7]
			else:
				listItem.setInfo( type="music", infoLabels={ "title": item[2], "album": item[4], "artist": 
item[3]})
				urn=item[6]
			try:
				sessionidjar = open(self.sessionidJar, 'r')
				useridjar=open(self.useridJar, 'r')
				sessionid = simplejson.load(sessionidjar)
				userid=simplejson.load(useridjar)
			except:
				sessionid=""
				userid=""
			if sessionid!="" and userid!="":
				listItem.addContextMenuItems([("Flow this song","XBMC.RunPlugin(plugin://plugin.audio.mflow/?action=flowsong:"+urn+":"+userid+":"+sessionid+")")])
			#listItem.addContextMenuItems([("Play all","playlist.playoffset(MUSIC , 0)")])
			print str(urn)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),url,listItem, isFolder=False)
			
			if existinglength==0: 
				playlist.add(item[1], listItem)
			else:
				urls.append(item[1])
				saveitems.append(listItem)
			
				
			offset=offset+1
		if existinglength!=0:
			urljar = open(self.urlJar, 'w')
			itemsjar=open(self.itemsJar, 'w')
			simplejson.dump(urls, urljar)
			simplejson.dump(listing,itemsjar) 
			urljar.close()
			itemsjar.close()
			
		xbmcplugin.setContent(int(sys.argv[1]), 'songs')
		#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, items[0])
		
		
		

