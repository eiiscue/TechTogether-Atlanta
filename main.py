from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import requests
from bs4 import BeautifulSoup
from googlesearch import search

# Credit for Google Search links importing :  https://www.geeksforgeeks.org/performing-google-search-using-python-code/
# Text Summarization Model  : https://huggingface.co/facebook/bart-large-cnn Pre Trained
# Abstract Text Summarization Model : https://www.thepythoncode.com/article/text-summarization-using-huggingface-transformers-python

# Text Summarization Tool : dhttps://towardsdatascience.com/summarize-long-text-documents-using-machine-learning-d49aaf5fc99a

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

class QueryPage:
    def __init__(self,phrase = ''):
        self.phrase = phrase
    def getLinksPage(self):
        queryLinks =[]
        # try :

        # requests.exceptions.HTTPError: 403 Client Error:
        for j in search(self.phrase,tld='co.in',num = 5 ,stop = 6,pause= 2):
            queryLinks.append(j)
        return queryLinks
    def getTextFromURL(self,url):
        r = requests.get(url)
        s = BeautifulSoup(r.text,"html.parser")
        text = ' '.join(map(lambda x:x.text, s.find_all('p')))
        return text
#     Source For Text From URL : http://www.assafelovic.com/blog/2020/12/28/how-to-build-a-url-text-summarizer-with-simplenbspnlp
    def textSummarizer(self):
        if not self.phrase:
            print("INVALID PHRASE ")
        links = self.getLinksPage()
        text = ""
        for link in links:
            text += self.getTextFromURL(link)+" "
        res = {}
        # with open('textInput','w',encoding="utf-8") as f:
        #     f.write(text)
        # parser = PlaintextParser.from_string(str, Tokenizer("ENGLISH"))
        try:
            parser1 = HtmlParser.from_url(links[0], Tokenizer("ENGLISH"))
            parser2 = HtmlParser.from_url(links[1], Tokenizer("ENGLISH"))
            parser3 = HtmlParser.from_url(links[2], Tokenizer("ENGLISH"))
            parser4 = HtmlParser.from_url(links[3], Tokenizer("ENGLISH"))
            parser5 = HtmlParser.from_url(links[4], Tokenizer("ENGLISH"))
        except requests.HTTPError as exception:
            print(exception)
        stemmer = Stemmer("ENGLISH")
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words("ENGLISH")
        res = []
        for sentence in summarizer(parser1.document, 10):
            res.append(sentence)
        for sentence in summarizer(parser2.document, 10):
            res.append(sentence)
        for sentence in summarizer(parser3.document, 5):
            res.append(sentence)
        for sentence in summarizer(parser4.document, 5):
            res.append(sentence)
        for sentence in summarizer(parser5.document, 5):
            res.append(sentence)
        return res
a = QueryPage("Bitcoin?")
qL = a.getLinksPage()
print(qL,len(qL))
summary = '\n '.join(str(sentence) for sentence in a.textSummarizer())
print(summary)
