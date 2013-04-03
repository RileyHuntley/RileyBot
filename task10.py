import os
import pywikibot
import robot

## Variables ##
creator = page.getCreator() 
reason = u'Non-notable diplomat stub article. For the relevant notability policy, please see [[Wikipedia:Notability_(people)#Diplomats|Wikipedia:Notability (people)#Diplomats]].'
warn_template = u'{{subst:Proposed deletion notify|%s|concern=%s}} ~~~~'
self.stop_page = pywikibot.Page(self.site, 'User:RileyBot/Stop/10')
log = pywikibot.Page(self.site, 'User:RileyBot/Logs/10')
## Regex ##
regex_skip = """\{\{(Template:)?([Pp]ROD
|[Pp]roD
|[Pp]rod
|[Pp]roposal to delete)"""
regex_skip = regex_skip.replace('\n', '')
REGEX = re.compile(regex_skip, flags=re.IGNORECASE)

class ProdBot(robot.Robot):
	def __init__(self):
        robot.Robot.__init__(self, task=10)
        self.site = pywikibot.getSite()
        self.page_with_links = pywikibot.Page(self.site, 'User:Kleinzach/Dips') ##NEED TO ATTACH THIS TO title_1
        self.reason = '[[User:RileyBot|Bot]] trial: Nominating %s for [[WP:proposed deletion|Proposed deletion]] by request of [[User:Kleinzach|Kleinzach]].) ([[User:RileyBot/10|Task 10]]'
	## Does this even work? ##
	robot.Robot.self.trial = True
	robot.Robot.self.trial_max = 20
	
	def list_of_pages(self):
        gen = self.page_with_links.linkedPages(namespaces=0) ##NEED TO ATTACH THIS TO title_1
        return gen
        
	## Check page; [[User:RileyBot/Stop/10]] ##
	def check_page(self):
		text = self.stop_page.get(force=True)
        if text.lower() != 'run':
        	log_contentError = log.get(get_redirect = True)
			log_contentError = log_contentError + "\n\n" + "# [[:User:RileyBot/Stop/10]]: '''Error: Stop page disabled.''' {{subst:#time: r|now}}" + "\n"
			log.put(log_contentError, "[[User:RileyBot|Bot]]: Logging error; Stop page disabled.) ([[User:RileyBot/10|Task 10]]")
            raise Exception("Stop page disabled")
	def do_page(self, page):	
        	title_1 = page.title()
		if page.isRedirectPage():
            		self.output('Page %s is a redirect; skipping.' % page.title())
            		return
		newtext = text = page.get()
		if not REGEX.findall(text):
		if pywikibot.NoPage():
			self.output('Page %s does not exist; skipping'  % page.title())
		newtext = '{{subst:Proposed deletion|%s}}\n' % (reason) + newtext
		## Check ##
		self.check_page()
		if text != page.get():
			pywikibot.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
		                % page.title())
            	pywikibot.showDiff(text, newtext)
                    page.put(text, comment=comment or self.comment, watchArticle = True, minorEdit = True, **kwargs)
                if pywikibot.LockedPage:
                    pywikibot.output(u"Page %s is locked; skipping."
                                     % page.title(asLink=True))
                if pywikibot.EditConflict:
                    pywikibot.output(
                        u'Skipping %s because of edit conflict'
                        % (page.title()))
	
	def warn_user(self)
		warn_title = pywikibot.Page(wiki, 'User talk:'+creator)
		if page.isRedirectPage():
            		self.output('Page %s is a redirect; skipping.' % page.title())
		if pywikibot.NoPage():
			self.output('Page %s does not exist; skipping'  % page.title())
            		return
		warn_text = warn_template % (title_1, reason)
		warn_text = warn_text.encode('utf-8')
		warn_page = pywikibot.Page(wiki, warn_title)
		## Double check ##
		self.check_page()
		warn_page.edit(warn_text, section="new", sectiontitle="== [[Wikipedia:Proposed deletion|Proposed deletion]] of %s ==", summary="[[User:RileyBot|Bot]] notification: proposed deletion of %s.) ([[User:RileyBot/10|Task 10]]", bot=10) % (warn_title, warn_title)
		print warn_text
	def log(self)
		## See line 10 for the log page ##
		## We don't check the checkpage here because we want to remember what pages we tagged (even if the bot makes errors) ##
		log_content = log.get(get_redirect = True)
		log_content = log_content + "\n" + "# [[:" + title_1 + "]]:" + reason + "{{subst:#time: r|now}}"
		log.put(log_content, "[[User:RileyBot|Bot]]: Logging [[WP:proposed deletion|proposed deletion]] nomination of [[" + title_1 + "]].) ([[User:RileyBot/10|Task 10]]")
	
	def run(self):
	generator = self.list_of_pages()
	
if __name__ == "__main__":
    bot = ProdRobot()
    bot.run()
