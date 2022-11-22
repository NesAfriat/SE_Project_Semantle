# import sys
#
# import gensim, os, nltk
# from gensim.models import Word2Vec
# from pathlib import Path
#
# def filter_words(sentence):
#     return [word.lower() for word in nltk.word_tokenize(sentence) if word.isalnum() and len(word) > 1]
#
#
# def tokenize(text):
#     return [filter_words(sentence) for sentence in nltk.sent_tokenize(text)]
#
#
# def train_new_model(dementions=100, model_type=1) -> Word2Vec:
#     ignore = {".DS_Store", ".txt"}
#     sentences = []
#     print("\n\n\n\n========================  creating the new model  ========================")
#     path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Trains"
#     print("\nparsing files and words, this might take a while...")
#     items_count = len([entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))])
#     items = list(range(0, items_count))
#     i = 0
#     for root, dirs, files in os.walk(path):
#         for filename in files:
#             if filename not in ignore:
#                 with open(os.path.join(root, filename), 'r', encoding= 'unicode_escape') as rf:
#                     text = rf.read()
#                     sentences.extend(tokenize(text))
#                     i=i+1
#                     prc = round(( i*100 / items_count),3)
#                     sys.stdout.write(f"\r {prc}%")
#     print(">>parsing ended")
#     print(">>starting model training")
#     model = gensim.models.Word2Vec(
#         sentences,
#         sg=model_type,  # skipgram, 0 for cbow
#         min_count=5,
#         vector_size=dementions  # num of dementions
#     )
#     vocab = model.wv.key_to_index.keys()
#     print(">>model training finished\n>>Saving model")
#     # save the model to file
#     path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Model/word2vec.wordvectors"
#     model.wv.save(path)
#     print(">>Saving ended")
#     print(">>done!")
#     return model, vocab
#
# def contains_number(string):
#     return any(char.isdigit() for char in string)
#
# def train_existing_model(model):
#     sentences = []
#     ignore = {".DS_Store", ".txt"}
#     print(">> starting parse the source, this might take a while...")
#     path = os.path.dirname(Path(os.curdir).parent.absolute()) + "/Extras/"
#     items_count = len([entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))])
#     items = list(range(0, items_count))
#     for root, dirs, files in os.walk(path):
#         for filename in files:
#             if filename not in ignore:
#                 with open(os.path.join(root, filename), 'r', encoding='utf8') as rf:
#                     text = rf.read()
#                     sentences.extend(tokenize(text))
#                     i = i + 1
#                     prc = round((i * 100 / items_count), 3)
#                     sys.stdout.write(f"\r {prc}%")
#
#     # update model
#     model.train(sentences,
#                 total_examples=word2vec_model.corpus_count,
#                 epochs=word2vec_model.epochs
#                 )
#     print(">>training finished successfully!")
#
