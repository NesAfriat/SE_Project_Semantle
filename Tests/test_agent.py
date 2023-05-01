import io
import unittest
from unittest.mock import patch, Mock
from Semantle_AI.Business.Agents.Agent1 import Agent1
from Semantle_AI.Business.Algorithms.Naive import Naive
from Semantle_AI.Business.Agents.Data import Data


class TestAgentPlayGame(unittest.TestCase):

    @patch("Semantle_AI.Business.Agents.Data", spec=True)
    @patch("Semantle_AI.Business.Algorithms.Naive")
    @patch("Semantle_AI.Business.Agents.Agent.__init__")
    def test_play_game(self, mock_init, mock_algo, mock_data):
        # Mocking the necessary objects
        mock_host = Mock()
        mock_host.error = 1.0
        mock_out = Mock()
        agent = Agent1()
        agent.set_host(mock_host)
        agent.algorithm = mock_algo
        agent.init = Mock(return_value=None)
        agent.algorithm.calculate.return_value = "secret_word"
        mock_host.check_word.return_value = 1.0
        mock_host.getWord.return_value = "secret_word"

        # Set up the mock for the Data class
        mock_data.return_value.is_priority = False
        mock_data.return_value.last_score = -2
        mock_data.return_value.remain_words = ["word1", "word2", "word3"]
        mock_data.return_value.statistics = {}
        mock_data.update_statistic = Mock()

        agent.data = mock_data.return_value

        # Test the function
        agent.start_play(mock_out)

        # Assert the function calls
        self.assertTrue(mock_host.select_word_and_start_game.called)
        self.assertTrue(mock_host.check_word.called_with("test_word"))
        self.assertTrue(mock_out.call_count >= 2)  # At least 2 outputs

if __name__ == '__main__':
    unittest.main()
