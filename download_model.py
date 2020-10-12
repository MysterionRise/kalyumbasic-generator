from gensim.models import KeyedVectors
import spacy


def pipe_add(n, names=['sentencizer']):
    pos = 0
    for x in names:
        if not x in n.pipe_names:
            if pos >= len(n.pipe_names):
                n.add_pipe(n.create_pipe(x))
                pos += 1
            else:
                n.add_pipe(n.create_pipe(x), before=n.pipe_names[pos])
                pos += 1
    return n


nlp_ru = pipe_add(spacy.load('./ru2'), ['tagger', 'parser'])
print("RU pipeline: {}".format(nlp_ru.pipe_names))

token = nlp_ru('привет')[0]
print('{}_{}'.format(token.lemma_, token.pos_))

model = KeyedVectors.load_word2vec_format('180/model.bin', binary=True)
print(model['{}_{}'.format(token.lemma_, token.pos_)].shape)
