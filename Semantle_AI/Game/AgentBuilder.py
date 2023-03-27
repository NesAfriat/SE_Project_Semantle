from Business.Agents.Agent1 import Agent1
from Business.Agents.Agent2 import Agent2
from Business.Agents.ManualAgent import ManualAgent
from Game import ModelFactory
fasttext_wiki = "fasttext-wiki-news-subwords-300"  # 1GB
glove_wiki = "glove-wiki-gigaword-300"  # 376MB
word2vec_google = "word2vec-google-news-300"  # 1.662GB
local_word2vec = "Google_Word2Vec.bin"

class AgentBuilder():
    def __init__(self):
        self.agent=None

    def create_agent_and_model(self, agent_type,host,model_name,model_factory):
        model = None
        match agent_type:
            case "agent1":
                self.agent= Agent1()
                self.with_model(model_factory,model_name)
            case "agnet2":
                self.agent= Agent2()
                self.with_host_model(host.model)
            case _:
                self.agent= ManualAgent()
                self.with_model(model_factory,model)
        print(agent_type,"created")

    def with_id(self, id):
        self.agent.set_id(self, id)

    def with_model(self, model_factory, model_name):
        model, vocab = model_factory.get_model(model_name)
        self.agent.set_model(model)

    def with_algo(self, algo):
        match algo:
            case "multi-lateration":
                self.agent.set_agent_MultiLateration_algorithm()
            case "n-Lateration":
                self.agent.set_agent_nlateration_algorithm()
            case _:
                self.agent.set_agent_naive_algorithm()

    def get_agent(self):
        return self.agent