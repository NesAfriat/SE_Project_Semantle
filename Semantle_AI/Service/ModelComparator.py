import Business.ModelFactory as MF
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os
import random

FASTTESXT_WIKI = "fasttext-wiki-news-subwords-300"  # 1GB
GLOVE_WIKI = "glove-wiki-gigaword-300"  # 376MB
WORD2VEC_GOOGLE = "word2vec-google-news-300"  # 1.662GB
WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"


def load_model(model):
    if model == WORD2VEC:
        return MF.load_from_file(model, WORDS_LIST)
    else:
        return MF.load_from_gensim(model

                                   , WORDS_LIST)


class ModelComparator:
    models_url = []

    def __init__(self):
        self.models_url = [FASTTESXT_WIKI, GLOVE_WIKI, WORD2VEC_GOOGLE]

    def compare_models(self):
        result = dict()
        w2v_model, w2v_vocabulary = MF.load_from_file(WORD2VEC, WORDS_LIST)
        for model_name in self.models_url:
            print("\n\n\n\nloading model : " + model_name)
            model, vocab = MF.load_from_gensim(model_name, WORDS_LIST)
            result[model_name] = len(model.models_vocab_intersection(w2v_vocabulary))

    # def create_models_graph_with_semantle(self, model1, model2,sample_size = 100):
    #     print(f"\n\n\n\nloading models : {model1} and {model2}")
    #     w2v_model, w2v_vocabulary = MF.load_from_gensim(WORD2VEC, WORDS_LIST)
    #     w2v_model1, w2v_vocabulary1 = MF.load_from_gensim(model1, WORDS_LIST)
    #     w2v_model2, w2v_vocabulary2 = MF.load_from_gensim(model2, WORDS_LIST)
    #
    #     print("\n\n===================  Generating compare graph with Semantle  ===================\n\n")
    #     print(f">>Choosing words samples. Amount : {sample_size}")
    #     # Take a random sample of words from each vocabulary
    #     words1 = random.sample(w2v_vocabulary1, sample_size)
    #     words2 = random.sample(w2v_vocabulary2, sample_size)
    #
    #     # Create two empty lists to store the distances
    #     distances1 = []
    #     distances2 = []
    #
    #     print(">>Calculate the distances between each pair of words.")
    #     # Calculate the distances between each pair of words
    #     for word1 in words1:
    #         for word2 in words2:
    #             try:
    #                 sim1 = w2v_model1.similarity(word1, word2)
    #                 sim2 = w2v_model2.similarity(word1, word2)
    #                 distances1.append(sim1)
    #                 distances2.append(sim2)
    #             except ValueError:
    #                 a = 0
    #
    #     print(">>Plotting the results.")
    #     # Plot the distances against each other
    #     plt.scatter(distances1, distances2)
    #     plt.xlabel('Distances in Model 1')
    #     plt.ylabel('Distances in Model 2')
    #     # Save the plot as a PNG file if a save path is provided
    #     dir_name = generate_models_compare_name()
    #     print(">>Saving the graph as png file.")
    #     # Save the plot as a PNG file if a save path is provided
    #     if dir_name is not None:
    #         plt.savefig(dir_name)
    #         print(f">>File was saved in {dir_name}")
    #     plt.show()

    @staticmethod
    def create_models_graph(model1, model2, sample_size=2000):

        print(f"\n\n\n\nloading models : {model1} and {model2}")
        w2v_model1, w2v_vocabulary1 = load_model(model1)
        w2v_model2, w2v_vocabulary2 = load_model(model2)

        print("\n\n======================  Generating compare graph ======================\n\n")

        print(f">>Choosing words samples. Amount : {sample_size}")
        # Take a random sample of words from each vocabulary
        words1 = random.sample(w2v_vocabulary1, sample_size)
        words2 = random.sample(w2v_vocabulary2, sample_size)

        # Create two empty lists to store the distances
        distances1 = []
        distances2 = []

        print(">>Calculate the distances between each pair of words.")
        # Calculate the distances between each pair of words
        for word1 in words1:
            for word2 in words2:
                if word2 in w2v_vocabulary1 and word1 in w2v_vocabulary2:
                    sim1 = w2v_model1.model.similarity(word1, word2)
                    sim2 = w2v_model2.model.similarity(word1, word2)
                    distances1.append(sim1)
                    distances2.append(sim2)

        print(">>Plotting the results.")
        # Plot the distances against each other
        plt.scatter(distances1, distances2)
        plt.xlabel(f'Distances in Model {model1}')
        plt.ylabel(f'Distances in Model {model2}')
        # Save the plot as a PNG file if a save path is provided
        dir_name = generate_models_compare_name()
        file_name = f"{dir_name}/models_{model1}-{model2}_{sample_size}_points.png"
        print(">>Saving the graph as png file.")
        # Save the plot as a PNG file if a save path is provided
        if dir_name is not None:
            plt.savefig(file_name)
            print(f">>File was saved in {file_name}")
        plt.show()


def generate_models_compare_name():
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/models_compare/without_semantle/{time}"
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError as e:
        pass
    return path


def generate_models_compare_with_semantle_name():
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/models_compare/without_semantle/{time}"
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError as e:
        pass
    return path
