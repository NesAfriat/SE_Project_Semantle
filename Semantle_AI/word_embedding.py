# Python program to generate word vectors using Word2Vec
# Code from https://www.geeksforgeeks.org/python-word-embedding-using-word2vec/
# importing all necessary modules
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import nltk
warnings.filterwarnings(action='ignore')
import gensim
from gensim.models import Word2Vec


class WordEmbeddeing:
    def __init__(self):
        self.data=[]

    # Create CBOW model
    def create_CBOW_model_from_file(self,file):
        if len(self.data)==0:
            self.words_to_data(file)
        model = gensim.models.Word2Vec(self.data, min_count=1,
                                        vector_size=100, window=5)
        return model

    # Create Skip Gram model
    def create_skipGram_model_from_file(self,file):
        if len(self.data)==0:
            self.words_to_data(file)
        model = gensim.models.Word2Vec(self.data, min_count=1, vector_size=100,
                                         window=5, sg=1)
        return model

    def get_similarity(self,model,word1,word2):
        # Print results
        return model.wv.similarity(word1, word2)

    def words_to_data(self,file):
        #  Reads a words file
        sample = open(file,mode="r", encoding="utf-8")
        s = sample.read()
        # Replaces escape character with space
        f = s.replace("\n", " ")
        # iterate through each sentence in the file
        nltk.download('punkt')
        for i in sent_tokenize(f):
            temp = []
            # tokenize the sentence into words
            for j in word_tokenize(i):
                temp.append(j.lower())

            self.data.append(temp)







