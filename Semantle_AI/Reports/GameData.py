
class GameData():
    def __init__(self ,agent_model,host_model,algorithm,distance_method):
        self.agent_model= agent_model
        self.host_model= host_model
        self.algorithm = algorithm
        self.distance_method = distance_method

        # self.is_online=is_online
        # self.is_won= is_won
        # self.number_total_guesses= number_total_guesses
        # self.num_random_guesses= num_random_guesses
        # self.duration= duration