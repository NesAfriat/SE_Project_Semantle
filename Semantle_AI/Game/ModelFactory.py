import copy
import os
from pathlib import Path
from gensim.models import KeyedVectors
from Business.Model.Model import Model
import gensim.downloader as api


def existing_model(path):
    return os.path.isfile(path)


def filter_vocab(vocab, word_list):
    if word_list is None:
        return vocab
    try:
        path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Business/Model/" + word_list
        file = open(path, "r")
        words_set = set((file.read()).split("\n"))
        voc = words_set & vocab
        return voc
    except ValueError as e:
        raise e


def load_from_file(name, word_list=None):
    print("\n\n======================  Model loading ======================")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Business/Model/" + name
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
        # filter only if given path to words
        model_vocab = filter_vocab(vocab, word_list)
        print(f">>vocabulary is loaded, The number of words is: {len(model_vocab)} ")
        print(">>done!")
    return Model(my_model, model_vocab), copy.copy(model_vocab)


def load_from_gensim(name, word_list=None):
    print("\n\n======================  Model loading ======================")
    print(">>Loading model.")
    my_model = api.load(name)
    print(">>model loaded successfully!")
    print(">>loading vocabulary")
    # getting the vocabulary
    vocab = set(my_model.key_to_index)
    print(">>filtering words")
    # filter only if given path to words
    model_vocab = filter_vocab(vocab, word_list)
    print(f">>vocabulary is loaded, The number of words is: {len(model_vocab)} ")
    print(">>done!")
    return Model(my_model, model_vocab), model_vocab


class ModelMap:
    _instance = None
    _model_map = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_model(self, model_name):
        if model_name in self._model_map:
            return self._model_map[model_name]
        else:
            if not model_name in self._model_map.keys():
                if model_name== "Google_Word2Vec.bin":
                    self._model_map[model_name] = load_from_file(model_name)
                else:
                    self._model_map[model_name] = load_from_file(model_name)
        return self._model_map[model_name]
