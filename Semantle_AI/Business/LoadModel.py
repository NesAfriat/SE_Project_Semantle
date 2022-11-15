import os
from pathlib import Path
from gensim.models import KeyedVectors
import gensim.downloader as api


# load model from file

def existing_model(name):
    return os.path.isfile(os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/" + name)


def load_trained_model(name):
    print("======================  loading existing model from file  ======================")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/" + name
    my_model = KeyedVectors.load(path, mmap='r')
    print(">>model loaded successfully!")
    print(">>loading vocabulary!")
    # getting the vocabulary
    vocab = list(my_model.index_to_key)
    print(">>vocabulary is loaded")
    print(f">> vocab size is: {len(vocab)} words.")
    print(">>done!")
    return my_model, vocab, True


def load_from_file(trained, name):
    try:
        print("\n\n======================  loading existing model  ======================")
        if existing_model(name):
            return load_trained_model(name)
        print(
            f"file not fount in dir : {Path(os.curdir).parent.absolute()}/Model/" + name + ",\nDownloading from gensim "
                                                                                           "models...")
        print(">>Downloading gensim model, please make sure you have an active internet connection.")
        my_model = api.load("word2vec-google-news-300")
        print(">>model loaded successfully!")
        print(">>loading vocabulary!")
        # getting the vocabulary
        vocab = list(my_model.key_to_index)
        print(">>vocabulary is loaded")
        print(f">> vocab size is: {len(vocab)} words.")
        print(">>done!")
    except ValueError as e:
        print(f"Error while trying download to model.\n{str(e)}")
        return None, None, None
    return my_model, vocab, False
