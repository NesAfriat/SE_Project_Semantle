import copy
import os
from gensim.models import KeyedVectors
from Semantle_AI.Business import MethodDistances
from Semantle_AI.Business.Model.Model import Model
import gensim.downloader as api
import Semantle_AI.ModelCreator as mc

dist_dict = {
    "euclid": MethodDistances.euclid_function(),
    "cosine": MethodDistances.cosine_function()
}


def existing_model(path):
    return os.path.isfile(path)


def replace_subdir(path, old_subdir, new_subdir):
    path_parts = path.split(os.sep)
    updated_path_parts = [new_subdir if part == old_subdir else part for part in path_parts]
    updated_path = os.sep.join(updated_path_parts)
    return updated_path


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


def load_to_dict(dist_file, vec_file):
    dist_dict = {}
    with open(dist_file, 'r') as file:
        for line in file:
            key, value = line.strip().split("$")  # split line into key and value
            dist_dict[key] = float(value)  # convert value to float and store in dictionary

    vec_dict = {}
    with open(vec_file, 'r') as file:
        for line in file:
            # Split line into word and vector string
            word, vector_str = line.strip().split("=")
            # Convert vector string into a list of floats
            vector = list(map(float, vector_str.split()))
            vec_dict[word] = vector
    return dist_dict, vec_dict


def is_file_empty(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            if len(content.strip()) == 0:
                return True
            else:
                return False
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except IOError:
        print(f"An error occurred while reading the file '{file_path}'.")


def load_from_file(name, word_list=None, dist_method=None):
    print("\n\n======================  Model loading ======================")
    # check if the model already saved as txt files.
    if dist_method is not None:
        # removing the test dir from the path to the files.
        if "Tests" in os.getcwd():
            path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
            path = os.path.join(path, "Business", "Model")
        else:
            path = os.path.join(os.getcwd(), "Business", "Model")

        # set the paths and check if exists.
        dist_path = os.path.join(path, f"{name}_{dist_method}.txt")
        vec_path = os.path.join(path, f"{name}_vectors.txt")

        if not os.path.exists(dist_path) or is_file_empty(dist_path) or \
                not os.path.exists(vec_path) or is_file_empty(vec_path):

            # Loading the model to save it.
            if "Tests" in os.getcwd():
                model_path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
                model_path = os.path.join(model_path, "Business", "Model", name)
            else:
                model_path = os.path.join(os.getcwd(), "Business", "Model", name)
            if not existing_model(model_path):
                raise ValueError(f"file not fount in dir : {model_path}" +
                                 ",\n Please make sure the model exists in folder before starting the program...")

            print(">>Loading model.")
            my_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
            print(">>model loaded successfully!")
            print(">>loading vocabulary")
            # getting the vocabulary
            vocab = set(my_model.key_to_index)
            print(">>filtering words")
            # filter only if given path to words
            model_vocab = filter_vocab(vocab, word_list)
            print(f">>vocabulary is loaded, The number of words is: {len(model_vocab)}")
            print(">>Saving the nex model as vectors and distances.")
            # After loading the model, save the data for next times.

            distances, vectors = mc.save_word_combinations(my_model, model_vocab, name, dist_path, vec_path,
                                                           dist_dict[dist_method])
            del my_model, vocab
            print(">>done!")
        # If the data exists, load it.
        else:
            print(">>Loading the distances and vectors dictionaries")
            distances, vectors = load_to_dict(dist_path, vec_path)
            model_vocab = set(vectors.keys())
            print(">>done!")

        return Model(distances, vectors, model_vocab)
    else:
        raise ValueError("Dist method in load_from_gensim must not be None")


def load_from_gensim(name, word_list=None, dist_method=None):
    print("\n\n======================  Model loading ======================")
    # check if the model already saved as txt files.
    if dist_method is not None:
        # removing the test dir from the path to the files.
        if "Tests" in os.getcwd():
            path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
            path = os.path.join(path, "Business", "Model")
        else:
            path = os.path.join(os.getcwd(), "Business", "Model")

        # set the paths and check if exists.
        dist_path = os.path.join(path, f"{name}_{dist_method}.txt")
        vec_path = os.path.join(path, f"{name}_vectors.txt")
        if not os.path.exists(dist_path) or is_file_empty(dist_path) or \
                not os.path.exists(vec_path) or is_file_empty(vec_path):
            # the data isn't saved. load the model and then save the data.
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
            print(">>Saving the nex model as vectors and distances.")
            # After loading the model, save the data for next times.
            distances, vectors = mc.save_word_combinations(my_model, model_vocab, name, dist_path, vec_path,
                                                           dist_dict[dist_method])
            del my_model, vocab
            print(">>done!")
        # If the data exists, load it.
        else:
            print(">>Loading the distances and vectors dictionaries")
            distances, vectors = load_to_dict(dist_path, vec_path)
            model_vocab = set(vectors.keys())
            print(">>done!")

        return Model(distances, vectors, model_vocab)
    else:
        raise ValueError("Dist method in load_from_gensim must not be None")


def save_vectors(model, model_name):
    # Save vectors to a text file
    model.wv.save_word2vec_format(f'{model_name}_vectors.txt')


def load_vectors(model_name):
    # Load vectors from a text file
    return KeyedVectors.load_word2vec_format(f'{model_name}_vectors.txt')


class ModelFactory:
    _instance = None
    _model_map = {}

    @staticmethod
    def get_model(model_name, dist_func_name, host_vocab=None):
        words_list = "words.txt"
        if model_name in ModelFactory._model_map:
            model = ModelFactory._model_map[model_name]
            if host_vocab is not None:
                model.vocab = model.vocab & host_vocab
            return model
        else:
            if not model_name in ModelFactory._model_map.keys():
                if model_name == "Google_Word2Vec.bin":
                    ModelFactory._model_map[model_name] = load_from_file(model_name, words_list, dist_func_name)
                else:
                    ModelFactory._model_map[model_name] = load_from_gensim(model_name, words_list, dist_func_name)

        model = ModelFactory._model_map[model_name]
        if host_vocab is not None:
            model.vocab = model.vocab & host_vocab
        return model
