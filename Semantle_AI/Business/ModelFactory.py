import copy
import os
from pathlib import Path
from gensim.models import KeyedVectors
from Semantle_AI.Business.Model.Model import Model
import gensim.downloader as api


def existing_model(path):
    return os.path.isfile(path)


def filter_vocab(vocab, word_list):
    if word_list is None:
        return vocab
    try:
        if "Tests" in os.getcwd():
            path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
            path = os.path.join(path, "Business", "Model", word_list)
        else:
            path = os.path.join(os.getcwd(), "Business", "Model", word_list)
        file = open(path, "r")
        words_set = set((file.read()).split("\n"))
        voc = words_set & vocab
        return voc
    except ValueError as e:
        raise e


def replace_subdir(path, old_subdir, new_subdir):
    path_parts = path.split(os.sep)
    updated_path_parts = [new_subdir if part == old_subdir else part for part in path_parts]
    updated_path = os.sep.join(updated_path_parts)
    return updated_path


def load_to_dict(filename):
    result_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split("$")  # split line into key and value
            result_dict[key] = float(value)  # convert value to float and store in dictionary
    return result_dict


def load_from_file(name, word_list=None, dist_method=None):
    print("\n\n======================  Model loading ======================")
    if "Tests" in os.getcwd():
        path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
        path = os.path.join(path, "Business", "Model", name)
    else:
        path = os.path.join(os.getcwd(), "Business", "Model", name)
    if not existing_model(path):
        raise ValueError(f"file not fount in dir : {path}" +
                         ",\n Please make sure the model exists in folder before starting the program...")

    print(">>Loading model.")
    my_model = KeyedVectors.load_word2vec_format(path, binary=True)
    print(">>model loaded successfully!")
    print(">>loading vocabulary")
    # getting the vocabulary
    vocab = set(my_model.key_to_index)
    print(">>filtering words")
    # filter only if given path to words
    model_vocab = filter_vocab(vocab, word_list)
    print(f">>vocabulary is loaded, The number of words is: {len(model_vocab)}")
    if dist_method is not None:
        print(">>loading the distances dictionary")
        if "Tests" in os.getcwd():
            path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
            path = os.path.join(path, "Business", "Model", f"{name}_{dist_method}.txt")
        else:
            path = os.path.join(os.getcwd(), "Business", "Model", f"{name}_{dist_method}.txt")

        if os.path.exists(path):
            distances = load_to_dict(path)
        else:
            distances = dict()
        print(">>done!")
        return Model(my_model, model_vocab, distances), copy.copy(model_vocab)
    else:
        print(">>done!")
        return Model(my_model, model_vocab, dict()), copy.copy(model_vocab)


def load_from_gensim(name, word_list=None, dist_method=None):
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
    if dist_method is not None:
        print(">>loading the distances dictionary")
        if "Tests" in os.getcwd():
            path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
            path = os.path.join(path, "Business", "Model", f"{name}_{dist_method}.txt")
        else:
            path = os.path.join(os.getcwd(), "Business", "Model", f"{name}_{dist_method}.txt")

        if os.path.exists(path):
            distances = load_to_dict(path)
        else:
            distances = dict()
        print(">>done!")
        return Model(my_model, model_vocab, distances), copy.copy(model_vocab)
    else:
        print(">>done!")
        return Model(my_model, model_vocab, dict()), copy.copy(model_vocab)
