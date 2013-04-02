import os
import pywikibot
import robot

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
  
	def __init__(self):
        robot.Robot.__init__(self, task=10)
        self.reason = '[[User:RileyBot|Bot]] trial: Nominating %s for [[WP:proposed deletion|Proposed deletion]] by request of [[User:Kleinzach|Kleinzach]].) ([[User:RileyBot/10|Task 10]]'
	def do_page(self, page):	
        title_1 = page.title()
		if page.isRedirectPage():
            self.output('Page %s is a redirect; skipping.' % page.title())
            return
		text = page.get() 
		if pywikibot.NoPage():
			self.output('Page %s does not exist; skipping'  % page.title())
		text = '{{subst:Proposed deletion|Non-notable diplomat stub article. For the relevant notability policy, please see [[Wikipedia:Notability_(people)#Diplomats|Wikipedia:Notability (people)#Diplomats]].}}\n' + text
		if text != page.get():
			pywikibot.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
		                % page.title())
            pywikibot.showDiff(page.get(), text)
            pywikibot.output(u'Comment: %s' % comment)
            choice = pywikibot.inputChoice(
                u'Do you want to accept these changes?',
                ['Yes', 'No'], ['y', 'N'], 'N')
            if choice == 'y':
                try:
                    # Save the page
                    page.put(text, comment=comment or self.comment, **kwargs)
                except pywikibot.LockedPage:
                    pywikibot.output(u"Page %s is locked; skipping."
                                     % page.title(asLink=True))
                except pywikibot.EditConflict:
                    pywikibot.output(
                        u'Skipping %s because of edit conflict'
                        % (page.title()))
                else:
                    return True
        return False
