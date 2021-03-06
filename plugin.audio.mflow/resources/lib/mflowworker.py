#by Sam Price
import xbmc
import xbmcplugin
import xbmcgui
import dircache
import fnmatch
import urllib
import urllib2
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
		URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/SearchFlows?HashTags="+query+"&Take="+self.take+"&DuplicateContentFilter=true"
		result=simplejson.load(urllib.urlopen(URL))
		if result["FlowPostsTotalCount"]>0:
			return result["FlowPosts"]
		else:
			return ''
		
	def mflowuserflows(self,sessionid,userid):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/SearchFlowPosts?UserId="+userid+"&Take="+self.take+"&DuplicateContentFilter=true"
		result=simplejson.load(urllib.urlopen(URL))
		return result["Posts"]


	def mflowfavouriteuserflows(self,sessionid,userid):
		if int(self.take)>100:
			take="100"
		else: 
			take=str(self.take)
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetFavouriteUserFlows?UserId="+userid+"&PreviewUserId="+userid+"&Take="+take+"&DuplicateContentFilter=true"
		result=simplejson.load(urllib.urlopen(URL))
		return result["Flows"]

	def mflowfavouritehashflows(self,sessionid,userid):

		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetFavouriteHashTagsPage?UserId="+userid+"&PreviewUserId="+userid+"&Take="+self.take+"&DuplicateContentFilter=true"
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
		result=simplejson.load(urllib2.urlopen(URL))
		if result["PublicSessionId"]!="00000000-0000-0000-0000-000000000000":
		 self.userid=result["UserId"]
		 print "userid:" +self.userid
		 self.sessionid=result["PublicSessionId"]
		 sessionidjar = open(self.sessionidJar, 'w')
		 useridjar=open(self.useridJar, 'w')
		 simplejson.dump(self.userid, useridjar)
		 simplejson.dump(self.sessionid,sessionidjar) 
		 return [self.userid,self.sessionid]
		else:
                 return 0

	def mflowtagsget(self, userid):
		import datetime
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/json/SyncReply/GetTrendingTags?Take=50&Before="+datetime.date.isoformat(datetime.datetime.now())+"&PreviewUserId="+userid
		print URL
		result=simplejson.load(urllib.urlopen(URL))
		return result["HashTags"]

	def mflowalbumlatest(self):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/JSON/SyncReply/GetHomePage"
		result=simplejson.load(urllib.urlopen(URL))
		return result['LatestContent']['Albums']

	def mflowtracktag(self, tag,userid):
		import datetime
		if self.take<100:
			flowtake=self.take
		else:
			flowtake=100
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/json/SyncReply/GetTagFlows?Tag="+urllib.quote_plus(tag.encode('utf-8','ignore'))+"&Take="+str(flowtake)+"&PreviewUserId="+userid
		print URL
		result=simplejson.load(urllib.urlopen(URL))
		if result["FlowsTotalCount"]>0:
			return result['Flows']
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

	def mflowtrendingplaylistsget(self):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/json/SyncReply/GetDiscoverPlaylists?DiscoverPlaylistType=Trending&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		if result["TotalCount"]>0:
			return result["UserPlaylists"]
		else:
			return 0

	def mflowfollowedplaylistsget(self, userid):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/json/SyncReply/GetDiscoverPlaylists?DiscoverPlaylistType=Following&Take="+self.take+"&UserId="+userid
		result=simplejson.load(urllib.urlopen(URL))
		if result["TotalCount"]>0:
			return result["UserPlaylists"]
		else:
			return 0


	def mflowtracklatest(self,userid):
		import datetime
		if self.take<100:
			flowtake=self.take
		else:
			flowtake=100
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetLiveFlows?AfterDate="+datetime.date.isoformat(datetime.datetime.now())+"&Take="+str(flowtake)+"&PreviewUserId="+userid
		print URL
		#URL=u"http://ws.mflow.com/DigitalDistribution.SearchIndex.Host.WebService/Public/Json/SyncReply/SearchFlows?After="+datetime.date.isoformat(datetime.datetime.now())+"&Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		return result['Flows']	

	def mflowalbumpopular(self):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/JSON/SyncReply/GetHomePage?Take="+self.take
		result=simplejson.load(urllib.urlopen(URL))
		return result['MostFlowedContent']['Albums']


	def mflowtags(self, results, userid):
		listing=[]
		for res in results:
			label=res['Name']
			uri=u"plugin://plugin.audio.mflow?action=viewtag:"+urllib.quote_plus(label.encode('utf-8','ignore'))+":"+userid
			#art="http://fs.mflow.com/"+res["RelativeArtistArtPath"]
			listing.append([label,uri])
		return listing

	def mflowplaylists(self, results, sessionid, userid):
		listing=[]
		for res in results:
			if " pt." in res['Name']:
				label=listing[-1][0]
				jigsaw=listing[-1][1].split(":")
				del jigsaw[0]
				del jigsaw[0]
				sessionid=jigsaw[-1]
				del jigsaw[-1]
				userid=jigsaw[-1]
				del jigsaw[-1]
				uri=u"plugin://plugin.audio.mflow?action=viewplaylists:"
				for pieces in jigsaw:
					uri+=str(pieces)
					uri+=":"
				uri+=str(res["Id"])
				uri+=":"
				uri+=str(userid)
				uri+=":"
				uri+=str(sessionid)
				listing.pop()
				listing.append([label,uri])
			else:
				label=res['Name']
				uri=u"plugin://plugin.audio.mflow?action=viewplaylist:"+str(res["Id"])+":"+str(userid)+":"+str(sessionid)
				#art="http://fs.mflow.com/"+res["RelativeArtistArtPath"]
				listing.append([label,uri])
			print uri
		return listing

	def playlistflows(self, id, userid,sessionid,listing=[]):
		URL=u"http://ws.mflow.com/DigitalDistribution.UserCatalogue.Host.WebService/Public/Json/SyncReply/GetUserPlaylistFlows?UserPlaylistId="+str(id)+"&SessionId="+str(sessionid)+"&UserId="+str(userid)+"&Take="+self.take
		print URL
		result=simplejson.load(urllib.urlopen(URL))
		result=simplejson.load(urllib.urlopen(URL))
		for res in result["PlaylistFlows"]:
			listing.append(res["Flow"])
		print listing
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
		unavailable=0
		for flow in filteredresults:
			uri=""
                        try:
				uri=toppath+flow["RelativeOggPreviewPath"]
			except:
				pass
			if uri=="":
				try:
					uri=toppath+flow["PreviewAssetPath"]
				except:
					unavailable=1
			title=flow["TrackName"]
			album=flow["AlbumName"]
			artist=flow["ArtistName"]
			urn=flow["TrackUrn"]
			flowimg=""
			try:
				flowimg=toppath+flow["RelativeAlbumImagePath"]
			except:	
				pass

			if flowimg=="":
				try:
					flowimg=toppath+flow["ImageAssetPath"]
					
				except:
					art=self.noteImg
			label=title+" - " + album+ " - " + artist
			if unavailable!=1:
				listing.append([label,uri, title, artist,album,flowimg, urn])
		return listing
	
	def mflowtrack(self,results, query):
		toppath="http://fs.mflow.com/"
		filteredresults=self.removeDuplicates(results)
		listing=[]
		for res in filteredresults:
				unavailable=0
				try:
					uri=toppath+res['RelativePreviewPath']
				except:
					unavailable=1	
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
				if unavailable!=1:
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
			for item in ["Your Playlists", "Your Flows", "Favourite User Flows", "Favourite Tag Flows", "Trending Playlists", "Followed Users' Playlists"]:
				listItem=xbmcgui.ListItem(item,iconImage=self.noteImg, thumbnailImage=self.noteImg)
				listItem.setInfo( type="music", infoLabels={ "Title": item } )
				xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action="+item+":"+sessionid+":"+userid,listItem, isFolder=True)
			for item in ["Latest Track Flows","Trending Tags", "Enter a Tag"]:
				listItem=xbmcgui.ListItem(item,iconImage=self.hashImg, thumbnailImage=self.hashImg)
				listItem.setInfo( type="music", infoLabels={ "Title": item } )
				xbmcplugin.addDirectoryItem(self._pluginId,"plugin://plugin.audio.mflow?action="+item+":"+userid,listItem, isFolder=True)
				
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
		
		
		

