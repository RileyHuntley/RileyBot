import mwclient
import settings
site = mwclient.Site(settings.url)
site.login(settings.username, settings.password)
## https://en.wikipedia.org/w/api.php?action=query&list=watchlist&wllimit=500&wlowner=Riley%20Huntley&wltoken=479782&wlshow=!bot&wlprop=user|comment|timestamp|sizes|flags&format=jsonfm
kwargs = {'action':'query',
          'list':'watchlist',
                  'wllimit':'5',
  	  'wlowner':settings.username,
		  'wltoken':settings.token,
		  'wlshow':'!bot',
		  'wlprop':'user|comment|timestamp|sizes|flags',
		  'format':'jsonfm'
}


data = site.api(**kwargs)
print data
if not 'wlstart' in data['query-continue']['watchlist']:
    print('You have no items in your watchlist or none of your watched items were edited in the time period displayed.!')
else:
    print('You have items in your watchlist and your watched items were edited in the time period displayed, moving on...')
