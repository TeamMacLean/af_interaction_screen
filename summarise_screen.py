#!/usr/bin/env python

'''
Usage:

    This script takes one command-line argument, which is the path to the AF_RUN_DIR directory.
    Run the script using the command: python script_name.py AF_RUN_DIR, where script_name.py is the name of the Python script file.
    Ensure that the necessary input files and directories are available in the AF_RUN_DIR directory before running the script.
    The script retrieves the top-ranked models from each run directory within AF_RUN_DIR.
    It then extracts the 'iptm' and 'ptm' values from the corresponding pickle files.
    The script prints the results in the following format: run_folder, model_name, iptm, ptm.
    If a ranking_debug.json file is not found in a run directory, it will be skipped, and the script continues execution.
    The output is displayed in the console.
'''


import pickle
import os
import sys
import json

def get_best_models(run, top=5):
    """
    Retrieve the top-ranked models from the given run directory.

    Args:
        run (str): Path to the run directory.
        top (int): Number of top-ranked models to retrieve (default: 5).

    Returns:
        list: List of model names.

    Raises:
        FileNotFoundError: If the ranking_debug.json file does not exist in the run directory.
    """
    ranking_debug = os.path.join(run, "ranking_debug.json")
    if not os.path.exists(ranking_debug):
        print("Didn't find {} - skipping".format(ranking_debug), file=sys.stderr)
        return None
    with open(ranking_debug, "r") as fh:
        rankings = json.loads(fh.read())
        return rankings["order"][0:top]

def get_iptm_ptm(p):
    """
    Get the values of 'iptm' and 'ptm' from a pickle file.

    Args:
        p (str): Path to the pickle file.

    Returns:
        tuple: A tuple containing the values of 'iptm' and 'ptm' as floats.
    """
    pkl = pickle.load(open(p, "rb"))
    return (float(pkl['iptm']), float(pkl['ptm']))

def get_pickle_data(md):
    """
    Get the 'iptm' and 'ptm' values for multiple pickle files.

    Args:
        md (tuple): A tuple containing the run directory and a list of model names.

    Returns:
        list: A list of tuples, where each tuple contains the 'iptm' and 'ptm' values for a pickle file.

    Note:
        If the model names list is None, the function will return None.
    """
    if md[1] is None:
        return None
    pkl_paths = [os.path.join(md[0], "result_" + m + ".pkl") for m in md[1]]
    return [get_iptm_ptm(p) for p in pkl_paths]

def print_results(runs, best_models, pkl_data):
    """
    Print the results in the required format.

    Args:
        runs (list): List of run directories.
        best_models (list): List of model names.
        pkl_data (list): List of tuples containing 'iptm' and 'ptm' values.

    Returns:
        None
    """
    print(",".join(["run_folder", "model_name", "iptm", "ptm"]))
    for i in range(len(runs)):
        run = runs[i]
        mods = best_models[i]
        iptm = pkl_data[i]
        if mods is None:
            x = [str(e) for e in [run] + [None] * 3]
            print(",".join(x))
        else:
            for j in range(len(mods)):
                res = [str(e) for e in [run, mods[j], iptm[j][0], iptm[j][1]]]
                print(",".join(res))

def main(AF_RUN_DIR):
    """
    Main entry point of the script.

    Args:
        AF_RUN_DIR (str): Path to the AF_RUN_DIR directory.

    Returns:
        None
    """
    runs = [os.path.join(AF_RUN_DIR, d) for d in os.listdir(AF_RUN_DIR) if os.path.isdir(os.path.join(AF_RUN_DIR, d))]
    best_models = [get_best_models(r) for r in runs]
    pkl_data = [get_pickle_data(md) for md in zip(runs, best_models)]
    print_results(runs, best_models, pkl_data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarise_screen AF_RUN_DIR")
    else:
        AF_RUN_DIR = sys.argv[1]
        main(AF_RUN_DIR)
