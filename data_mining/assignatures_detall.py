from abc import abstractmethod
from html.parser import HTMLParser
from time import time
import requests
import re
import os
import glob
import json

import tqdm

class AssignaturesParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.tags = []
        self.classes = []
        self.attrs = {}

        self.data = {}
        self.property = None
    
    def fitxa(self):
        return 'fitxa' in self.classes
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.append(attrs.get('class', '').strip())
        self.tags.append(tag)
        self.attrs = attrs

        klass = self.classes[-1]
        if tag == 'a' and self.fitxa() and klass == 'external':
            self.data['web'] == attrs.get('href', None)
        
    def handle_data(self, data):
        if not self.tags:
            return
        tag = self.tags[-1]
        attrs = self.attrs or {}
        if tag == 'section' and attrs.get('id') == 'descripcio':
            self.data['desc'] = data.strip()
        elif self.fitxa():
            if data.strip() in ('Crèdits', 'Tipus', 'Departament'):
                self.property = data.strip()
            elif self.property and 'col-xs-9 col-md-9' in self.classes[-2:]:
                self.data[self.property] = data.strip()
                self.property = None

    
    def handle_endtag(self, tag):
        stack_tag = None
        while tag != stack_tag:
            stack_tag = self.tags.pop()
            self.classes.pop()
        self.attrs = None


if __name__ == "__main__":
    with open("data/assignatures_basic.json", "r", encoding="utf-8") as f:
        data:list[dict] = json.load(f)

    new_data = []
    for dat in tqdm.tqdm(data):
        if 'url_fib' not in dat:
            continue
        response = requests.get(dat['url_fib'])
        html = response.text
        parser = AssignaturesParser()
        parser.feed(html)
        dat.update(parser.data)
        new_data.append(dat)


    with open("data/assignatures_detall.json", "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
