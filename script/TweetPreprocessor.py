# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:45:08 2016

@author: aedouard
"""

import re

class TweetPreprocessor(object):

    def __init__(self):
        self.FLAGS = re.MULTILINE | re.DOTALL
        self.ALLCAPS = '<allcaps>'
        self.HASHTAG = '<hashtag>'
        self.URL = '<url>'
        self.USER = '<user>'
        self.SMILE = '<smile>'
        self.LOLFACE = '<lolface>'
        self.SADFACE = '<sadface>'
        self.NEUTRALFACE = '<neutralface>'
        self.HEART = '<heart>'
        self.NUMBER = '<number>'
        self.REPEAT = '<repeat>'
        self.ELONG = '<elong>'

    def _hashtag(self, text):
        text = text.group()
        hashtag_body = text[1:]
        if hashtag_body.isupper():
            result = (self.HASHTAG + " {} " + self.ALLCAPS).format(hashtag_body)
        else:
            result = " ".join([self.HASHTAG] + [hashtag_body])#re.split(r"(?=[A-Z])", hashtag_body, flags=self.FLAGS))
        return result

    def _allcaps(self, text):
        text = text.group()
        return text.lower() + ' ' + self.ALLCAPS

    def preprocess(self, text):
        eyes, nose = r"[8:=;]", r"['`\-]?"

        re_sub = lambda pattern, repl: re.sub(pattern, repl, text, flags=self.FLAGS)

        text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", self.URL)
        text = re_sub(r"/"," / ")
        text = re_sub(r"@\w+", self.USER)
        text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), self.SMILE)
        text = re_sub(r"{}{}p+".format(eyes, nose), self.LOLFACE)
        text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), self.SADFACE)
        text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), self.NEUTRALFACE)
        text = re_sub(r"<3", self.HEART)
        text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", self.NUMBER)
        text = re_sub(r"#\S+", self._hashtag)
        text = re_sub(r"([!?.]){2,}", r"\1 " + self.REPEAT)
        text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 " + self.ELONG)

        text = re_sub(r"([A-Z]){2,}", self._allcaps)

        return text.lower()