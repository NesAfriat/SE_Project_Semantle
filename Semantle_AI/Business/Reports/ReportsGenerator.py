from matplotlib import pyplot as plt
from Business.Agents.Agent import Agent
from Business.Reports.GuessData import GuessData
from Business.Reports.GameData import GameData
import os
import csv
from matplotlib.ticker import MultipleLocator
from datetime import datetime
from collections import Counter, OrderedDict
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
    time, cwd = getTimeAndCwd()
    path = os.path.join(cwd, "Service", "Reports_output", "algorithms_compare")
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError:
        pass
    return path,time


def generate_algorithm_stat_name(algo_name):
    # datetime object containing current date and time
    time, cwd = getTimeAndCwd()
    path = os.path.join(cwd, "Service", "Reports_output", "algorithm_stat", algo_name)
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError:
        pass
    return path,time


def getTimeAndCwd():
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    cwd = os.getcwd()
    return time, cwd


def generate_noise_compare_name(algo_name, withQueue):
    # datetime object containing current date and time
    time, cwd = getTimeAndCwd()
    path = os.path.join(cwd, "Service", "Reports_output", "Noise_compare", f"Queue={withQueue}", algo_name)
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError as e:
        pass
    return path,time


def generate_error_vector_name(error_method, error_size_method):
    # datetime object containing current date and time
    time, cwd = getTimeAndCwd()
    path = os.path.join(cwd, "Service", "Reports_output", "Priority_calculation", f"{error_method}_{error_size_method}")
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError:
        pass
    return path, time


def generate_data_files():
    path, time = generate_algorithms_compare_name()
    dir_name = os.path.join(path, time)
    with open(os.path.join(dir_name, "guesses.csv"), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["guess_No", "remaining_guesses", "game_No"])
        for game_num in game_guesses.keys():
            for gs_num in game_guesses[game_num]:
                g_num = gs_num.guess_num
                g_rg = gs_num.next_guess_num_options
                writer.writerow([g_num, g_rg, game_num])

    with open(os.path.join(dir_name, " games.csv"), 'w', newline='') as file:
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


def generate_error_graph(results: OrderedDict, runs_number: int, words_list, model1_name, model2_name,
                         error_method, error_size_method):
    words_list = list(words_list)
    # Create the plot
    fig, ax = plt.subplots()

    # setting the pixels ( full hd = 1920 x 1080 in pixels = 19.2 x 10.8 in inches)
    # setting the pixels ( ultra hd = 3760 x 2160 in pixels = 47 x 27 in inches)
    fig.set_size_inches(19.2, 10.8)
    # color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    x_min = 100
    x_max = 0
    y_min = 100
    y_max = 0
    x = results.keys()
    y = results.values()
    # iterating over all noises. for each one we will create another graph.
    for (run, max_val) in results.items():
        if run < x_min:
            x_min = run
        if run > x_max:
            x_max = run
        if max_val < y_min:
            y_min = max_val
        if max_val > y_max:
            y_max = max_val
        # color = color_cycle[i % len(color_cycle)]
        # i += 1
    ax.scatter(x, y, s=100)
    x = list(x)
    y = list(y)
    for i, val in enumerate(y):
        ax.annotate(val, xy=(x[i], val), xytext=(x[i], val + 50), ha='center')
    # setting the plot labels.
    ax.set_xlabel('Run number', fontsize=30)
    ax.set_ylabel('Guesses until win', fontsize=30)
    ax.set_title(f'Guesses per run', fontsize=30)

    # setting ticks for each axis.
    x_tick = get_natural_numbers(x_min, x_max)
    plt.xticks(x_tick, fontsize=10)
    y_ticks = generate_y_values_by_range(y_min, y_max)
    plt.yticks(y_ticks, fontsize=10)

    # # adjusting the plot to the pixels size.
    # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

    # getting the dir and file name.
    dir_name, time_stamp = generate_error_vector_name(error_method, error_size_method)
    # setting dir and file name, and saving the csv files.
    filename = os.path.join(dir_name, f"{runs_number}_{error_method}_{error_size_method}",
                            f"{model1_name}_{model2_name}", time_stamp)    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(os.path.join(filename, "PriorityCompare.csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["RunNumber", "GuessTillWin", "Word"])
        counter = 0
        for (run, guess) in results.items():
            writer.writerow([run, guess, words_list[counter]])
            counter += 1

    # Save plot as png file
    plt.savefig(os.path.join(filename, "PriorityCompare.png"))

    # Show plot
    plt.show()
    return None


def generate_noises_graph_spread(results: OrderedDict, algo_name: str, runs_number: int, dist_name, withQueue):
    # getting the dir and file name.
    dir_name, time_stamp = generate_noise_compare_name(algo_name, withQueue)

    dir_name = os.path.join(dir_name, f"algo={algo_name}_runs={runs_number}_dist={dist_name}", time_stamp)
    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # setting dir and file name, and saving the csv files.
    filename = os.path.join(dir_name, "NoiseCompare.csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Noise", "GuessTillWin", "Word"])
        for (noise, gues_dict) in results.items():
            counter = 0
            for (word, guesses) in gues_dict.items():
                writer.writerow([noise, guesses, word])
                counter += 1

    return None


def generate_noises_graph_avg(results: OrderedDict, algo_name: str, runs_number: int, dist_name, withQueue):
    points = OrderedDict()

    # iterate over the vals and check average for each noise value.
    for noise in results.keys():
        guesses_counter = 0
        guesses_sum = 0

        # pass each noise values and calculate the avg.
        for (word, guess_num) in results[noise].items:
            guesses_counter += 1
            guesses_sum += guess_num

        # after finishing all summing. saving the point for the noise.
        points[noise] = guesses_sum / guesses_counter

    # after collecting all points values for every noise. starting to create the graph.
    # Create the plot
    fig, ax = plt.subplots()

    # setting the pixels ( full hd = 1920 x 1080 in pixels = 19.2 x 10.8 in inches)
    fig.set_size_inches(19.2, 10.8)
    ax.scatter([round((err - 1.0) * 100, 1) for err in points.keys()], [points[err] for err in points.keys()], s=30)

    # getting the points x,y values.
    x = []
    y = []
    pos = [10, -10]
    loc = ['bottom', 'top']
    count = 0
    for key, value in points.items():
        key2 = round((key - 1.0) * 100, 1)
        x.append(key2)
        y.append(value)
        ax.annotate(f"{key2}%", xy=(key2, value), xytext=(0, pos[count % 2]),
                    textcoords="offset points",
                    ha='center', va=loc[count % 2])
        count += 1

    # setting ticks for each axis
    x_tick = generate_x_values(min(x), max(x))
    plt.xticks(x_tick, fontsize=10)
    y_ticks = generate_y_values(min(y), max(y))
    plt.yticks(y_ticks, fontsize=10)

    # adjusting the plot to the pixels size
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

    # getting the dir and file name.
    dir_name, time_stamp = generate_noise_compare_name(algo_name, withQueue)
    dir_name = os.path.join(dir_name, f"{algo_name}_{runs_number}_{dist_name}", time_stamp)
    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # setting dir and file name, and saving the csv files.
    filename = os.path.join(dir_name, "NoiseCompare.csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Noise", "GuessNumber", "Words"])
        for key in points.keys():
            result_string = ', '.join(results[key].keys())
            key2 = round((key - 1.0) * 100, 1)
            writer.writerow([key2, points[key], result_string])

    # Save plot as png file
    filename = os.path.join(dir_name, "NoiseCompare.png")
    plt.savefig(filename)

    # Show plot
    plt.show()
    return None


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
    dir_name, time_stamp = generate_algorithm_stat_name(algo_name)
    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    filename = os.path.join(dir_name, f"{algo_name}_{runs_number}", time_stamp, "LGD.csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Value", "Percentage"])
        for p in points:
            writer.writerow([p[0], p[1]])

    # Save plot as png file
    filename = os.path.join(dir_name, f"{algo_name}_{runs_number}", time_stamp, "LGD.png")
    plt.savefig(filename)
    # Show plot
    plt.show()


def generate_x_values(x, y):
    values = []
    current_value = x
    while current_value <= y:
        values.append(current_value)
        current_value += 1.0
    return values


def generate_y_values(x, y):
    values = []
    current_value = x
    while current_value <= y:
        values.append(current_value)
        current_value += 0.5
    return values


def generate_x_values_by_range(x_min, x_max):
    values = []
    current_value = x_min
    jumps = round(x_max - x_min) / 30
    while current_value <= x_max:
        values.append(current_value)
        current_value += jumps
    return values


def generate_y_values_by_range(y_min, y_max):
    values = []
    current_value = y_min
    jumps = round(y_max - y_min) / 30
    while current_value <= y_max:
        values.append(current_value)
        current_value += jumps
    return values


def get_natural_numbers(min_value, max_value):
    natural_numbers = []
    for i in range(min_value, max_value + 1):
        natural_numbers.append(i)
    return natural_numbers
