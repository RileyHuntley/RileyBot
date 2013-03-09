#!/usr/bin/env python
"""
Copyright (C) 2012 Riley Huntley

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

import wikipedia as pywikibot

class RileyBot():
    def __init__(self):
        self.site = pywikibot.Site()
        self.stop_page = pywikibot.Page(self.site, 'User:RileyBot/Stop')

    def check_run_page(self):
        text = self.stop_page.get(force=True)
        if text.lower() != 'run':
            raise Exception("Stop page disabled")
  def run(self):
		page = wikipedia.Page(site, u"User:RileyBot/Test")
        self.do_page(page)		
		
	def do_page(self, page):
		print page
        text = page.get(get_redirect = True)
        try:
            self.check_run_page()
            page.put(u"Test", u"Bot testing in userspace")
        except pywikibot.exceptions.PageNotSaved:
            pass
        except pywikibot.exceptions.LockedPage:
            pass



if __name__ == "__main__":
    bot = RileyBot()
    bot.run()
