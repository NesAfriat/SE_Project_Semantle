# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cProfile
import pstats
import pandas as pd
from Semantle_AI.New_service.Menu import Menu
import openpyxl

def main():
    menu = Menu()
    menu.start_menu()


def main_func():
    menu = Menu()
    menu.start_menu()


if __name__ == '__main__':

    run_profiler = False
    if run_profiler:
        # Configuring the sProfile
        profiler = cProfile.Profile()
        profiler.enable()

    main_func()

    if run_profiler:
        # made for saving the stats from cprofile
        profiler.disable()

        stats_file = 'profile_results.pstat'
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.dump_stats(stats_file)

        p = pstats.Stats(stats_file)
        rows = []
        for func, info in p.stats.items():

            current_row = []
            current_row.append(func)  # function name
            current_row.extend(info[:4])  # cc, nc, tt, ct
            rows.append(current_row)

        df = pd.DataFrame(rows, columns=['function', 'callsCount', 'numCalls', 'totalTime', 'cumtime'])
        df.to_excel('profile_results.xlsx')
