#!/usr/bin/python
# -*- coding: utf-8  -*-
import sys
import catlib
import pagegenerators
import wikipedia
import codecs
import os
import re
import time
regex_skip    =  [
                  u'extant organization',
                  u'COI editnotice',
                 ]
regex_skip    = ur'\{(Template:)?('+u'|'.join(regex_skip)+u')'
REGEX         = re.compile(regex_skip, flags=re.IGNORECASE)
site = wikipedia.getSite()
log_page      = wikipedia.Page(site,u'User:RileyBot/Logs/11')
stop_page     = wikipedia.Page(site,u'User:RileyBot/Stop/11')
def main():
    log('Run started')
    cat = catlib.Category(site,'Category:Organizations')
    gen = pagegenerators.CategorizedPageGenerator(cat)
    for page in gen:
        check_page()
        if page.exists():
            if not page.isRedirectPage():
                page = "Talk:%s" % (page)
                text = page.get()
                if not REGEX.search(text):
                    newtext = '{{COI editnotice}}\n%s' % (text)
                    try:
                        page.put(newtext, comment=u'[[User:RileyBot|Bot]] trial: Adding [[Template:COI editnotice]] to [[%s]].) ([[User:RileyBot/11|Task 11]]' % page.title(), watchArticle = False, minorEdit = True)
                        log(u'Saved edit on [[%s]]' % page.title())
                    except wikipedia.LockedPage:
                        log(u"Page %s is locked; skipping." % page.title())
                    except wikipedia.EditConflict:
                        log(u'Skipping %s because of edit conflict' % (page.title()))
                    except:
                        log(u'Skipping %s because of unknown error' % (page.title()))
                else:
                    log('[[%s]] ignored due to regular expression' % page.title())
            else:
                log('Page %s is a redirect; skipping.' % page.title())
        else:
            log('Page %s does not exist; skipping.' % page.title())
    shut_down()
def check_page():
  text = stop_page.get(force=True)
  if text.lower() != u'enable':
    log('Check page disabled')
    shut_down()
    
def shut_down():
  log(u'Run Ended')
  f = codecs.open('RileyBot11.txt','r', 'utf-8')
  log_text = f.read()
  f.close()
  text = log_page.get()
  log_page.put(log_text,'Uploading logs for [[User:RileyBot/11|Task 11]]')
  sys.exit(0)
def log(text):
  tm = time.strftime(u'%Y-%m-%d %H:%M:%S',time.gmtime())
  f3 = codecs.open('RileyBot11.txt', 'a', 'utf-8')
  f3.write('\n* %s\t%s' % (tm,text))
  f3.close()

if __name__ == "__main__":
  main()
