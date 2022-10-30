import sys

import gensim, os, nltk
from gensim.models import Word2Vec
from pathlib import Path
from sklearn.decomposition import PCA
from nltk.corpus import words

def filter_words(sentence):
    return [word.lower() for word in nltk.word_tokenize(sentence) if word.isalnum() and len(word) > 1]


def tokenize(text):
    return [filter_words(sentence) for sentence in nltk.sent_tokenize(text)]


def train_new_model(dementions=100, model_type=1) -> Word2Vec:
    ignore = {".DS_Store", ".txt"}
    sentences = []
    print("\n\n\n\n========================  creating the new model  ========================")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Trains"
    print("\nparsing files and words, this might take a while...")
    items_count = len([entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))])
    items = list(range(0, items_count))
    i = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename not in ignore:
                with open(os.path.join(root, filename), 'r', encoding='utf8') as rf:
                    text = rf.read()
                    sentences.extend(tokenize(text))
                    i=i+1
                    prc = round(( i*100 / items_count),3)
                    sys.stdout.write(f"\r {prc}%")
    print(">>parsing ended")
    print(">>starting model training")
    model = gensim.models.Word2Vec(
        sentences,
        sg=model_type,  # skipgram, 0 for cbow
        min_count=1,
        vector_size=dementions  # num of dementions
    )
    vocab = model.wv.key_to_index.keys()
    print(">>model training finished\n>>Saving model")
    # save the model to file
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/Model.p"
    model.save(path)
    print(">>Saving ended")
    # instantiate the pca objects
    print(">>instantiating pca components.")
    pca = PCA(n_components=2)
    print(">>instantiated, creating pca object of the model...")
    # fit and transform the pca object
    my_pca = pca.fit_transform(model.wv[vocab])
    print(">>done!")
    return model, vocab , pca

def contains_number(string):
    return any(char.isdigit() for char in string)

def train_existing_model(model):
    sentences = []
    ignore = {".DS_Store", ".txt"}
    print(">> starting parse the source, this might take a while...")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Extras/"
    items_count = len([entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))])
    items = list(range(0, items_count))
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename not in ignore:
                with open(os.path.join(root, filename), 'r', encoding='utf8') as rf:
                    text = rf.read()
                    sentences.extend(tokenize(text))
                    i = i + 1
                    prc = round((i * 100 / items_count), 3)
                    sys.stdout.write(f"\r {prc}%")

    # update model
    model.train(sentences,
                total_examples=word2vec_model.corpus_count,
                epochs=word2vec_model.epochs
                )
    print(">>training finished successfully!")

    # print(">>model saved\n\n>>trying examples:")
    # check similar words
    # print(f"\nMost similar word for the word: down is: {word2vec_model.wv.most_similar('down')}")
    # print(f"\nMost similar word for the words: down, walking - is: {word2vec_model.wv.most_similar(['down', 'walking'])}")

    # get similarity scores
    # print(f"\nThe similarity between the words: down, walking - is: {word2vec_model.wv.similarity('down', 'walking')}")
    # print(">>finished!")
