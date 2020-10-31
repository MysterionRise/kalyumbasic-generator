import pandas as pd
from nltk.parse import CoreNLPParser
from nltk.corpus import stopwords
import re

PATTERN = r'[\+=%|–·>*",.;@#?!&$:_)(/~•-]+'


def fix_synonyms(sent):
    STRANGE = {
        'MS SQL': 'MSSQL',
        'MS SQL SERVER': 'MSSQLSERVER'
    }
    for w, r in STRANGE.items():
        sent = re.sub(w, r, sent)
    return sent


if __name__ == '__main__':
    stop_words = set(stopwords.words('english'))
    parser = CoreNLPParser(url='http://localhost:9000')
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    df = pd.read_excel('~/Downloads/past_projects_16.10.2020.xlsx', sheet_name='SQL Results')
    databases = {}
    tools = {}
    technologies = {}
    for index, row in df.iterrows():
        if type(row['DATABASE']) == str:
            sent = re.sub(PATTERN, ' ', row['DATABASE'])
            sent = sent.upper()
            sent = fix_synonyms(sent)
            tokens = parser.tokenize(sent)
            for token in tokens:
                if token.lower() not in stop_words:
                    databases[token] = databases.get(token, 0) + 1
        if type(row['TOOLS']) == str:
            sent = re.sub(PATTERN, ' ', row['TOOLS'])
            sent = sent.upper()
            sent = fix_synonyms(sent)
            tokens = parser.tokenize(sent)
            for token in tokens:
                if token.lower() not in stop_words:
                    tools[token] = tools.get(token, 0) + 1
        if type(row['TECHNOLOGIES']) == str:
            sent = re.sub(PATTERN, ' ', row['TECHNOLOGIES'])
            sent = sent.upper()
            sent = fix_synonyms(sent)
            tokens = parser.tokenize(sent)
            for token in tokens:
                if token.lower() not in stop_words:
                    technologies[token] = technologies.get(token, 0) + 1

    for k, v in sorted(databases.items(), key=lambda item: -item[1]):
        print('{}: {}'.format(k, v))

    for k, v in sorted(tools.items(), key=lambda item: -item[1]):
        print('{}: {}'.format(k, v))

    for k, v in sorted(technologies.items(), key=lambda item: -item[1]):
        print('{}: {}'.format(k, v))
    # print(databases)
