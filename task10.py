import os
import pywikibot
import robot

##VARIABLES##
creator = page.getCreator() 
reason = u'Non-notable diplomat stub article. For the relevant notability policy, please see [[Wikipedia:Notability_(people)#Diplomats|Wikipedia:Notability (people)#Diplomats]].'
warn_template = u'{{subst:Proposed deletion notify|%s|concern=%s}} ~~~~'

def log(title_1):
    LOGFILE = 'Task10.log'
    if os.path.isfile(LOGFILE):
        f = open(LOGFILE, 'r')
        old = f.read()
        f.close()
    else:
        old = ''
    msg = '*[[:%s]]\n' % (title_1)
    f = open(LOGFILE, 'w')
    f.write(old+msg)
    f.close()
	
class ProdBot(robot.Robot):	

	def __init__(self):
        robot.Robot.__init__(self, task=10)
        self.reason = '[[User:RileyBot|Bot]] trial: Nominating %s for [[WP:proposed deletion|Proposed deletion]] by request of [[User:Kleinzach|Kleinzach]].) ([[User:RileyBot/10|Task 10]]'
	robot.Robot.self.trial = True
	robot.Robot.self.trial_max = 20
	robot.Robot.self.CONFIGURATION_PAGE = CONFIGURATION_PAGE % self.username
	robot.Robot.self.CHECK_CONFIG_PAGE_EVERY = CHECK_CONFIG_PAGE_EVERY
	self.startLogging(pywikibot.Page(self.site, 'User:RileyBot/Task10/Log'))
		
	def do_page(self, page):	
        	title_1 = page.title()
		if page.isRedirectPage():
            		self.output('Page %s is a redirect; skipping.' % page.title())
            		return
		newtext = text = page.get()
		if pywikibot.NoPage():
			self.output('Page %s does not exist; skipping'  % page.title())
		newtext = '{{subst:Proposed deletion|%s}}\n' % (reason) + newtext
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
		
		
		
		
regex_skip = """\{\{(Template:)?([Pp]ROD
|[Pp]roD
|[Pp]rod
|[Pp]roposal to delete)"""
regex_skip = regex_skip.replace('\n', '')
REGEX = re.compile(regex_skip, flags=re.IGNORECASE)


def clean(box):
    text = box.get()
    if not REGEX.findall(text):
        newtext = HEADER + text
        box.put(newtext, "Robot: Reinserting sandbox header")
	def warn_user(self, page2)
		warn_title = pywikibot.Page(wiki, 'User talk:'+creator)
		if page.isRedirectPage():
            		self.output('Page %s is a redirect; skipping.' % page.title())
		if pywikibot.NoPage():
			self.output('Page %s does not exist; skipping'  % page.title())
            		return
		warn_text = warn_template % (title_1, reason)
		warn_text = warn_text.encode('utf-8')
		warn_page = pywikibot.Page(wiki, warn_title)
		warn_page.edit(warn_text, section="new", sectiontitle="== [[Wikipedia:Proposed deletion|Proposed deletion]] of %s ==", summary="[[User:RileyBot|Bot]] notification: proposed deletion of %s.) ([[User:RileyBot/10|Task 10]]", bot=10) % (warn_title, warn_title)
		print warn_text
if __name__ == "__main__":
    bot = ProdRobot()
    try:
        bot.run()
    finally:
        bot.pushLog()
