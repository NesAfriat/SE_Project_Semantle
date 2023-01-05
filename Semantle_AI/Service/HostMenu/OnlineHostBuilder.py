from Business.Hosts.OnlineHost import OnlineHost
from Service.HostMenu.HostBuilder import HostBuilder


class OnlineHostBuilder(HostBuilder):

    def __init__(self, out, inp, finished):
        super().__init__(out, inp, finished)
        self.host = OnlineHost()

    def start_menu(self):
        pass
