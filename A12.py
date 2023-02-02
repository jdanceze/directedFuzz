import itertools as it

from bisect import bisect_left
from typing import List

import numpy as np
import pandas as pd
import scipy.stats as ss

from pandas import Categorical


def VD_A(treatment: List[float], control: List[float]):
    """
    Computes Vargha and Delaney A index
    A. Vargha and H. D. Delaney.
    A critique and improvement of the CL common language
    effect size statistics of McGraw and Wong.
    Journal of Educational and Behavioral Statistics, 25(2):101-132, 2000
    The formula to compute A has been transformed to minimize accuracy errors
    See: http://mtorchiano.wordpress.com/2014/05/19/effect-size-of-r-precision/
    :param treatment: a numeric list
    :param control: another numeric list
    :returns the value estimate and the magnitude
    """
    m = len(treatment)
    n = len(control)

    if m != n:
        raise ValueError("Data d and f must have the same length")

    r = ss.rankdata(treatment + control)
    r1 = sum(r[0:m])

    # Compute the measure
    # A = (r1/m - (m+1)/2)/n # formula (14) in Vargha and Delaney, 2000
    A = (2 * r1 - m * (m + 1)) / (2 * n * m)  # equivalent formula to avoid accuracy errors

    levels = [0.147, 0.33, 0.474]  # effect sizes from Hess and Kromrey, 2004
    magnitude = ["negligible", "small", "medium", "large"]
    scaled_A = (A - 0.5) * 2

    magnitude = magnitude[bisect_left(levels, abs(scaled_A))]
    estimate = A

    return estimate, magnitude


def VD_A_DF(data, val_col: str = None, group_col: str = None, sort=True):
    """
    :param data: pandas DataFrame object
        An array, any object exposing the array interface or a pandas DataFrame.
        Array must be two-dimensional. Second dimension may vary,
        i.e. groups may have different lengths.
    :param val_col: str, optional
        Must be specified if `a` is a pandas DataFrame object.
        Name of the column that contains values.
    :param group_col: str, optional
        Must be specified if `a` is a pandas DataFrame object.
        Name of the column that contains group names.
    :param sort : bool, optional
        Specifies whether to sort DataFrame by group_col or not. Recommended
        unless you sort your data manually.
    :return: stats : pandas DataFrame of effect sizes
    Stats summary ::
    'A' : Name of first measurement
    'B' : Name of second measurement
    'estimate' : effect sizes
    'magnitude' : magnitude
    """

    x = data.copy()
    if sort:
        x[group_col] = Categorical(x[group_col], categories=x[group_col].unique(), ordered=True)
        x.sort_values(by=[group_col, val_col], ascending=True, inplace=True)

    groups = x[group_col].unique()

    # Pairwise combinations
    g1, g2 = np.array(list(it.combinations(np.arange(groups.size), 2))).T

    # Compute effect size for each combination
    ef = np.array([VD_A(list(x[val_col][x[group_col] == groups[i]].values),
                        list(x[val_col][x[group_col] == groups[j]].values)) for i, j in zip(g1, g2)])

    return pd.DataFrame({
        'A': np.unique(data[group_col])[g1],
        'B': np.unique(data[group_col])[g2],
        'estimate': ef[:, 0],
        'magnitude': ef[:, 1]
    })


if __name__ == '__main__':

    i_skipfuzz_go = [37,68,193,245,103,259,49,22,143,253,28,318,189,50000,155,104,746,213,11,257]
    time_skipfuzz_go = [82,87,102,117,76,117,80,76,93,114,78,131,111,3600,96,82,251,108,76,82]

    i_skipfuzz = [193,139,13,207,281,185,10,158,50000,417,234,106,172,125,207,40,353,81,50000,194]
    time_skipfuzz = [108,94,78,113,106,110,83,108,3600,174,117,97,104,95,116,82,143,91,3600,120]

    time_skipfuzz_go_scatter = [77,80,79,77,109,74,120,78,106,75,79,75,78,75,73,88,72,87,73,81]
    time_skipfuzz_scatter = [70,73,71,72,70,89,72,88,70,80,71,73,71,69,72,70,71,69,75,71]

    time_skipfuzz_go_concat = [76,76,82,76,76,75,74,73,100,74,75,80,75,76,85,89,90,83,81,76]
    time_skipfuzz_concat = [74,76,80,85,79,80,109,88,80,88,82,82,84,80,84,92,80,83,72,73]

    time_skipfuzz_go_extract = [90,675,3600,3600,3600,3600,3600,3600,80,3600,3600,178,3600,338,578,348,152,230,1417,3600]
    time_skipfuzz_extract = [133,366,469,90,1143,3600,1883,236,129,3600,404,366,1288,130,3600,873,3600,1889,285,729]

    time_skipfuzz_go_composite = [85.4,93,74,74,94,90,93,89,81,81,76,83,75,86,87,80,88,87,78,111,88]
    time_skipfuzz_composite = [96.55,85,85,107,122,84,93,89,90,125,154,92,87,82,83,82,86,95,87,83,120]

    time_skipfuzz_go_sobol = [87,117,3600,95,91,185,84,83,85,92,124,113,83,95,144,135,3600,3600,3600,3600]
    time_skipfuzz_sobol = [113,94,86,88,85,87,101,103,84,85,172,101,105,89,86,83,92,83,114,92]

    time_skipfuzz_go_pyfunc = [759,97,188,89,237,175,3600,1829,359,907,292,173,493,601,3600,129,127,241,3600,310]
    time_skipfuzz_pyfunc = [3600,3600,1161,826,1561,121,1370,272,324,3600,3600,657,510,1071,700,991,3600,189,243,509]

    time_skipfuzz_go_outer = [157,93,95,96,94,99,97,98,97,95,102,95,156,96,98,99,97,111,100,97]
    time_skipfuzz_outer = [123,104,111,122,151,110,77,80,96,146,78,110,116,100,106,101,103,81,106,111]

    # estimate_i, magnitude_i = VD_A(i_skipfuzz_go, i_skipfuzz)
    # print("A12-i: ", 1 - estimate_i)
    
    estimate_time, magnitude_time = VD_A(time_skipfuzz_go_sobol, time_skipfuzz_sobol)
    print("A12-time: ", 1 - estimate_time)

    #print("scatter: ",ss.mannwhitneyu(x = time_skipfuzz_go_scatter, y = time_skipfuzz_scatter, alternative='less'))
    print("Concat: ",ss.mannwhitneyu(x = time_skipfuzz_go_concat, y = time_skipfuzz_concat, alternative='less'))
    print("extract: ",ss.mannwhitneyu(x = time_skipfuzz_go_extract, y = time_skipfuzz_extract, alternative='less'))
    print("composite: ",ss.mannwhitneyu(x = time_skipfuzz_go_composite, y = time_skipfuzz_composite, alternative='less'))
    print("sobol: ",ss.mannwhitneyu(x = time_skipfuzz_go_sobol, y = time_skipfuzz_sobol, alternative='less'))
    print("pyfunc: ",ss.mannwhitneyu(x = time_skipfuzz_go_pyfunc, y = time_skipfuzz_pyfunc, alternative='less'))
    print("outer: ",ss.mannwhitneyu(x = time_skipfuzz_go_outer, y = time_skipfuzz_outer, alternative='less'))