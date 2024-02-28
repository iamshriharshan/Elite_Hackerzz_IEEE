import spacy
import json
import string
import re
from pathlib import Path
from bs4 import BeautifulSoup


class Paper:

    def __init__(self, path:str) -> None:
        
        self.path = path
        self.json = json.load(open(path, encoding='utf-8'))
        self.title = self.json['articleTitle']
        self.number = self.json['articleNumber']
        self.authors = self.json['authors']
        self.abstract = self.json['abstract']
        self.clean_text = self._get_text()

    def __str__(self) -> str:
        return f'{self.title}'

    def __repr__(self):
        return f'{self.title}'

    def _get_text(self) -> list:
        text = self.abstract + "\n" + "\n".join([p.text for p in BeautifulSoup(self.json['xml'], 'lxml').find_all('p')])
        return self.clean_text(text)
    
    def _remove_punct(self, doc):
        return (t for t in doc if t.text not in string.punctuation)

    def _remove_stop_words(self, doc):
        return (t for t in doc if not t.is_stop)

    def _lemmatize(self, doc):
        return ' '.join(t.lemma_ for t in doc)

    def clean_text(self,text:str) -> str:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        removed_punct = self._remove_punct(doc)
        removed_stop_words = self._remove_stop_words(removed_punct)
        return self._lemmatize(removed_stop_words)

def getData(path_to_data:str)-> list[list]:
    papers = [Paper(path) for path in Path(path_to_data).rglob('*.json')]
    return papers

