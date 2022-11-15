
import gensim.downloader as api

print(api.load("glove-wiki-gigaword-300", return_path=True))  # output: /home/user/gensim-data/glove-twitter-25/glove-twitter-25.gz
