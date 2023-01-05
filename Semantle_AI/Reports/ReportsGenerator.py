from Reports.GuessData import GuessData
from Reports.GameData import GameData
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime

game_guesses= {} #guesses by game numbers
games_data= {}

#game_extension - duration,is_won,is_online, number_total_guesses,num_random_guesses,duration
#guess extension - semantic_distance,duration_from_last,vocab_words_remain

def save_guess_data(game_number,guess_num,next_guess_num_options):
    guess= GuessData(guess_num,next_guess_num_options)
    if game_number not in game_guesses:
        game_guesses[game_number]= {}
    game_guesses[game_number].append(guess)

def save_game_data(game_number,agent_model_name,host_model_name, algorithm_name, distance_method):
    game= GameData(agent_model_name,host_model_name,algorithm_name,distance_method)
    if game_number not in games_data:
        games_data[game_number]= {}
    games_data[game_number].append(game)



def generate_name():
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H%M")
    return "reports_"+ dt_string


def create_directory():
    # Directory
    directory = generate_name()
    os.mkdir(directory)
    print("Directory '% s' created" % directory)
    return directory


def generate_data_files():
    dir_name= create_directory()
    with open(dir_name+ '/guesses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["guess_No", "remaining_guesses", "game_No"])
        writer.writerow([1, 450, 1])
        writer.writerow([2, 24, 1])
        writer.writerow([3, 1, 1])
        writer.writerow([1, 450, 2])
        writer.writerow([2, 448, 2])
        writer.writerow([3, 443, 2])
        for game_num in game_guesses.keys():
            g_num= game_guesses[game_num].guess_num
            g_rg= game_guesses[game_num].next_guess_num_options
            writer.writerow([g_num, g_rg, game_num])

    with open(dir_name + '/games.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["game_No","agent_model_name","host_model_name", "algorithm"])
        writer.writerow([1, "google", "google", "s-lateration"])
        writer.writerow([2, "nana10", "google", "n-lateration"])


        for game_num in games_data.keys():
            amodel= games_data[game_num].agent_model_name
            hmmodel= games_data[game_num].host_model_name
            algo= games_data[game_num].algorithm_name
            writer.writerow([game_num, amodel, hmmodel, algo])
    return dir_name

def generate_algo_guesses_from_csv():
    dir_name= generate_data_files()
    # Read in the guesses CSV file
    df1 = pd.read_csv(dir_name+"/guesses.csv")
    # Read in the games CSV file
    df2 = pd.read_csv(dir_name+"/games.csv")
    # Merge the two dataframes on the "game_number" column
    df = pd.merge(df1, df2, on="game_No")
    # Group the data by algorithm and get the mean number of remaining words for each algorithm
    grouped_df = df.groupby("algorithm")
    # Get the names of the algorithms
    def extract_values(group):
        return [(row['algorithm'],row['guess_No'], row['remaining_guesses']) for _, row in group.iterrows()]

    algo_results = [extract_values(group) for _, group in grouped_df]

    # Extract the guesses_No and remained_words coordinates and for each algorithm
    guesses_No, remained_gusses = zip(*[(x,y) for (algo,x,y) in algo_results[0]])
    algo1 = algo_results[0][0][0]
    x2, y2 = zip(*[(x,y) for (algo,x,y) in algo_results[1]])
    algo2 = algo_results[1][0][0]

    # Create a figure and a subplot
    fig, ax = plt.subplots()
    # Plot the points for each list on the subplot
    ax.plot(guesses_No, remained_gusses, 'o-', color='orange', label=algo1)
    ax.plot(x2, y2, 'o-', color='blue', label=algo2)
    # Add a legend and show the plot
    ax.legend()
    plt.show()



