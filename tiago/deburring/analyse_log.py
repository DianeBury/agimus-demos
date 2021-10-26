#!/usr/bin/env python

import os, sys
import glob
from util import pretty_dict_string, plot_box
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

devel_dir = os.getenv ('DEVEL_HPP_DIR')

def countPatternBetweenStopper (filename, pattern, stopper):
    res = []
    count = 0
    with open (filename, 'r') as f:
        for line in f:
            if stopper in line:
                if count != 0:
                    res.append(count)
                count = 0
            elif pattern in line:
                count += 1
    if count != 0:
        res.append(count)
    return res

def all_same_value(dico):
    value = None
    for key in dico:
        if value is None:
            value = dico[key]
        elif value != dico[key]:
            return False
    return True

def filename_from_pid(pid):
    filename = devel_dir + '/install/var/log/hpp/benchmark.' + pid + '.log'
    return filename

cases = ['Basic', 'Sorting', 'Vmax', 'Memory', 'Complete']

def analyse(filename=None, time_steps=[]):
    print("Analysing file: " + filename)
    patterns = {c:c+' computeDistanceLowerBound' for c in cases}
    patterns.update( {'Discrete'+str(step): 'Discrete'+str(step)+' computeDistance' for step in time_steps})
    stoppers = {c:c+' new path' for c in cases}
    stoppers.update( {'Discrete'+str(step): 'Discrete'+str(step)+' new path' for step in time_steps} )
    counts = {c:countPatternBetweenStopper(filename, patterns[c], stoppers[c]) for c in patterns}
    counts = {c:counts[c] for c in counts if len(counts[c])>0}
    stats = {c:pd.DataFrame(counts[c]) for c in counts}
    for c in stats:
        print(c)
        print(stats[c].describe())
        print(' ')
    return counts, stats

def add_dict(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key].extend(dict2[key])
        else:
            dict1[key] = dict2[key]

def analyse_all_files(filenames):
    patterns = {c:c+' computeDistanceLowerBound' for c in cases}
    stoppers = {c:c+' new path' for c in cases}
    count_all = {}
    for filename in filenames:
        print("Analysing file " + filename)
        counts = {c:countPatternBetweenStopper(filename, patterns[c], stoppers[c]) for c in cases}
        counts = {c:counts[c] for c in counts if len(counts[c])>0}
        add_dict(count_all, counts)
    stats = {c:pd.DataFrame(count_all[c]) for c in count_all}
    for c in stats:
        print(c)
        print(stats[c].describe())
        print(' ')
    return count_all, stats
    
basic1 = "/root/catkin_ws/src/agimus-demos/tiago/deburring/data/benchmark_basic_32970.log"
sorting1 = "/root/catkin_ws/src/agimus-demos/tiago/deburring/data/benchmark_sorting_37180.log"
vmax1 = "/root/catkin_ws/src/agimus-demos/tiago/deburring/data/benchmark_vmax_36909.log"
vmax2 = "/root/catkin_ws/src/agimus-demos/tiago/deburring/data/benchmark_vmax_22707.log"
memory1 = "/root/catkin_ws/src/agimus-demos/tiago/deburring/data/benchmark_memory_32679.log"
complete1 = "/root/catkin_ws/src/agimus-demos/tiago/deburring/data/benchmark_complete_37946.log"
complete2 = "/root/catkin_ws/src/agimus-demos/tiago/deburring/data/benchmark_complete_36640.log"


if __name__ == '__main__':
    if len(sys.argv) <=1:
        print("Finding most recent log ...")
        list_of_files = glob.glob(devel_dir + '/install/var/log/hpp/*.log')
        if len(list_of_files) == 0:
            print("No log file in " + devel_dir + '/install/var/log/hpp/*.log')
        else:
            latest_file = max(list_of_files, key=os.path.getctime)
            pid = latest_file.split('benchmark.')[1].split('.log')[0]
            print("Latest benchmark log file found: " + pid)
            results, stats = analyse(filename_from_pid(pid))
    else:
        if sys.argv[1] == "all":
            filenames = [basic1, sorting1, vmax1, memory1, complete1]
            print("Analysing all files (" + str(len(filenames)) + " files)" )
            counts, stats = analyse_all_files(filenames)
        else:
            filename = sys.argv[1]
            print("Input file: " + filename)
            results, stats = analyse(filename)