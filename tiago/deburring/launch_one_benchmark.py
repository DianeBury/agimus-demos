#!/usr/bin/env python

import os, sys, time
import cv_benchmark as benchmark
import glob
from hpp.corbaserver.manipulation import Robot, loadServerPlugin, createContext, newProblem, ProblemSolver, ConstraintGraph, Rule, Constraints, CorbaClient
from hpp.gepetto.manipulation import ViewerFactory
import analyse_log
import util
import numpy as np

devel_dir = "/root/catkin_ws/"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Input error")
    else:
        method = sys.argv[1]
        time_step = 0
        if method.lower() == "discrete":
            time_step = float(sys.argv[2])
            print("Time step = " + str(time_step))
        ps, base_order, base_paths, clusters_path = benchmark.run(method, time_step)
        log_path = devel_dir + 'install/var/log/hpp/benchmark*.log'
        list_of_files = glob.glob(log_path)
        if len(list_of_files) == 0:
            print("No log file in " + log_path)
            print("Is logging activated ?")
        else:
            latest_file = max(list_of_files, key=os.path.getctime)
            pid = latest_file.split('benchmark.')[1].split('.log')[0]
            new_filename = devel_dir + 'src/agimus-demos/tiago/deburring/data/benchmark_' + method.lower() + '_' + pid + '.log'
            print("Moving log file (" + latest_file + ") to data folder (" + new_filename + ")")
            os.rename(latest_file, new_filename)
            counts, stats = analyse_log.analyse(new_filename, [time_step])
            util.pretty_print_stats(stats)