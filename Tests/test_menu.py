import unittest
from io import StringIO
from unittest.mock import MagicMock
from Semantle_AI.Business.Agents.ManualAgent import ManualAgent
from Semantle_AI.Service.AgentHandlers.AgentHandler import AgentHandler
from Semantle_AI.Business.MethodDistances import cosine_function
from Semantle_AI.Service.AgentHandlers.ManualAgentHandler import ManualAgentHandler

class TestManualAgentHandler(unittest.TestCase):

    def setUp(self):
        self.out = StringIO()
        self.inp = MagicMock()
        self.finished = MagicMock()
        self.manual_agent_handler = ManualAgentHandler(self.out, self.inp, self.finished)

    def test_on_online_mode(self):
        self.manual_agent_handler.agent.set_agent_word2vec_model_online = MagicMock()
        self.manual_agent_handler.on_online_mode()
        self.manual_agent_handler.agent.set_agent_word2vec_model_online.assert_called_once()

    def test_on_offline_mode(self):
        self.manual_agent_handler.agent.set_host_model = MagicMock()
        self.manual_agent_handler.on_offline_mode()
        self.manual_agent_handler.agent.set_host_model.assert_called_once()

    def test_start_menu(self):
        self.manual_agent_handler.busy_choose = MagicMock(side_effect=['1','3'])

        self.assertTrue(self.manual_agent_handler.start_menu())
        self.assertFalse(self.manual_agent_handler.start_menu())

if __name__ == '__main__':
    unittest.main()
