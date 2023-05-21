from parameterized import parameterized
import unittest
from Semantle_AI.Business.Game.ModelFactory import load_from_gensim, load_from_file


class model_tests(unittest.TestCase):
    def setUp(self):
        self.num = 1

    @parameterized.expand([('fasttext-wiki-news-subwords-300',), ("glove-wiki-gigaword-300",), ("word2vec-google-news-300",),("Google_Word2Vec.bin",)])
    def test_loading_gensim_model(self, model_name):
        model, vocab = None, None
        model, vocab = load_from_gensim(model_name, None)
        self.assertTrue(vocab is not None)
        self.assertTrue(model is not None)

    def test_load_model_semantle(self):
        model, vocab = None, None
        model, vocab = load_from_file(name="Google_Word2Vec.bin", dist_method="euclid")
        self.assertTrue(model is not None)
        self.assertTrue(vocab is not None)
        print(vocab)
        self.assertTrue('dog' in vocab)
