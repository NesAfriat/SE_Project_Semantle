FASTTESXT_WIKI = "fasttext-wiki-news-subwords-300"  # 1GB
GLOVE_WIKI = "glove-wiki-gigaword-300"  # 376MB
WORD2VEC_GOOGLE = "word2vec-google-news-300"  # 1.662GB
WORD2VEC = "Google_Word2Vec.bin"
WORDS_LIST = "words.txt"

import Business.OldModelFactory as MF


class ModelComperator:
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
        for i, j in result.items():
            print("\n\n")
            print(i)
            print(j)
