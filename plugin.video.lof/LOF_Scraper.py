import re
import time

class LOF_Scraper:

    def __init__(self):
        # URL's
        self.baseurl = 'http://www.liveonlinefooty.com/'
        self.channelurl = ''.join([self.baseurl, 'watchlive/channel%s.php'])
        self.loginurl = ''.join([self.baseurl, 'amember/login.php'])
        self.memberurl = ''.join([self.baseurl, 'amember/member.php'])
        self.scheduleurl = ''.join([self.baseurl, 'schedule.php'])
        self.swfurl = ' swfUrl=http://www.livesporton.net/player2.swf live=true'
        # Regex Patterns
        self.unapwd_regex = '<h3 align="left">Welcome,<b><i> (.+?)</i>'
        self.sub_regex = '<a href="http://www.liveonlinefooty.com/watchlive/">(.+?)</a>'
        self.rtmp_regex = '\'streamer\',\'(.+?)\'\)'
        self.playpath_regex = '\'file\',\'(.+?)\'\)'
        self.appurl_regex = 'rtmp://(.+?)/(.+?)\'\)'
        self.schedule_regex = '<div id="mycss.">(.+?)</div>'
        self.match_time_regex = '<td width="100" align="center" valign="middle">(.+?):(.+?)</td>'
        self.match_date_regex = '<td width="100" align="center" valign="middle">(.+?) (.+?) (.+?)</td>'
        self.match_comp_regex = '<td align="left" valign="top"><span class="title">(.+?)</span><br/>(.+?)<br />'
        self.match_chan_regex = '<a href="watchlive/\?channel(.+?).php">(.+?)</a>'
        # Regex Statements
        self.rtmp = re.compile(self.rtmp_regex, re.DOTALL|re.M)
        self.playpath = re.compile(self.playpath_regex, re.DOTALL|re.M)
        self.appurl = re.compile(self.appurl_regex, re.DOTALL|re.M)
        self.schedule = re.compile(self.schedule_regex, re.DOTALL|re.M)
        self.matchtime = re.compile(self.match_time_regex, re.DOTALL|re.M)
        self.matchcomp = re.compile(self.match_comp_regex, re.DOTALL|re.M)
        self.matchdate = re.compile(self.match_date_regex)
        self.matchchan = re.compile(self.match_chan_regex, re.DOTALL|re.M)

        
    def build_rtmp_url(self, link, channelurl):
        rtmp_path = self.rtmp.search(link).group(1)
        play_path = self.playpath.search(link).group(1)
        appurl = self.appurl.search(link).group(2)
        alist = [rtmp_path,' playpath=',play_path,' app=',appurl,' pageURL=',channelurl,self.swfurl]
        rtmp_url = ''.join(alist)
        return rtmp_url


    def get_event_info(self, schedule):
	match_hour = (self.matchtime.search(schedule)).group(1)
	match_min = (self.matchtime.search(schedule)).group(2)
	match_title = (self.matchcomp.search(schedule)).group(1)
	match_comp = (self.matchcomp.search(schedule)).group(2)
	match_day = (self.matchdate.search(schedule)).group(1)
	match_date = (self.matchdate.search(schedule)).group(2)
	match_month = (self.matchdate.search(schedule)).group(3)
	match_year = time.strftime("%y")
	match_date = match_date[0:-2]
        if len(match_date) == 1:
            match_date = '0' + match_date
#	if match_month > time.strftime('%b'):
#		match_year = str(int(match_year + 1))
	slist = [match_month, match_date, match_year, match_hour, match_min]
	tc1 = time.strptime(''.join(slist), '%b%d%y%H%M')
	tc2 = time.mktime(tc1)
	tc3 = time.ctime(tc2 - time.timezone)
	tc4 = time.strptime(tc3, '%a %b %d %H:%M:00 %Y')
	tc5 = time.strftime('%H:%M | %a %b %d', tc4)
	slist = [tc5, ' | ', match_title]
	eventinfo = ''.join(slist)
	return eventinfo
