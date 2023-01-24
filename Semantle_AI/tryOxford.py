
import gensim.downloader as api

#fasttext-wiki-news-subwords-300 1GB
#glove-wiki-gigaword-300 376MB
#word2vec-ruscorpora-300 198MB
#word2vec-google-news-300 1.662GB

print(api.load("glove-wiki-gigaword-300", return_path=True))  # output: /home/user/gensim-data/glove-twitter-25/glove-twitter-25.gz
w2v_embedding = api.load("glove-wiki-gigaword-300")



