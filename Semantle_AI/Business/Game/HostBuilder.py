from Semantle_AI.Business import MethodDistances
from Semantle_AI.Business.Hosts.OnlineHost import OnlineHost
from Semantle_AI.Business.Hosts.OfflineHost import OfflineHost
from Semantle_AI.Business.Game.ModelFactory import ModelFactory
from Semantle_AI.Business.Game.AgentBuilder import dict_model


class HostBuilder():
    def __init__(self):
        self.host = None

    def create_host(self, host_type):
        match host_type:
            case "online":
                self.host = OnlineHost()
            case _:
                self.host = OfflineHost()

    def with_model(self, model_name, dist_func_name):
        model, vocab = ModelFactory.get_model(dict_model.get(model_name),dist_func_name)
        self.host.set_model(model, vocab)

    def with_distance_function(self, dist_func):
        if dist_func == "euclid":
            self.host.model.set_dist_function(MethodDistances.euclid_function())
        else:
            self.host.model.set_dist_function(MethodDistances.cosine_function())

    def get_host(self):
        return self.host
