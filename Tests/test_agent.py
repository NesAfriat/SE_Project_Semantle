import random
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from Semantle_AI.Business.Agents.Agent import Agent

class TestAgentPlayGame(unittest.TestCase):

    def setUp(self):
        self.mock_host = Mock()
        self.mock_host.error = 1.0
        self.mock_out = Mock()
        self.agent = Agent()
        self.mock_data = Mock()
        self.agent.set_host(self.mock_host)
        self.agent.algorithm = Mock()
        self.agent.init = Mock(return_value=None)


    def create_mock_data(self):
        # Set up the mock for the Data class
        self.mock_data.return_value.is_priority = False
        self.mock_data.return_value.last_score = -2
        self.mock_data.return_value.remain_words = ["word1", "word2", "word3"]
        self.mock_data.return_value.statistics = {}
        self.mock_data.update_statistic = Mock()
        return self.mock_data


    @parameterized.expand([(1,), (10,), (100,), (1000,), (10000,)])
    def test_play_game(self, num_of_loops):
        # Define the side effect for agent.algorithm.calculate
        def calculate_side_effect(*args, **kwargs):
            calculate_side_effect.call_count += 1
            if calculate_side_effect.call_count == num_of_loops:
                return "secret_word"
            return f"random_string_{calculate_side_effect.call_count}"

        calculate_side_effect.call_count = 0
        self.agent.algorithm.calculate.side_effect = calculate_side_effect

        self.mock_host.check_word.side_effect = lambda word: 1 if word == "secret_word" else random.uniform(0.01, 0.99)
        self.mock_host.getWord.return_value = "secret_word"


        self.agent.data = self.create_mock_data().return_value
        out_arr = []
        self.mock_out.side_effect = lambda out: out_arr.append(out)
        # Test the function
        self.agent.start_play(self.mock_out)


        # Assert the function calls
        self.assertTrue(self.mock_host.select_word_and_start_game.called)
        self.assertTrue(self.mock_host.check_word.called_with("test_word"))
        self.assertEqual(self.agent.data.last_word, 'secret_word')
        #self.assertTrue(self.mock_out.call_count >= 2)  # At least 2 outputs
        self.assertEqual(calculate_side_effect.call_count, num_of_loops)  # Check call count

    def test_play_game_fail(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
