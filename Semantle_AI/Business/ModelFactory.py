import copy
import os
from gensim.models import KeyedVectors
from Business.Model.Model import Model
import gensim.downloader as api


def existing_model(path):
    return os.path.isfile(path)


def filter_vocab(vocab, word_list):
    if word_list is None:
        return vocab
    try:
        path =  "./Business/Model/" + word_list
        file = open(path, "r")
        words_set = set((file.read()).split("\n"))
        voc = words_set & vocab
        return voc
    except ValueError as e:
        raise e


def load_from_gensim(name, word_list=None):
    print("\n\n======================  Model loading ======================")
    print(">>Loading model.")
    my_model = api.load(name)
    print(">>model loaded successfully!")
    print(">>loading vocabulary")
    # getting the vocabulary
    vocab = set(my_model.key_to_index)
    print(">>filtering words")
    ##filter only if given path to words
    model_vocab = filter_vocab(vocab, word_list)
    print(f">>vocabulary is loaded, The number of words is: {len(model_vocab)} ")
    print(">>done!")
    return Model(my_model, model_vocab), copy.copy(model_vocab)


def load_from_file(name, word_list=None):
    print("\n\n======================  Model loading ======================")
    path =  "./Business/Model/" + name
    if not existing_model(path):
        raise ValueError(f"file not fount in dir : {path}" +
                         ",\n Please make sure the model exists in folder before starting the program...")
    else:
        print(">>Loading model.")
        my_model = KeyedVectors.load_word2vec_format(path, binary=True)
        print(">>model loaded successfully!")
        print(">>loading vocabulary")
        # getting the vocabulary
        vocab = set(my_model.key_to_index)
        print(">>filtering words")
        ##filter only if given path to words
        model_vocab = filter_vocab(vocab, word_list)
        print(f">>vocabulary is loaded, The number of words is: {len(model_vocab)} ")
        print(">>done!")
    return Model(my_model, model_vocab), copy.copy(model_vocab)
