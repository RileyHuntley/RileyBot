import mwclient
from time import mktime
from datetime import datetime
import time
import codecs
import settings
# CC-BY-SA Theopolisme
# page where run logs are uploaded to
site2 = mwclient.Site('en.wikipedia.org')
# page where watchlist is checked
log_page = site2.Pages['User:RileyBot/Logs/Watchlist']
l = []
def log(text):
  # timestamp every item to make tracking easier, also use UTC time to avoid local issues
  tm = time.strftime(u'%Y-%m-%d %H:%M:%S',time.gmtime())
  f3 = codecs.open('RileyBotWatchlist.txt', 'a', 'utf-8')
  # post every item to its own line
  f3.write('\n* %s\t%s' % (tm,text))
  f3.close()

def generate(wiki):
	print "Working on " + wiki
	log('Working on' + wiki)
	site1 = mwclient.Site(wiki)
	site1.login(settings.username, settings.password)
	data = site1.watchlist(prop="ids|timestamp|title")
        page3 = site1.Pages['User:RileyBot/Stop']
        text3 = page3.get
        if text3.lower() != u'enable':
            log('Check page disabled')
        print data
	
	global l
	l.append("\n=== " + wiki + " ===")

	l.append("""\n{| class="wikitable sortable"
	|-
	! Page title !! Revision timestamp !! Diff""")

	iz = 0
	for x in data:
		if iz <= 25:
			dt = datetime.fromtimestamp(mktime(x['timestamp']))
			l.append("\n|-\n| " + """<span class="plainlinks">[//""" + wiki + "/wiki/" + x['title'].replace(" ","_") + " " + x['title'] + "]</span> || " + str(dt) + " || " + "[//" + wiki + "/w/index.php?diff=prev&oldid=" + str(x['revid']) + " diff]")
			iz = iz + 1
		else:
			print "That's all for now!"

	l.append("\n|}")

# @Riley_Huntley - Edit this list of wikis to suit your liking.
wikis = ['en.wikipedia.org',
'en.wikiquote.org',
'en.wikivoyage.org',
'es.wikivoyage.org',
'fr.wikivoyage.org',
'he.wikisource.org', 
'simple.wikipedia.org', 
'sa.wikipedia.org',
'wikisource.org', 
'sv.wikivoyage.org',
'test2.wikipedia.org', 
'test.wikipedia.org', 
'tt.wiktionary.org']

for wiki in wikis:
	generate(wiki)

final = ''.join(l)
	
# @Riley_Huntley - You can change this to log in as your own bot if you'd like.
site2.login(settings.username, settings.password)

page = site2.Pages['User:RileyBot/watchlist']
page.save(final, summary = "[[User:RileyBot|Bot]]: Updating global watchlist")
log('Global watchlist updated')
def shut_down():
  # log shutdown
  log(u'Run Ended')
  # get the contents of the log file
  f = codecs.open('RileyBotWatchlist.txt','r', 'utf-8')
  log_text = f.read()
  f.close()
  text = log_page.get()
  # post the log file to the wiki log page
  log_page.put(log_text,'[[User:RileyBot|Bot]]: Uploading logs for [[User:RileyBot/Watchlist|Watchlist]]')
  sys.exit(0)
# general logging function

if __name__ == "__main__":
  main()
