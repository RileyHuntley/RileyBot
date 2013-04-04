#!/usr/bin/python
# -*- coding: utf-8  -*-
import pagegenerators
import codecs
import os
import re
import time
import wikipedia
# array of strings to search for and exclude those from re-tagging
regex_skip    =  [
                  u'prod',
                  u'proposal to delete',
                  u'proposed deletion',
                 ]
regex_skip    = ur'"\\{(Template:)?('+u'|'.join(regex_skip)+u')'
REGEX         = re.compile(regex_skip, flags=re.IGNORECASE)
site          = wikipedia.getSite()
# page where run logs are uploaded to
log_page      = wikipedia.Page(site,u'User:RileyBot/Logs/10')
# links from this page are what get tagged
source_page   = wikipedia.Page(site,u'User:Riley_Huntley/Sandbox')
# automated shutdown feature
stop_page     = wikipedia.Page(site,u'User:RileyBot/Stop/10')
# PROD reason
tag_reason    = u'Non-notable diplomat stub article. For the relevant notability policy, please see [[Wikipedia:Notability_(people)#Diplomats|Wikipedia:Notability (people)#Diplomats]].'
# user talk page notice
warn_template = u'{{subst:Proposed deletion notify|%s|concern='+tag_reason+'}} ~~~~'

def main():
  log('Run started')
  # get a list of pages to tag
  pages_to_work_on = [x for x in pagegenerators.NamespaceFilterPageGenerator(source_page.linkedPages(),[2])]
  for page in pages_to_work_on:
    # is the bot allowed to do this task?
    check_page()
    # if page has already been deleted, log and skip
    if page.exists():
      # check if it is a redirect, if it is log and skip
      if not page.isRedirectPage():
        # get page contents
        text = page.get()
        # check to see if there is a template on the black list, if it is log and skip
        if not REGEX.search(text):
          # add PROD notice
          newtext = '{{subst:Proposed deletion|%s}}\n%s' % (tag_reason,text)
          try:
            # try and save the page and log it
            page.put(newtext, comment=u'[[User:RileyBot|Bot]] trial: Nominating [[%s]] for [[WP:proposed deletion|Proposed deletion]] by request of [[User:Kleinzach|Kleinzach]].) ([[User:RileyBot/10|Task 10]]' % page.title(), watchArticle = False, minorEdit = True)
            log(u'Tagging [[%s]]' % page.title())
          # page is protected
          except wikipedia.LockedPage:
            log(u"Page %s is locked; skipping." % page.title())
          # Edit conflicted with another user
          except wikipedia.EditConflict:
            log(u'Skipping %s because of edit conflict' % (page.title()))
          # some unknown error has occurred, log and review at a latter date
          except:
            log(u'Skipping %s because of unknown error' % (page.title()))
          # page has been tagged for PROD now need to notify the creator
          warn_user(page)
        else:
          log('[[%s]] ignored due to regular expression' % page.title())
      else:
        log('Page %s is a redirect; skipping.' % page.title())
    else:
      log('Page %s does not exist; skipping.' % page.title())
  shut_down()
  
def check_page():
  # get check page and if contents are not 'run' have the bot shutdown as someone has disabled the bot
  text = stop_page.get(force=True)
  if text.lower() != u'run':
    log('Check page disabled')
    shut_down()
# notfy a user about a page that has been tagged for deletion, dont check the stop page as we want to avoid not notifying the creator of the talk page
def warn_user(page):
  # get the first person to edit the page not 100% reliable but is the best for identifying who created a page
  creator,ts = page.getCreator()
  # create a page object for their talk page
  talk_page = wikipedia.Page(site,u'User talk:%s' % creator)
  # due to renames, switching accounts and what not sometimes the talk page has been redirected to a different username if so find out and use that as the correct page
  if talk_page.isRedirectPage():
    talk_page = talk_page.getRedirectTarget()
    if not talk_page.isTalkPage():
      # for some reason the new talk page isnt a talk page (banned/blocked user, whos talk page redirects to their user page ect)
      log(u'Unable to locate talk page for [[User:%s]]' % creator)
      return
  # format talk page notice
  warn_text = warn_template % (page.title())
  # get user talk page contents
  text = talk_page.get()
  # combine the two
  text+=u"\n%s" % warn_text
  try:
    # save the talk page and log the details
    talk_page.put(text, u"[[User:RileyBot|Bot]] notification: proposed deletion of [[%s]] [[User:RileyBot/10|Task 10]]" % page.title())
    log(u'Notifying [[User:%s]] about [[%s]]' % (page.title()))
  except wikipedia.LockedPage:
    log(u"Page %s is locked; skipping." % (talk_page.title()))
  except wikipedia.EditConflict:
    log(u'Skipping %s because of edit conflict' % (talk_page.title()))
  except:
    log(u'Skipping %s because of unknown error' % (talk_page.title()))
  return
# used to wrap up and cleanly exit the program, can be called from mutiple locations within the program 
def shut_down():
  # log shutdown
  log(u'Run Ended')
  # get the contents of the log file
  f = codecs.open('RileyBot10.txt','r', 'utf-8')
  log_text = f.read()
  f.close()
  text = log_page.get()
  # post the log file to the wiki log page
  log_page.put(log_text,'Uploading all logs for [[User:RileyBot/10|Task 10]]')

# general logging function
def log(text):
  # timestamp every item to make tracking easier, also use UTC time to avoid local issues
  tm = time.strftime(u'%Y-%m-%d %H:%M:%S',time.gmtime())
  f3 = codecs.open('RileyBot10.txt', 'a', 'utf-8')
  # post every item to its own line
  f3.write('\n* %s\t%s' % (tm,text))
  f3.close()

if __name__ == "__main__":
  main()
