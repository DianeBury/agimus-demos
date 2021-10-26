#!/usr/bin/env python

import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def get_stats(all_times):
    df = pd.DataFrame(all_times)
    stats = {}
    for key in all_times:
        stats[key] = {}
        stats[key]['min'] =  min(all_times[key])
        stats[key]['max'] =  max(all_times[key])
        stats[key]['mean'] =  sum(all_times[key]) / len(all_times[key])
    return stats

def plot_hist(all_times, key):
    print(key)
    data = all_times[key]
    plt.hist(data, bins=100)
    plt.show()
    
def plot_box(all_times):
    cases = ['Basic', 'Sorting', 'Vmax', 'Memory', 'Complete']
    data = [all_times[key] for key in cases]
    fig, ax = plt.subplots()
    ax.set_title('Number of iterations per path')
    
    meanpointprops = dict(marker='D', markerfacecolor='green', markersize=12)

    ax.boxplot(data, showmeans=True, meanprops=meanpointprops)
    plt.yscale('log')
    plt.xticks(range(1,6), cases)
    plt.rcParams.update({'font.size':22})
    plt.show()

def pretty_dict_string(dico, indent=0, output=None):
    pretty_string = ""
    for key, value in dico.items():
        if type(value) is dict:
            pretty_string += '    ' * indent + str(key) + '\n'
            pretty_string += pretty_dict_string(value, indent+1)
        else:
            pretty_string +=  '    ' * indent + str(key) + ' : ' + str(dico[key]) + '\n'
        if indent == 0:
            pretty_string += '\n'
    return pretty_string

def pretty_print_stats(stats):
    if type(stats) is dict:
        for key in stats:
            print(key + "\n")
            pretty_print_stats(stats[key])
    elif type(stats) is list:
        new_stats = pd.DataFrame(stats)
        pretty_print_stats(new_stats)
    elif type(stats) is pd.core.frame.DataFrame:
        print(stats.describe())
        print("")

def find_free_filename(filename0, extension):
    i = 0
    file_ok = False
    while not file_ok:
        if i == 0:
            filename = filename0
        else:
            name = filename0.split(extension)[0]
            filename = name + str(i) + extension
        myfile = Path(filename)
        if myfile.is_file():
            i += 1
        else:
            file_ok = True
    return filename