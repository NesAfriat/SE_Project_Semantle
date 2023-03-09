import errno
from matplotlib import pyplot as plt
from Business.Reports.GuessData import GuessData
from Business.Reports.GameData import GameData
import os
import csv
from matplotlib.ticker import MultipleLocator
from datetime import datetime
from collections import Counter
from typing import Set

game_guesses = {}  # guesses by game numbers
games_data = {}


def save_guess_data(game_number, guess_num, next_guess_num_options):
    guess = GuessData(guess_num, next_guess_num_options)
    if game_number not in game_guesses:
        game_guesses[game_number] = list()
    game_guesses[game_number].append(guess)


def save_game_data(game_number, agent_model_name, host_model_name, algorithm_name, distance_method):
    game = GameData(agent_model_name, host_model_name, algorithm_name, distance_method)
    games_data[game_number] = game


def generate_algorithms_compare_name():
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/algorithms_compare/{time}"
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError as e:
        pass
    return path


def generate_algorithm_stat_name(algo_name):
    # datetime object containing current date and time
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/algorithm_stat_{algo_name}/{time}"
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError as e:
        pass
    return path


def generate_data_files():
    dir_name = generate_algorithms_compare_name()
    with open(dir_name + '/guesses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["guess_No", "remaining_guesses", "game_No"])
        for game_num in game_guesses.keys():
            for gs_num in game_guesses[game_num]:
                g_num = gs_num.guess_num
                g_rg = gs_num.next_guess_num_options
                writer.writerow([g_num, g_rg, game_num])

    with open(dir_name + '/games.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["game_No", "agent_model_name", "host_model_name", "algorithm"])
        for game_num in games_data.keys():
            amodel = games_data[game_num].agent_model
            hmmodel = games_data[game_num].host_model
            algo = games_data[game_num].algorithm
            writer.writerow([game_num, amodel, hmmodel, algo])
    return dir_name


def generate_algo_guesses_from_csv(path):
    guesses_file_path = os.path.join(path, 'guesses.csv')
    games_file_path = os.path.join(path, 'games.csv')

    # Load game data from csv
    games_data_tmp = {}
    with open(games_file_path, newline='') as games_file:
        reader = csv.reader(games_file)
        next(reader)  # skip header
        for row in reader:
            game_num = int(row[0])
            agent_model_name = row[1]
            host_model_name = row[2]
            algorithm_name = row[3]
            games_data_tmp[game_num] = {
                'agent_model_name': agent_model_name,
                'host_model_name': host_model_name,
                'algorithm_name': algorithm_name,
                'guesses': []
            }

    # Load guess data from csv
    with open(guesses_file_path, newline='') as guesses_file:
        reader = csv.reader(guesses_file)
        next(reader)  # skip header
        for row in reader:
            guess_num = int(row[0])
            remaining_guesses = int(row[1])
            game_num = int(row[2])
            games_data_tmp[game_num]['guesses'].append((guess_num, remaining_guesses))

    # Plot guesses by game
    fig, ax = plt.subplots()
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    for i, (game_num, game_data) in enumerate(games_data_tmp.items()):
        guesses = game_data['guesses']
        algorithm_name = game_data['algorithm_name']
        x = [guess[0] for guess in guesses]
        y = [guess[1] for guess in guesses]
        color = color_cycle[i % len(color_cycle)]
        ax.plot(x, y, label=f'{algorithm_name}', color=color, linewidth=2.0, alpha=0.7, marker='o', markersize=4)

    ax.set_xlabel('Guess Number', fontsize=12)
    ax.set_ylabel('Remaining Guesses', fontsize=12)
    ax.legend(fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
    plt.show()


def generate_graph(filtered_keys: Set[str], algo_name: str, runs_number: int):
    # Count the frequency of each value in the filtered keys
    value_counts = Counter(filtered_keys)
    total = sum(value_counts.values())

    # Calculate the percentage of each value and sort by value
    percentages = {}
    for k, v in value_counts.items():
        percentages[k] = v / total * 100

    # Convert the percentages to a list of (value, percentage) tuples
    points = list(percentages.items())
    points.sort(key=lambda x: x[0])

    # Create the plot
    fig, ax = plt.subplots()
    ax.scatter([p[0] for p in points], [p[1] for p in points], s=5)

    # Set the title and axis labels
    ax.set_title(f"Algorithm {algo_name} Results")
    ax.set_xlabel("Guess Value")
    ax.set_ylabel("Percentage")

    # Set the x-axis to display only natural number ticks
    ax.xaxis.set_major_locator(MultipleLocator(0.5))

    # Save plot points to csv file
    dir_name = generate_algorithm_stat_name(algo_name)
    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    filename = f"{dir_name}/{algo_name}_{runs_number}_LGD.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Value", "Percentage"])
        for p in points:
            writer.writerow([p[0], p[1]])

    # Save plot as png file
    filename = f"{dir_name}/{algo_name}_{runs_number}_LGD.png"
    plt.savefig(filename)
    # Show plot
    plt.show()


def set_size(w, h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax = plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w) / (r - l)
    figh = float(h) / (t - b)
    ax.figure.set_size_inches(figw, figh)
