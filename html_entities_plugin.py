# $Id: html_entities_plugin.py 142 2017-10-30 21:07:26Z jmcfarren $

import sublime
import sublime_plugin
import re
from .html_entities import HtmlEntities

class HtmlEntitiesCommand(sublime_plugin.TextCommand):


    def run(self, edit, action=''):
        settings = sublime.load_settings('HtmlEntities.sublime-settings')
        charset = settings.get('charset')
        valid_charsets = settings.get('valid_charsets')
        # get region and content
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        if charset == 'auto':
            charset = settings.get('fallback_charset')
            results = re.search(settings.get('auto_charset_pat'), content)
            if results and results.group(1) in valid_charsets:
                charset = results.group(1)
        he = HtmlEntities(settings, charset)
        if self.view.sel()[0].empty():
            # if there was no user text selection update the entire window buffer
            content = self.view.substr(region)
            if action == 'encode':
                self.view.replace(edit, region, he.encode(content))
            elif action == 'decode':
                self.view.replace(edit, region, he.decode(content))
            elif action == 'num2name':
                self.view.replace(edit, region, he.num2name(content))
        else:
            # if selection(s), update each
            for region in self.view.sel():
                if not region.empty():
                    content = self.view.substr(region)
                    if action == 'encode':
                        self.view.replace(edit, region, he.encode(content))
                    elif action == 'decode':
                        self.view.replace(edit, region, he.decode(content))
                    elif action == 'num2name':
                        self.view.replace(edit, region, he.numberToName(content))