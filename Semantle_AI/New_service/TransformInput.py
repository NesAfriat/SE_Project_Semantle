import json


# Define a function to read the configurations from the JSON file
def read_configurations(file_path):
    with open(file_path, "r") as f:
        configurations = json.load(f)
    return configurations


# Define the file path for the JSON file
def transform_input(config_file_path):
    # Read the configurations from the JSON file
    configurations = read_configurations(config_file_path)

    # Create a list to hold the games
    games = []

    # Iterate through the configurations and extract the game data
    for config in configurations:

        game = {
            "agent": config["agent"],
            "host": config["host"],
            "distance_function": config["distance_function"],
            "error": config["error"],
            "calc_error": config["calc_error"],
            "agent_model": config["agent_model"],
            "host_model": config["host_model"],
            "algorithm": config["algorithm"],
            "algorithm_list": config["algorithm_list"],
            "runs": config["runs"],
            "game_type": config["game_type"]
        }
        games.append(game)

    # Print the list of games
    print(games)
    return games
