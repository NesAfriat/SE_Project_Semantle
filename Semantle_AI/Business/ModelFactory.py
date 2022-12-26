import os
from pathlib import Path
from gensim.models import KeyedVectors
import gensim.downloader as api


# load model from file
from Business.Model.Model import Model


def existing_model(path):
    return os.path.isfile(path)


# def load_trained_model(name):
#     print("======================  loading existing model from file  ======================")
#     path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/" + name
#     my_model = Model(KeyedVectors.load(path, mmap='r'))
#     print(">>model loaded successfully!")
#     print(">>loading vocabulary!")
#     # getting the vocabulary
#     vocab = my_model.get_vocab()
#     print(">>vocabulary is loaded")
#     print(f">> vocab size is: {len(vocab)} words.")
#     print(">>done!")
#     return my_model, vocab


def load_from_file(name):

    print("\n\n======================  loading Model  ======================")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/" + name
    if not existing_model(path):
        raise ValueError(f"file not fount in dir : {path}" +
                   ",\n Please make sure the model exists in folder before starting the program...")
    else:
        print(">>Loading model.")
        my_model = Model(KeyedVectors.load_word2vec_format(path, binary=True))
        print(">>model loaded successfully!")
        print(">>loading vocabulary!")
        # getting the vocabulary
        vocab = my_model.get_vocab()
        print(f">>vocabulary is loaded, The number of words is: {len(vocab)} ")
        print(">>done!")
    return my_model,vocab
