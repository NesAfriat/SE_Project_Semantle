import os
from pathlib import Path
from gensim.models import KeyedVectors
from Business.Model.Model import Model


def existing_model(path):
    return os.path.isfile(path)

def filter_vocab(vocab, word_list):
    try:
        path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/" + word_list
        file = open(path, "r")
        words = (file.read()).split("\n")
        voc = [x for x in vocab if (x in words)]
        return voc
    except ValueError as e:
        raise e




def load_from_file(name, word_list):

    print("\n\n======================  loading Model  ======================")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/" + name
    if not existing_model(path):
        raise ValueError(f"file not fount in dir : {path}" +
                   ",\n Please make sure the model exists in folder before starting the program...")
    else:
        print(">>Loading model.")
        my_model = KeyedVectors.load_word2vec_format(path, binary=True)
        print(">>model loaded successfully!")
        print(">>loading vocabulary")
        # getting the vocabulary
        vocab = list(filter(lambda pair: pair[0], my_model.key_to_index))
        print(">>filtering words")
        vocab = filter_vocab(vocab, word_list)
        print(f">>vocabulary is loaded, The number of words is: {len(vocab)} ")
        print(">>done!")
    return my_model, vocab
