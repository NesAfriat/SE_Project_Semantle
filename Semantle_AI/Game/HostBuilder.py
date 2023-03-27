from Business import MethodDistances
from Business.Hosts.OnlineHost import OnlineHost
from Business.Hosts.OfflineHost import OfflineHost


class HostBuilder():
    def __init__(self):
        self.host=None

    def create_host(self, host_type):
        match host_type:
            case "online":
                self.host= OfflineHost()
            case _:
                self.host= OnlineHost()

    def with_model(self, model_name,model_factory):
            model, vocab= model_factory.get_model(model_name)
            self.host.set_model(model,vocab)

    def with_distace_function(self,dist_func):
            if dist_func == "euclid":
                self.host.model.set_dist_function(MethodDistances.euclid_function())
            else:
                self.host.model.set_dist_function(MethodDistances.cosine_function())

    def get_host(self):
        return self.host