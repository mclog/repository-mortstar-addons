"""
    Script for generating smart playlists based on a seeding track and last.fm api
	Created by: ErlendSB
"""

import os
import random
import httplib, urllib, urllib2
import sys, time
import xbmc, xbmcgui, xbmcaddon
from urllib import quote_plus, unquote_plus
import re
from os.path import exists
from os import remove


class MyPlayer( xbmc.Player ) :
	countFoundTracks = 0
	foundTracks = []
	currentSeedingTrack = 0
	firstRun = 0
	SCRIPT_NAME = "LAST.FM Playlist Generator"

	
	__settings__ = xbmcaddon.Addon(id='script.lastfmplaylistgeneratorPM')
	apiPath = "http://ws.audioscrobbler.com/2.0/?api_key=71e468a84c1f40d4991ddccc46e40f1b"
	
	def __init__ ( self ):
		xbmc.Player.__init__( self )
		xbmc.PlayList(0).clear()
		self.firstRun = 1
		BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
		process = os.path.join( BASE_RESOURCE_PATH , "pm.pid")
		removeauto('lastfmplaylistgeneratorpm')
		addauto("if os.path.exists('" + os.path.normpath(process).replace('\\','\\\\') + "'):#lastfmplaylistgeneratorpm\n\tos.remove('" + os.path.normpath(process).replace('\\','\\\\') + "')","lastfmplaylistgeneratorpm")
		xbmc.executebuiltin("Notification(" + self.SCRIPT_NAME+",Start by playing a song)")
		#print "init MyPlayer"
	
	def onPlayBackStarted(self):
		print "onPlayBackStarted"
		xbmc.sleep(2000)
		if xbmc.Player().isPlayingAudio() == True:
			currentlyPlayingTitle = xbmc.Player().getMusicInfoTag().getTitle()
			print currentlyPlayingTitle + " started playing"
			currentlyPlayingArtist = xbmc.Player().getMusicInfoTag().getArtist()
			self.countFoundTracks = 0
			#self.foundTracks = []
			if (self.firstRun == 1):
				self.firstRun = 0
				#print "firstRun - clearing playlist"
				xbmc.PlayList(0).clear()
				xbmc.executebuiltin('XBMC.ActivateWindow(10500)')
				xbmc.PlayList(0).add(url= xbmc.Player().getMusicInfoTag().getURL())
			self.foundTracks += [currentlyPlayingTitle + '|' + currentlyPlayingArtist]
			#print "Start looking for similar tracks"
			self.fetch_similarTracks(currentlyPlayingTitle,currentlyPlayingArtist)
	
	def fetch_similarTracks( self, currentlyPlayingTitle, currentlyPlayingArtist ):
		apiMethod = "&method=track.getsimilar"

		# The url in which to use
		Base_URL = self.apiPath + apiMethod + "&artist=" + urllib.quote_plus(currentlyPlayingArtist) + "&track=" + urllib.quote_plus(currentlyPlayingTitle)
		#print Base_URL
		WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
		WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
		WebSock.close()                     # Closes connection to url

		xbmc.executehttpapi("setresponseformat(openRecordSet;<recordset>;closeRecordSet;</recordset>;openRecord;<record>;closeRecord;</record>;openField;<field>;closeField;</field>)");

		similarTracks = re.findall("<track>.+?<name>(.+?)</name>.+?<artist>.+?<name>(.+?)</name>.+?</artist>.+?</track>", WebHTML, re.DOTALL )
		random.shuffle(similarTracks)
		countTracks = len(similarTracks)
		#print "Count: " + str(countTracks)
		for similarTrackName, similarArtistName in similarTracks:
			#print "Looking for: " + similarTrackName + " - " + similarArtistName
			similarTrackName = similarTrackName.replace("+"," ").replace("("," ").replace(")"," ").replace("&quot","'").replace("'","''").replace("&amp;","and")
			similarArtistName = similarArtistName.replace("+"," ").replace("("," ").replace(")"," ").replace("&quot","'").replace("'","''").replace("&amp;","and")
			sql_music = "select strTitle, strArtist, strAlbum, strPath, strFileName from songview where strTitle LIKE '%%" + similarTrackName + "%%' and strArtist LIKE '%%" + similarArtistName + "%%' order by random() limit 1"
			music_xml = xbmc.executehttpapi( "QueryMusicDatabase(%s)" % quote_plus( sql_music ), )
			# separate the records
			records = re.findall( "<record>(.+?)</record>", music_xml, re.DOTALL )
			for count, item in enumerate( records ):
				# separate individual fields
				fields = re.findall( "<field>(.*?)</field>", item, re.DOTALL )
				artist = fields[1]
				trackTitle = fields[0]
				trackPath = fields[3] + fields[4]
				print "Found: " + trackTitle + " by: " + artist
				if (similarTrackName + '|' + similarArtistName not in self.foundTracks and artist != currentlyPlayingArtist):
					listitem = xbmcgui.ListItem(trackTitle)
					cache_name = xbmc.getCacheThumbName( artist )
					fanart = "special://profile/Thumbnails/Music/%s/%s" % ( "Fanart", cache_name, )
					listitem.setProperty('fanart_image',fanart)
					print "Fanart:%s" % fanart
					xbmc.PlayList(0).add(url=trackPath, listitem=listitem)
					xbmc.executebuiltin("Container.Refresh")
					#xbmc.executebuiltin( "AddToPlayList(" + trackPath + ";0)")
					self.countFoundTracks += 1
					self.foundTracks += [similarTrackName + '|' + similarArtistName]
			if (self.countFoundTracks >= 3):
				break
			
		if (self.countFoundTracks == 0):
			time.sleep(3)
			#self.firstRun = 1
			print "None found"
			xbmc.executebuiltin("Notification(" + self.SCRIPT_NAME+",No similar tracks were found)")
			return False
			
		xbmc.executebuiltin('SetCurrentPlaylist(0)')

def addauto(newentry, scriptcode):
	autoexecfile = "special://masterprofile/autoexec.py"
	if exists(autoexecfile):
		fh = open(autoexecfile)
		lines = []
		for line in fh.readlines():
			lines.append(line)
		lines.append("import time" + "#" + scriptcode + "\n")
		lines.append("time.sleep(2)" + "#" + scriptcode + "\n")
		lines.append(newentry + "#" + scriptcode + "\n")
		fh.close()
		f = open(autoexecfile, "w")
		if not "import xbmc\n" in lines:
			f.write("import xbmc" + "#" + scriptcode + "\n")
		if not "import os\n" in lines:
			f.write("import os" + "#" + scriptcode + "\n")
		f.writelines(lines)
		f.close()
	else:
		f = open(autoexecfile, "w")
		f.write("import xbmc" + "#" + scriptcode + "\n")
		f.write(newentry + "#" + scriptcode + "\n")
		f.close()

def removeauto(scriptcode):
	autoexecfile = "special://masterprofile/autoexec.py"
	if exists(autoexecfile):
		fh = open(autoexecfile)
		lines = [ line for line in fh if not line.strip().endswith("#" + scriptcode) ]
		fh.close()
		f = open(autoexecfile, "w")
		f.writelines(lines)
		f.close()
		
BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )

process = os.path.join( BASE_RESOURCE_PATH , "pm.pid")
p=MyPlayer()
while(1):
	if os.path.exists(process):
		if (xbmc.abortRequested):
			os.remove(process)
			print "deleting pid"
		xbmc.sleep(500)
	else:
		break