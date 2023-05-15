import random
import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch
from Semantle_AI.Business.Hosts.OfflineHost import OfflineHost
from Semantle_AI.Business.Hosts.OnlineHost import OnlineHost


class test_hosts(unittest.TestCase):

    def setUp(self):
        self.offline_host = OfflineHost()
        self.online_host = OnlineHost()
        self.mock_model = Mock()

    @parameterized.expand([({'dog', 'house', 'cat', 'child'},), ({'dog', 'house'},), ({'dog'},)])
    def test_select_word_offline_host(self, items):
        self.offline_host.set_model(self.mock_model, items)
        self.offline_host.select_word_and_start_game(
            lambda x: self.assertEqual(x, "================Offline game==============="))
        self.assertTrue(self.offline_host.secret_word is not None)

    def test_check_word_offline(self):
        items = {'dog', 'house', 'cat', 'child'}
        self.mock_model.return_value.get_distance_of_word = 1
        self.offline_host.set_model(self.mock_model, items)
        val = self.offline_host.check_word('dog')
    @patch('builtins.print')
    def test_online_host_select_word_and_start_game(self):
        str_finish = None

        self.online_host.select_word_and_start_game(lambda x: print(x))
