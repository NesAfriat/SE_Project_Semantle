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
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/algorithms_compare/{time}"
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError:
        pass
    return path


def generate_algorithm_stat_name(algo_name):
    # datetime object containing current date and time
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/algorithm_stat/{algo_name}/{time}"
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError:
        pass
    return path


def generate_noise_compare_name(algo_name):
    # datetime object containing current date and time
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/Noise_compare/{algo_name}/{time}"
    try:
        if os.path.exists(path):
            os.remove(path)
        os.makedirs(path, mode=0o7777)
        print("Directory '% s' created" % path)
    except IOError as e:
        pass
    return path


def generate_error_vector_name(error_method, error_size_method):
    # datetime object containing current date and time
    time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    path = f"./Reports_output/Priority_calculation/{error_method}_{error_size_method}/{time}"
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


def generate_error_graph(results: OrderedDict, runs_number: int, agent: Agent, words_list, model1_name, model2_name,
                         error_method, error_size_method):

    words_list = list(words_list)
    # Create the plot
    fig, ax = plt.subplots()

    # setting the pixels ( full hd = 1920 x 1080 in pixels = 19.2 x 10.8 in inches)
    # setting the pixels ( ultra hd = 3760 x 2160 in pixels = 47 x 27 in inches)
    fig.set_size_inches(19.2, 10.8)
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

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
    ax.scatter(x, y, s=150)

    # setting the plot labels.
    ax.set_xlabel('Run number', fontsize=30)
    ax.set_ylabel('Guesses until win', fontsize=30)
    ax.set_title(f'Guesses per run', fontsize=30)

    # setting ticks for each axis.
    x_tick = get_natural_numbers(x_min, x_max)
    plt.xticks(x_tick, fontsize=10)
    y_ticks = get_natural_numbers(y_min, y_max)
    plt.yticks(y_ticks, fontsize=10)

    # # adjusting the plot to the pixels size.
    # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

    # getting the dir and file name.
    dir_name = generate_error_vector_name(error_method, error_size_method)

    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # setting dir and file name, and saving the csv files.
    filename = f"{dir_name}/{runs_number}_{error_method}_{error_size_method}_" \
               f"{model1_name}_{model2_name}_PriorityCompare.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["RunNumber", "GuessTillWin", "Word"])
        counter = 0
        for (run, guess) in results.items():
            writer.writerow([run, guess, words_list[counter]])
            counter += 1

    # Save plot as png file
    filename = f"{dir_name}/{runs_number}_{error_method}{error_size_method}_" \
               f"{model1_name}_{model2_name}_PriorityCompare.png"
    plt.savefig(filename)

    # Show plot
    plt.show()
    return None


def generate_noises_graph_spread(results: OrderedDict, algo_name: str, runs_number: int, dist_name):
    # Create the plot
    fig, ax = plt.subplots()

    # setting the pixels ( full hd = 1920 x 1080 in pixels = 19.2 x 10.8 in inches)
    # setting the pixels ( full hd = 3760 x 2160 in pixels = 47 x 27 in inches)
    fig.set_size_inches(19.2, 10.8)
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    x_min = 100
    x_max = 0
    y_min = 100
    y_max = 0

    # iterating over all noises. for each one we will create another graph.
    for i, (noise, res_list) in enumerate(results.items()):
        if noise < x_min:
            x_min = noise
        if noise > x_max:
            x_max = noise
        lst = [round((noise - 1.0) * 100, 1)]
        x = [a for a in lst for i in range(len(res_list))]
        y = [num for num in res_list]
        tmp = min(y)
        if tmp < y_min:
            y_min = tmp
        tmp = max(y)
        if tmp > y_max:
            y_max = tmp
        color = color_cycle[i % len(color_cycle)]
        # ax.plot(x, y, label=f'{noise}', linewidth=2.0, alpha=0.7, marker='o', markersize=4, fontsize = 30)
        ax.scatter(x, y, color=color, s=150, label=f"{noise}%")

    # setting the plot labels.
    ax.set_xlabel('Noise value', fontsize=30)
    ax.set_ylabel('Guesses until win', fontsize=30)

    # setting ticks for each axis.
    x_tick = generate_x_values(round((x_min - 1.0) * 100, 1), round((x_max - 1.0) * 100, 1))
    plt.xticks(x_tick, fontsize=10)
    y_ticks = generate_y_values(y_min, y_max)
    plt.yticks(y_ticks, fontsize=10)

    # # adjusting the plot to the pixels size.
    # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

    # getting the dir and file name.
    dir_name = generate_noise_compare_name(algo_name)

    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # setting dir and file name, and saving the csv files.
    filename = f"{dir_name}/{algo_name}_{runs_number}_{dist_name}_NoiseCompare.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Noise", "GuessTillWin", "RunNumber"])
        counter = 0
        for noise in results.keys():
            counter += 1
            for result in results[noise]:
                noise2 = round((noise - 1.0) * 100, 1)
                writer.writerow([noise2, result, counter])

    # Save plot as png file
    filename = f"{dir_name}/{algo_name}_{runs_number}_{dist_name}_NoiseCompare.png"
    plt.savefig(filename)

    # Show plot
    plt.show()
    return None


def generate_noises_graph_avg(results: OrderedDict, algo_name: str, runs_number: int, dist_name):
    points = OrderedDict()

    # iterate over the vals and check average for each noise value.
    for noise in results.keys():
        guesses_counter = 0
        guesses_sum = 0

        # pass each noise values and calculate the avg.
        for guess_num in results[noise]:
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
    plt.yticks(y_ticksתfontsize=10)

    # adjusting the plot to the pixels size
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

    # getting the dir and file name.
    dir_name = generate_noise_compare_name(algo_name)

    # Create directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # setting dir and file name, and saving the csv files.
    filename = f"{dir_name}/{algo_name}_{runs_number}_{dist_name}_NoiseCompare.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Noise", "GuessNumber"])
        for key in points.keys():
            key2 = round((key - 1.0) * 100, 1)
            writer.writerow([key2, points[key]])

    # Save plot as png file
    filename = f"{dir_name}/{algo_name}_{runs_number}_{dist_name}_NoiseCompare.png"
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


def get_natural_numbers(min_value, max_value):
    natural_numbers = []
    for i in range(min_value, max_value+1):
        natural_numbers.append(i)
    return natural_numbers

