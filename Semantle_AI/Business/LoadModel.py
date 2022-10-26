import os

import gensim
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from pathlib import Path


# load model from file
def load_from_file():
    print("======================  loading existing model from file  ======================")
    path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/Model.p"
    model = gensim.models.Word2Vec.load(path)
    print(">>model loaded successfully!")
    print(">>loading vocabulary!")
    # getting the vocabulary
    vocab = list( model.wv.key_to_index.keys())
    print(">>vocabulary is loaded")
    print(f">> vocab value is: {len(vocab)}")
    #print(">>instantiating pca")
    # instantiate the pca objects
    #pca = PCA(n_components=2)
    #print(">>instantiated")
    return model,vocab
    # fit and transform the pca object
    #my_pca = pca.fit_transform(model.wv[vocab])

    # plot the data
    # print(">>creating model plot...")
    # plt.scatter(my_pca[:,0], my_pca[:,1])
    # for i,word in enumerate(vocab):
    # plt.annotate(word, xy=(my_pca[i,0],my_pca[i,1]))
    # plt.show()
