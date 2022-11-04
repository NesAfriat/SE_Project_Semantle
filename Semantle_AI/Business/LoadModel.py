import gensim.downloader as api

# load model from file
def load_from_file():
    try:
        print("\n\n======================  loading existing model from file  ======================")
    # Show all available models in gensim-data
        print(">>Downloading gensim model, please make sure you have an active internet connection.")
        my_model = api.load("glove-wiki-gigaword-50")
        #my_model = gensim.models.Word2Vec(model)
        print(">>model loaded successfully!")
        print(">>loading vocabulary!")
    # getting the vocabulary
        vocab = list(my_model.key_to_index)
        print(">>vocabulary is loaded")
        print(f">> vocab size is: {len(vocab)} words.")
    # instantiate the pca objects
        #print(">>instantiating pca components.")
        #pca = PCA(n_components=2)
        #print(">>instantiated, creating pca object of the model.")
    # fit and transform the pca object
        #my_pca = pca.fit_transform(model.wv[vocab])
        print(">>done!")
    except ValueError as e:
        print(f"Error while trying download to model.\n{str(e)}")
        return None, None, None
    return my_model, vocab
