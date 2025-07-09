from abc import abstractmethod
from html.parser import HTMLParser
from time import time
import requests
import re
import os
import glob
import json

class AssignaturesParser(HTMLParser):
    stack:list[str]
    klass:str
    data:list[dict]

    def __init__(self, titulacio):
        super().__init__()
        self.stack = []
        self.klass = ""
        self.data = []
        self.default = {'titulacio':titulacio}
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.klass = attrs.get('class', self.klass)
        self.stack.append(tag)
        if tag == 'tr':
            self.data.append(dict(self.default))
        elif self.stack[-2:] == ['td', 'a']:
            self.data[-1]['url_fib'] = attrs.get('href')
        

    def handle_endtag(self, tag):
        stack_tag = None
        while tag != stack_tag:
            stack_tag = self.stack.pop()
        if tag == 'tr' and self.data[-1] == self.default:
            del self.data[-1]

    
    def handle_data(self, data):
        if 'td' in self.stack[-2:]:
            self.data[-1][get_key(self.klass)] = data

def get_key(klass):
    return {
        "acronym": "sigles",
        "name": "nom",
        "language": "idioma"
    }.get(klass, klass)

def load_assignatures_titulacio(titulacio, url):
    response = requests.get(url)
    html = response.text
    parser = AssignaturesParser(titulacio)
    parser.feed(html)
    return parser.data

if __name__ == "__main__":
    data = []
    for titulacio, url in [
        ('GEI', 'https://www.fib.upc.edu/ca/estudis/graus/grau-en-enginyeria-informatica/pla-destudis/assignatures'),
        ('MIRI', 'https://www.fib.upc.edu/ca/estudis/masters/master-en-innovacio-i-recerca-en-informatica/pla-destudis/assignatures')
    ]:
        data.extend(load_assignatures_titulacio(titulacio, url))
    os.makedirs("data", exist_ok=True)
    with open("data/assignatures_basic.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

