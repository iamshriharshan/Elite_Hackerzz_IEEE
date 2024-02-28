import nltk
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
    
    def clean_text(self, text:str) -> list:

        #Removing HTML code
        pattern = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?<[^>]+>"

        text=re.sub(pattern,"",text)


        # remove leading and trailing white space
        text = text.strip()

        # replace multiple consecutive white space characters with a single space
        text = " ".join(text.split())

        #Normalizing data
        text=text.lower()

        #Tokenizing data
        tokens = nltk.word_tokenize(text)

        #Removing punctuation
        Just_word_tokens = [token for token in tokens if token not in string.punctuation]

        #Removing stopwords
        stopwords = nltk.corpus.stopwords.words("english")
        

        filtered_tokens = [token for token in tokens if token not in stopwords]

        #Removing frequently appearing words
        fdist = nltk.FreqDist(tokens)

        # remove the most common words (e.g., the top 10% of words by frequency)
        filtered_tokens2 = [token for token in tokens if fdist[token] < fdist.N() * 0.1]

        #Lemmatizing
        lemmatizer = nltk.stem.WordNetLemmatizer()

        # lemmatize each token
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return lemmatized_tokens

def getData(path_to_data:str)-> list[list]:
    papers = [Paper(path) for path in Path(path_to_data).rglob('*.json')]
    return papers

#_______main_______
h1=Paper('8825770.json')
print(h1.clean_text)
