import os

import gensim
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from pathlib import Path
from nltk.corpus import words
from pylab import mpl


# load model from file
def load_from_file():
    print("======================  loading existing model from file  ======================")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/Model.p"
    my_model = gensim.models.Word2Vec.load(path)
    print(">>model loaded successfully!")
    print(">>loading vocabulary!")
    # getting the vocabulary
    vocab = list( my_model.wv.key_to_index.keys())
    print(">>vocabulary is loaded")
    print(f">> vocab size is: {len(vocab)} words.")
    # instantiate the pca objects
    print(">>instantiating pca components.")
    pca = PCA(n_components=2)
    print(">>instantiated, creating pca object of the model...")
    # fit and transform the pca object
    my_pca = pca.fit_transform(my_model.wv[vocab])
    print(">>done!")
    return my_model,vocab,my_pca

def read_words():
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Vocab/vocab.txt"
    words = []
    with open(path,'r') as file:
        for line in file:
            for word in line.split():
                words.append(word)
    return words

def filter_vocab(model, path):
    words = read_words()

def show_visual( vocab, pca):

    print("==================================================")
    # plot the data
    print(">>creating model plot...")
    mpl.rcParams["font.sans-serif"] = ["SimHei"]
    mpl.rcParams["axes.unicode._minus"] = False
    plt.scatter(pca[:,0], pca[:,1])
    for i,word in enumerate(vocab):
        plt.annotate(word, xy=(pca[i,0],pca[i,1]))
    plt.show()
