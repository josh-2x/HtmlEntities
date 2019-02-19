# $Id: html_entities.py 138 2017-10-30 14:44:55Z jmcfarren $

import re
import html.parser

class HtmlEntities():


    def __init__(self, settings, charset):
       self.settings = settings
       self.charset = charset


    def encode(self, content):
        content = content.encode(self.charset, 'xmlcharrefreplace').decode(self.charset)
        content = self.iterSub(content, self.settings.get('html_extras').items())
        if self.settings.get('encode_style') == 'name':
            content = self.numberToName(content)
        return content


    def decode(self, content):
        return html.parser.HTMLParser().unescape(content)


    def numberToName(self, content):
        return self.iterSub(content, self.settings.get('num2name').items())


    def iterSub(self, content, subs = {}):
        for key, val in subs:
            content = re.sub(key, val, content)
        return content