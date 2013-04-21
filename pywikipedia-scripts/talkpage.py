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

template_skip_list = [u'extant organization', u'COI editnotice']
template_skip_regex = re.compile(ur'\{(Template:)?('+u'|'.join(template_skip_list)+u')',re.I)
skip_these = [u'Organization']
title_blacklist = [
                    u'list',
                  ]
title_blacklist_regex = re.compile(ur'(%s)' % u'|'.join(title_blacklist),re.I)
site = wikipedia.getSite()

log_page = wikipedia.Page(site,u'User:RileyBot/Logs/11')
stop_page = wikipedia.Page(site,u'User:RileyBot/Stop/11')

def main():
    check_page()
    log('Run started')
    cat = catlib.Category(site,'Category:Companies based in Idaho')
    gen = pagegenerators.CategorizedPageGenerator(cat)
    for page in gen:
        if page.namespace() == 0:
            if page.title() not in skip_these and not title_blacklist_regex.search(page.title()):
                if page.exists():
                    if not page.isRedirectPage():
                        talk_page = page.toggleTalkPage()
                        try:
                            text = talk_page.get()
                        except wikipedia.NoPage:
                            text = u''
                        if not template_skip_regex.search(text):
                            newtext = '{{COI editnotice}}\n%s' % (text)
                            try:
                                talk_page.put(newtext, comment=u'[[User:RileyBot|Bot]] trial: Added [[Template:COI editnotice]] to [[%s]]) ([[User:RileyBot/11|Task 11]]' % page.title(), watchArticle = False, minorEdit = True)
                                log(u'Saved edit on [[%s]]' % talk_page.title())
                            except wikipedia.LockedPage:
                                log(u"Page [[%s]] is locked; skipping." % talk_page.title())
                            except wikipedia.EditConflict:
                                log(u'Skipping [[%s]] because of edit conflict' % (talk_page.title()))
                            except:
                                log(u'Skipping [[%s]] because of unknown error' % (talk_page.title()))
                        else:
                            log('[[%s]] ignored due to regular expression' % talk_page.title())
                    else:
                        log('Page [[%s]] is a redirect; skipping.' % talk_page.title())
                else:
                    log('Page [[%s]] does not exist; skipping.' % talk_page.title())
            else:
                log('Page [[%s]] was in skip list.' % talk_page.title())
        else:
            log('Page [[%s]] is not in the article namespace.' % page.title())
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
    print tm + ": " + text
    f3 = codecs.open('RileyBot11.txt', 'a', 'utf-8')
    f3.write('\n* %s\t%s' % (tm,text))
    f3.close()

if __name__ == "__main__":
    main()
