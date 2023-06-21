import json
import os
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch
from Semantle_AI.GamHandler.Menu import Menu
from Semantle_AI.Service.AgentHandlers.ManualAgentHandler import ManualAgentHandler


def replace_subdir(path, old_subdir, new_subdir):
    path_parts = path.split(os.sep)
    updated_path_parts = [new_subdir if part == old_subdir else part for part in path_parts]
    updated_path = os.sep.join(updated_path_parts)
    return updated_path


class TestManualAgentHandler(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()
        self.inp = MagicMock()
        self.finished = MagicMock()
        self.manual_agent_handler = ManualAgentHandler(self.out, self.inp, self.finished)
        self.menu = Menu()

    def test_on_online_mode(self):
        self.manual_agent_handler.agent.set_agent_word2vec_model_online = MagicMock()
        self.manual_agent_handler.on_online_mode()
        self.manual_agent_handler.agent.set_agent_word2vec_model_online.assert_called_once()

    def test_on_offline_mode(self):
        self.manual_agent_handler.agent.set_host_model = MagicMock()
        self.manual_agent_handler.on_offline_mode()
        self.manual_agent_handler.agent.set_host_model.assert_called_once()

    def test_start_menu(self):
        self.manual_agent_handler.busy_choose = MagicMock(side_effect=['1', '3'])

        self.assertTrue(self.manual_agent_handler.start_menu())
        self.assertFalse(self.manual_agent_handler.start_menu())

    @patch('builtins.input', side_effect=['1', '2', '4'])
    def test_algorith_graph(self, input):
        self.menu.start_menu()
        path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
        path = os.path.join(path, "New_Service", "Reports_output", "algorithm_stat", "multi-lateration")
        self.assertTrue(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
