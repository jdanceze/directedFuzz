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


    time_skipfuzz_go_scatter = [230,181,178,172,178,176,180,176,173,172,172,167,173,173,177,186,173,3600,166,172]
    time_skipfuzz_scatter = [176,182,172,179,176,172,171,172,168,179,177,172,174,173,172,182,179,174,174,175]
    time_skipfuzz_go_ninv_scatter = [167,171,172,172,181,175,172,171,173,173,181,181,173,172,170,172,179,173,181,175]

    time_skipfuzz_go_concat = [70,71,72,71,71,71,72,72,73,71,72,88,71,71,71,72,71,71,72,71]
    time_skipfuzz_concat = [71,72,72,70,70,72,74,70,70,72,71,72,92,72,72,73,72,70,71,70]
    time_skipfuzz_go_ninv_concat = [71,72,71,72,69,70,71,69,73,72,70,71,70,70,70,68,69,70,73,72]
    time_skipfuzz_go_ns_concat = [72, 70, 70, 69, 70, 69, 71, 70, 71, 71, 73, 70, 71, 72, 70, 87, 69, 71, 73, 71]

    time_skipfuzz_go_extract = [130,83,3600,100,3600,3600,79,3600,3600,3600,112,3600,75,153,102,3600,3600,3600,77,108]
    time_skipfuzz_extract = [3600,162,3600,207,176,102,94,3600,72,83,87,132,187,152,3600,100,141,3600,3600,72]
    time_skipfuzz_go_ninv_extract = [174,106,136,112,3600,132,102,81,73,114,93,214,98,90,3600,83,81,121,107,206]
    time_skipfuzz_go_ns_extract = [3600, 243, 162, 177, 87, 107, 135, 92, 125, 127, 149, 81, 146, 87, 3600, 179, 124, 110, 179, 76]

    time_skipfuzz_go_sobol = [75,89,74,79,70,74,76,74,75,75,74,77,77,73,76,80,74,83,83,72]
    time_skipfuzz_sobol = [79,80,75,74,83,79,84,90,76,80,81,78,81,80,76,78,85,76,80,84]
    time_skipfuzz_go_ninv_sobol = [74,72,76,95,76,72,77,78,74,72,77,73,77,75,78,74,80,75,84,71]

    time_skipfuzz_go_composite = [76,74,71,73,74,90,71,72,72,73,72,72,74,72,71,72,72,72,72,71]
    time_skipfuzz_composite = [72,80,74,98,71,77,89,94,77,68,69,77,74,75,86,76,69,73,71,91]
    time_skipfuzz_go_ninv_composite = [80,74,75,72,73,71,71,73,72,73,77,72,73,72,71,72,75,73,73,72]
    time_skipfuzz_go_ns_composite = [76, 73, 73, 78, 74, 75, 75, 73, 73, 71, 80, 96, 72, 90, 76, 80, 75, 77, 72, 73]

    time_skipfuzz_go_pyfunc = [3600,103,103,3600,78,101,79,89,86,3600,78,3600,3600,96,93,3600,89,3600,3600,3600]
    time_skipfuzz_pyfunc = [220,98,181,185,181,103,124,110,73,77,104,212,208,328,84,3600,193,167,317,157]
    time_skipfuzz_go_ninv_pyfunc = [110,139,110,82,161,80,110,107,85,91,118,78,120,193,3600,93,161,87,139,87]
    time_skipfuzz_go_ns_pyfunc= [82, 84, 73, 145, 74, 140, 154, 193, 171, 78, 108, 77, 130, 118, 147, 162, 261, 187, 109, 97]

    time_skipfuzz_go_outer = [108,86,103,84,101,114,103,111,74,90,90,90,91,90,71,92,71,91,72,88]
    time_skipfuzz_outer = [92,72,96,90,89,90,90,90,70,90,88,89,73,89,90,88,70,89,93,90]
    time_skipfuzz_go_ninv_outer = [89,92,89,88,90,90,70,91,70,70,69,73,71,92,89,91,70,71,89,150]

    time_skipfuzz_poisson = [1058,3600,3600,1663,3600,3600,1127,1177,320,932,3600,3600,1361,1199,1372,482,3600,3600,3600,3600]
    time_skipfuzz_go_ninv_poisson = [998,332,3600,3600,3600,3600,3600,3600,3600,986,3600,3600,3600,3600,3600,3600,3600,3600,1342,3600]
    time_skipfuzz_go_ns_poission = [877, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 863, 3600, 265, 3600, 3600, 1248, 3600, 3600, 3600, 3600]

    time_skipfuzz_broadcast = [3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600]
    time_skipfuzz_go_ninv_broadcast = [3600,3600,373,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600,3600]

    time_skipfuzz_tensorlistresize = [72, 70, 72, 69, 71, 70, 71, 71, 71, 71, 73, 73, 72, 74, 72, 70, 69, 71, 74, 72]
    time_skipfuzz_go_ninv_tensorlistresize = [71, 70, 74, 72, 72, 72, 74, 72, 75, 73, 72, 72, 70, 72, 69, 73, 70, 72, 74, 69]

    # estimate_i, magnitude_i = VD_A(i_skipfuzz_go, i_skipfuzz)
    # print("A12-i: ", 1 - estimate_i)
    
    estimate_time_scatter, magnitude_time_scatter = VD_A(time_skipfuzz_go_ninv_scatter, time_skipfuzz_scatter)
    print("A12-time Scatter: ", 1 - estimate_time_scatter)

    estimate_time_Concat, magnitude_time_Concat = VD_A(time_skipfuzz_go_ns_concat, time_skipfuzz_concat)
    print("A12-time Concat: ", 1 - estimate_time_Concat)

    estimate_time_extract, magnitude_time_extract = VD_A(time_skipfuzz_go_ns_extract, time_skipfuzz_extract)
    print("A12-time extract: ", 1 - estimate_time_extract)

    estimate_time_sobol, magnitude_time_sobol = VD_A(time_skipfuzz_go_ninv_sobol, time_skipfuzz_sobol)
    print("A12-time sobol: ", 1 - estimate_time_sobol)

    estimate_time_composite, magnitude_time_composite = VD_A(time_skipfuzz_go_ns_composite, time_skipfuzz_composite)
    print("A12-time composite: ", 1 - estimate_time_composite)

    estimate_time_pyfunc, magnitude_time_pyfunc = VD_A(time_skipfuzz_go_ns_pyfunc, time_skipfuzz_pyfunc)
    print("A12-time pyfunc: ", 1 - estimate_time_pyfunc)

    estimate_time_outer, magnitude_time_outer = VD_A(time_skipfuzz_go_outer, time_skipfuzz_outer)
    print("A12-time outer: ", 1 - estimate_time_outer)

    estimate_time_poisson, magnitude_time_poisson = VD_A(time_skipfuzz_go_ninv_poisson, time_skipfuzz_poisson)
    print("A12-time poisson: ", 1 - estimate_time_poisson)

    estimate_time_broadcast, magnitude_time_vroadcast = VD_A(time_skipfuzz_go_ninv_broadcast, time_skipfuzz_broadcast)
    print("A12-time broadcast: ", 1 - estimate_time_broadcast)

    estimate_time_tensorlistresize, magnitude_time_tensorlistresize = VD_A(time_skipfuzz_go_ninv_tensorlistresize, time_skipfuzz_tensorlistresize)
    print("A12-time tensor list resize: ", 1 - estimate_time_tensorlistresize)

    print("scatter: ",ss.mannwhitneyu(x = time_skipfuzz_go_ninv_scatter, y = time_skipfuzz_scatter, alternative='greater'))
    print("Concat: ",ss.mannwhitneyu(x = time_skipfuzz_go_ns_concat, y = time_skipfuzz_concat, alternative='less'))
    print("extract: ",ss.mannwhitneyu(x = time_skipfuzz_go_ns_extract, y = time_skipfuzz_extract, alternative='less'))
    print("sobol: ",ss.mannwhitneyu(x = time_skipfuzz_go_ninv_sobol, y = time_skipfuzz_sobol, alternative='less'))
    print("composite: ",ss.mannwhitneyu(x = time_skipfuzz_go_ns_composite, y = time_skipfuzz_composite, alternative='less'))
    print("pyfunc: ",ss.mannwhitneyu(x = time_skipfuzz_go_ns_pyfunc, y = time_skipfuzz_pyfunc, alternative='less'))
    print("outer: ",ss.mannwhitneyu(x = time_skipfuzz_go_outer, y = time_skipfuzz_outer, alternative='less'))
    print("poisson: ",ss.mannwhitneyu(x = time_skipfuzz_go_ninv_poisson, y = time_skipfuzz_poisson, alternative='greater'))
    print("broadcast: ",ss.mannwhitneyu(x = time_skipfuzz_go_ninv_broadcast, y = time_skipfuzz_broadcast, alternative='less'))
    print("tensor list resize: ",ss.mannwhitneyu(x = time_skipfuzz_go_ninv_tensorlistresize, y = time_skipfuzz_tensorlistresize, alternative='less'))
