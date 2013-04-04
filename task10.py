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
import wikipedia
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

class ProdRobot(robot.Robot):
    def __init__(self):
        robot.Robot.__init__(self, task=10)
        self.site = wikipedia.getSite()
        self.page_with_links = wikipedia.Page(self.site, 'User:Riley_Huntley/Sandbox') ### [[User:Kleinzach/Dips]] ###
        ## Does this even work? ##
        self.trial = True
        self.trial_max = 20
        self.stop_page = wikipedia.Page(self.site, 'User:RileyBot/Stop/10')
        self.log = wikipedia.Page(self.site, 'User:RileyBot/Logs/10')

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
            wikipedia.output('Page %s is a redirect; skipping.' % page.title())
            return
        text = page.get()
        if not REGEX.findall(text):
            if not page.exists():
                wikipedia.output('Page %s does not exist; skipping'  % page.title()) #<-- THIS NEEDS to BE DONE BEFORE YOU .get()
        newtext = '{{subst:Proposed deletion|%s}}\n' % (reason2) + newtext
        ## Check ##
        self.check_page()
        wikipedia.showDiff(text, newtext)
        try:
            page.put(newtext, comment=u'[[User:RileyBot|Bot]] trial: Nominating [[%s]] for [[WP:proposed deletion|Proposed deletion]] by request of [[User:Kleinzach|Kleinzach]].) ([[User:RileyBot/10|Task 10]]' % page.title(), watchArticle = False, minorEdit = True)
        except wikipedia.LockedPage:
            wikipedia.output(u"Page %s is locked; skipping." % page.title(asLink=True))
        except wikipedia.EditConflict:  
            wikipedia.output( u'Skipping %s because of edit conflict' % (page.title()))
        
        self.warn_user(page)

    def warn_user(self,page):
        creator = page.getCreator()
        talk_page = wikipedia.Page(self.site, u'User talk:%s' % creator)
        if talk_page.isRedirectPage():
            wikipedia.output('Page %s is a redirect; skipping.' % page.title())
            return
        warn_text = warn_template % (page.title())
        text = talk_page.get()
        text+=u"\n%s" % warn_text
        talk_page.put(text, "[[User:RileyBot|Bot]] notification: proposed deletion of [[" + page.title() + "]].) ([[User:RileyBot/10|Task 10]]")  
        wikipedia.output( text)

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
