#!/usr/bin/python
# -*- coding: utf-8  -*-
#
"""
Copyright (C) 2013 Riley Huntley, Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
import os
import re
import pywikibot
import robot

## Variables ##
reason2 = u'Non-notable diplomat stub article. For the relevant notability policy, please see [[Wikipedia:Notability_(people)#Diplomats|Wikipedia:Notability (people)#Diplomats]].'
warn_template = u'{{subst:Proposed deletion notify|%s|concern=Non-notable diplomat stub article. For the relevant notability policy, please see [[Wikipedia:Notability_(people)#Diplomats|Wikipedia:Notability (people)#Diplomats]].}} ~~~~'
## Regex ##
regex_skip = """\{\{(Template:)?([Pp]ROD
|[Pp]roD
|[Pp]rod
|[Pp]roposal to delete
|[Pp]roposed deletion)"""
regex_skip = regex_skip.replace('\n', '')
REGEX = re.compile(regex_skip, flags=re.IGNORECASE)

def get_creator(site, title):
    #&prop=revisions&titles=File:Eksempel%20p%C3%A5%20s%C3%B8kemotor%202013-04-03%2016-12.jpg&rvprop=timestamp|user|comment&rvdir=newer&rvlimit=1&format=jsonfm
    params = {'action': 'query',
              'prop': 'revisions',
              'titles': title,
              'rvprop': 'user',
              'rvdir': 'newer',
              'rvlimit': '1',
              }
    req = pywikibot.data.api.Request(site=site, **params)
    data = req.submit()
    return data['query']['pages'].values()[0]['revisions'][0]['user']
    
class ProdRobot(robot.Robot):
    def __init__(self):
        robot.Robot.__init__(self, task=10)
        self.site = pywikibot.getSite()
        self.page_with_links = pywikibot.Page(self.site, 'User:Riley_Huntley/Sandbox') ### [[User:Kleinzach/Dips]] ###
        ## Does this even work? ##
        self.trial = True
        self.trial_max = 20
        self.stop_page = pywikibot.Page(self.site, 'User:RileyBot/Stop/10')
        self.log = pywikibot.Page(self.site, 'User:RileyBot/Logs/10')

    def list_of_pages(self):
        return self.page_with_links.linkedPages(namespaces=2) ### Main = (namespaces=0) ###

    def check_page(self):
        text = self.stop_page.get(force=True)
        if text.lower() != 'run':
            log_contentError = self.log.get(get_redirect = True)
            log_contentError = log_contentError + "\n\n" + "# [[:User:RileyBot/Stop/10]]: '''Error: Stop page disabled.''' {{subst:#time: r|now}}" + "\n"
            self.log.put(log_contentError, "[[User:RileyBot|Bot]]: Logging error; Stop page disabled.) ([[User:RileyBot/10|Task 10]]")
            raise Exception("Stop page disabled")

    def do_page(self, page):
        title_1 = page.title()
        if page.isRedirectPage():
            self.output('Page %s is a redirect; skipping.' % page.title())
            return
        newtext = text = page.get()
        if not REGEX.findall(text):
            if not page.exists():
                self.output('Page %s does not exist; skipping'  % page.title()) #<-- THIS NEEDS to BE DONE BEFORE YOU .get()
        self.reason = '[[User:RileyBot|Bot]] trial: Nominating [[' + title_1 + ']] for [[WP:proposed deletion|Proposed deletion]] by request of [[User:Kleinzach|Kleinzach]].) ([[User:RileyBot/10|Task 10]]'
		newtext = '{{subst:Proposed deletion|%s}}\n' % (reason2) + newtext
        ## Check ##
        self.check_page()
        if text != page.get():
            pywikibot.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
                             % page.title())
        pywikibot.showDiff(text, newtext)
        page.put(text, comment=self.reason, watchArticle = True, minorEdit = True)
        if pywikibot.LockedPage:
            pywikibot.output(u"Page %s is locked; skipping."
                             % page.title(asLink=True))
        if pywikibot.EditConflict:
            pywikibot.output(
                u'Skipping %s because of edit conflict'
                % (page.title()))
        creator = get_creator(self.site, page.title())
        self.warn_user(creator, page)

    def warn_user(self, creator, page):
        warn_pg = pywikibot.Page(self.site, 'User talk:'+creator)
        if page.isRedirectPage():
            self.output('Page %s is a redirect; skipping.' % page.title())
        warn_text = warn_template % (page.title())
        warn_text = warn_text.encode('utf-8')
        ## Double check ##
        self.check_page()
        ###MIGHT WORK NOW
        warn_pg.put(warn_text + "\n" + warn_template % page.title(), "[[User:RileyBot|Bot]] notification: proposed deletion of [[" + page.title() + "]].) ([[User:RileyBot/10|Task 10]]")  
        print warn_text

    def Onwiki_log(self):
    ## See line 10 for the log page. We don't check the checkpage here because we want to remember what pages we tagged (even if the bot is making errors) ##
        log_content = self.log.get(get_redirect = True)
        log_content = log_content + "\n" + "# [[:" + title_1 + "]]:" + reason2 + "{{subst:#time: r|now}}"
        self.log.put(log_content, "[[User:RileyBot|Bot]]: Logging [[WP:proposed deletion|proposed deletion]] nomination of [[" + title_1 + "]].) ([[User:RileyBot/10|Task 10]]")

    def run(self):
        for page in self.list_of_pages():
            self.do_page(page)

if __name__ == "__main__":
    bot = ProdRobot()
    bot.run()
