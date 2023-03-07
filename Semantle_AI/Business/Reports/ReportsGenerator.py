import errno
from matplotlib import pyplot as plt
from Business.Reports.GuessData import GuessData
from Business.Reports.GameData import GameData
import os
import pandas as pd
import csv
from datetime import datetime
from collections import Counter
from typing import Set

game_guesses = {}  # guesses by game numbers
games_data = {}


# game_extension - duration,is_won,is_online, number_total_guesses,num_random_guesses,duration
# guess extension - semantic_distance,duration_from_last,vocab_words_remain

def save_guess_data(game_number, guess_num, next_guess_num_options):
    guess = GuessData(guess_num, next_guess_num_options)
    if game_number not in game_guesses:
        game_guesses[game_number] = list()
    game_guesses[game_number].append(guess)


def save_game_data(game_number, agent_model_name, host_model_name, algorithm_name, distance_method):
    game = GameData(agent_model_name, host_model_name, algorithm_name, distance_method)
    games_data[game_number] = game


def generate_name():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H%M")
    return "reports_" + dt_string


def create_directory():
    # Directory
    directory = generate_name()
    path = "./Reports_output/" + directory
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError as e:
        pass
    return path


def generate_data_files():
    dir_name = create_directory()
    with open(dir_name + '/guesses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["guess_No", "remaining_guesses", "game_No"])
        # writer.writerow([1, 450, 1])
        # writer.writerow([2, 24, 1])
        # writer.writerow([3, 1, 1])
        # writer.writerow([1, 450, 2])
        # writer.writerow([2, 448, 2])
        # writer.writerow([3, 443, 2])
        for game_num in game_guesses.keys():
            for gs_num in game_guesses[game_num]:
                g_num = gs_num.guess_num
                g_rg = gs_num.next_guess_num_options
                writer.writerow([g_num, g_rg, game_num])

    with open(dir_name + '/games.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["game_No", "agent_model_name", "host_model_name", "algorithm"])
        # writer.writerow([1, "google", "google", "s-lateration"])
        # writer.writerow([2, "nana10", "google", "n-lateration"])

        for game_num in games_data.keys():
            amodel = games_data[game_num].agent_model
            hmmodel = games_data[game_num].host_model
            algo = games_data[game_num].algorithm
            writer.writerow([game_num, amodel, hmmodel, algo])
    return dir_name


def generate_algo_guesses_from_csv():
    dir_name = generate_data_files()
    # Read in the guesses CSV file
    df1 = pd.read_csv(dir_name + "/guesses.csv")
    # Read in the games CSV file
    df2 = pd.read_csv(dir_name + "/games.csv")
    # Merge the two dataframes on the "game_number" column
    df = pd.merge(df1, df2, on="game_No")
    # Group the data by algorithm and get the mean number of remaining words for each algorithm
    grouped_df = df.groupby("algorithm")

    try:
        # Get the names of the algorithms
        def extract_values(group):
            return [(row['algorithm'], row['guess_No'], row['remaining_guesses']) for _, row in group.iterrows()]

        algo_results = [extract_values(group) for _, group in grouped_df]

        # Extract the guesses_No and remained_words coordinates and for each algorithm
        x1, y1 = zip(*[(x, y) for (algo, x, y) in algo_results[0]])
        algo1 = algo_results[0][0][0]
        x2, y2 = zip(*[(x, y) for (algo, x, y) in algo_results[1]])
        algo2 = algo_results[1][0][0]
        x3, y3 = zip(*[(x, y) for (algo, x, y) in algo_results[2]])
        algo3 = algo_results[2][0][0]
        # Create a figure and a subplot
        fig, ax = plt.subplots()
        n = max(len(x1), len(x2), len(x3))
        thickness = n/300
        # Plot the points for each list on the subplot
        ax.plot(x1, y1, 'o-', color='orange', label=algo1, linewidth=thickness, markersize=thickness)
        ax.plot(x2, y2, 'o-', color='blue', label=algo2, linewidth=thickness, markersize=thickness)
        ax.plot(x3, y3, 'o-', color='red', label=algo3, linewidth=thickness, markersize=thickness)
        pts_x = n
        pts_y = n
        # resizing the plot by number of points
        set_size(pts_x/200, pts_y/200, ax)
        plt.xticks(fontsize=thickness*2)
        plt.yticks(fontsize=thickness*2)

        # set the axis titles
        # Add a title and axis labels to the chart
        plt.title("Algorithms compare graph")
        plt.ylabel("Remain words")
        plt.xlabel("Number of guesses")

        # Add a legend and show the plot
        ax.legend()
        plt.show()
    except IOError as e:
        if e.errno == errno.EPIPE:
            print("There was pipe error. please try again.")
            pass


def generate_graph(filtered_keys: Set[str], algo_name: str):
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

    # Save plot points to csv file
    dir_name = generate_data_files()
    time = datetime.now().strftime('%Y-%m-%d')
    dir_name = f"{dir_name}/{time}"
    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    filename = f"{dir_name}/{algo_name}_loops_{time}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Value", "Percentage"])
        for p in points:
            writer.writerow([p[0], p[1]])

    # Save plot as png file
    filename = f"{dir_name}/{algo_name}_guess_distribution_{time}.png"
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
