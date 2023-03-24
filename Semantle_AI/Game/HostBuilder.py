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

    def with_model(self, model):
        pass

    def get_host(self):
        return self.host