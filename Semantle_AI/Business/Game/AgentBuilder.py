from Semantle_AI.Business.Agents.Agent import Agent
from Semantle_AI.Business.Agents.ManualAgent import ManualAgent

dict_model = {'fasttext_wiki': 'fasttext-wiki-news-subwords-300',
              'glove_wiki': "glove-wiki-gigaword-300",
              'word2vec_google': "word2vec-google-news-300",
              'local_word2vec': "Google_Word2Vec.bin"}


class AgentBuilder():
    def __init__(self):
        self.agent = None

    def create_agent_and_model(self, agent_type, host, model_name, model_factory, dist_func_name, host_vocab=None):
        create = False
        self.agent = Agent()
        match agent_type:
            case "agent1":
                self.agent.set_model(host.model)
                create = True
            case "agent2":
                self.with_model(model_factory, model_name, dist_func_name, host_vocab)
                create = True
            case _:
                self.agent = ManualAgent()  # TODO: return regular manual game
        if create:
            print(agent_type, "created")
        else:
            raise ValueError("Agent model set was failed ... bug accure")

    def with_id(self, id):
        self.agent.set_id(id)

    def with_model(self, model_factory, model_name, dist_func_name, host_vocab=None):
        model = model_factory.get_model(dict_model.get(model_name), dist_func_name, host_vocab)
        self.agent.set_model(model)

    def with_algo(self, algo):
        match algo:
            case "multi-lateration":
                self.agent.set_agent_MultiLateration_algorithm()
            case "multi-lateration-agent-2":
                self.agent.set_agent_smart_MultiLateration_algorithm()
            case "n-lateration":
                self.agent.set_agent_nlateration_algorithm()

            case _:
                self.agent.set_agent_naive_algorithm()

    def get_agent(self):
        return self.agent

    def set_host(self, host):
        self.agent.set_host(host)
