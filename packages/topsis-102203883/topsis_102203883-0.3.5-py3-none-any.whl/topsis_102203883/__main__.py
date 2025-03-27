import pandas as pd
import numpy as np
import sys


def topsis(data, weights, impacts):
    """
    TOPSIS calculation

    parameters:
        data (numpy.ndarray): a 2D array of numeric values (decision matrix)
        weights (list): a list of weights for the criteria
        impacts (list): a list of '+' or '-' indicating benefit or cost criteria

    returns:
        numpy.ndarray: the ranking of alternatives
    """
    
    # normalized decision matrix
    n = data / np.sqrt((data**2).sum(axis=0))

    # weighted normalized matrix
    w = n * weights

    # ideal best and ideal worst
    ideal_b = []
    ideal_w = []
    
    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_b.append(max(w[:, i]))
            ideal_w.append(min(w[:, i]))
        elif impacts[i] == '-':
            ideal_b.append(min(w[:, i]))
            ideal_w.append(max(w[:, i]))
        else:
            raise ValueError("impact must be '+' or '-'")

    ideal_b = np.array(ideal_b)
    ideal_w = np.array(ideal_w)

    # separation measures
    separation_b = np.sqrt(((w - ideal_b) ** 2).sum(axis=1))
    separation_w = np.sqrt(((w - ideal_w) ** 2).sum(axis=1))

    # TOPSIS score
    scores = separation_w / (separation_b + separation_w)

    # 1-based ranking
    ranks =  scores.argsort()[::-1] + 1 
    
    return scores, ranks


def result():
    # command-line arguments
    if len(sys.argv) != 4:
        print("usage: python topsis.py <input_file> <weights> <impacts>")
        sys.exit(1)

    inp_file = sys.argv[1]
    out_file = f"{102203883}-result.csv"
    
    weights = sys.argv[2]
    impacts = sys.argv[3]

    # read the input file
    try:
        data = pd.read_csv(inp_file)
        alternatives = data.iloc[:, 0]
        matrix = data.iloc[:, 1:].values
    except Exception as e:
        print(f"error reading input file: {e}")
        sys.exit(1)

    # parse weights and impacts
    try:
        weights = [float(w) for w in weights.split(',')]
        impacts = impacts.split(',')
    except Exception as e:
        print(f"error parsing weights or impacts: {e}")
        sys.exit(1)

    # validate inputs
    if len(weights) != matrix.shape[1]:
        print("error: number of weights must match the number of criteria.")
        sys.exit(1)
    if len(impacts) != matrix.shape[1]:
        print("error: number of impacts must match the number of criteria.")
        sys.exit(1)

    # perform TOPSIS
    try:
        scores, ranks = topsis(matrix, weights, impacts)
    except Exception as e:
        print(f"error during TOPSIS calculation: {e}")
        sys.exit(1)

    # update the DataFrame
    data['Topsis Score'] = scores
    data['RANK'] = ranks

    # save results
    try:
        data.to_csv(out_file, index=False)
        print(f"results saved to {out_file}")
    except Exception as e:
        print(f"error saving results: {e}")
        sys.exit(1)


if __name__ == "__main__":
    result()