import random

from Business.Model import Model


class Host:
    def __init__(self):
        self.secret_word=None
        self.model= None

    def init_model(self,word_embedding,file):
        new_model= word_embedding.create_skipGram_model_from_file(file)
        self.model= Model(new_model)
        self.secret_word= random.choice(random.choice(word_embedding.data))
        print(self.secret_word)

    def get_model(self):
        return self.model

    def guess_word_offline(self,word):
        if self.model!=None:
            return self.model.get_distance_of_word(word,self.secret_word)

    def guess_word_online(self,word):
        pass

    def return_k_words(self,k):
        pass

