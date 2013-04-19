# -*- coding: utf-8 -*-
 
import sys
import os
 
import ceterach
 
import mwparserfromhell as mwparser
 
def main():
    global api
    api = ceterach.api.MediaWiki("http://en.wikivoyage.org/w/api.php")
    api.login("RileyBot", ceterach.passwords.lcsb2)
    bot = SandBot1(api)
    bot.run()
 
class SandBot1:
    REINSERT = "{{Please leave this line alone (SB)}}\n\n"
    SANDBOXES = ("Wikivoyage:Graffiti wall"
    )
    TEMPLATES = ("Template:Please leave this line alone (Sandbox heading)"
    )
 
    def __init__(self, api, shutoff="User:RileyBot/Graffiti wall/Run"):
        self.api = api
        self.shutoff_page = api.page(shutoff)
 
    @property
    def is_allowed(self):
        return self.shutoff_page.content.lower() == "run"
 
    def get_templates_on(self, page):
        tl = tuple(self.api.prop(500, "templates", tlnamespace=10, titles=page))
        if not tl[0].get("templates", None):
            return
        for x in tl[0]["templates"]:
            yield self.api.page(x["title"])
 
    def check_if_heading_is_gone(self, box):
        templates_in_box = self.get_templates_on(box)
        return not ("Template:Sandbox heading" in [x.title for x in templates_in_box])
 
    def run(self):
        if not self.is_allowed:
            return
        for sandbox in self.SANDBOXES:
            print(sandbox)
            box = self.api.page(sandbox)
            if box.revision_user == "RileyBot":
                continue
            if self.check_if_heading_is_gone(box.title):
                box.prepend(self.REINSERT, summary="Reinserting sandbox header", bot=Run)
                print("\thad a header reinserted!")
 
if __name__ == "__main__":
    main()
    api.logout()
