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


    time_skipfuzz_go_pyfunc = [10000, 64, 3181, 10000, 769, 621, 68, 11527, 952, 10000, 1221, 10000, 10000, 2101, 1167, 10000, 404, 10000, 10000, 10000]
    time_skipfuzz_pyfunc = [72, 719, 2461, 2350, 5557, 1119, 4878, 9773, 8111, 2781, 1570, 5329, 1034, 221, 6250, 8643, 3452, 265, 804, 3700]
    time_skipfuzz_go_ninv_pyfunc = [1542, 3116, 1454, 364, 4081, 536, 1915, 1641, 553, 944, 1838, 368, 2187, 5266, 10000, 1007, 3720, 991, 3297, 280]
    time_skipfuzz_go_ns_pyfunc = [249, 414, 38, 3079, 91, 2654, 3596, 6438, 4387, 169, 1422, 124, 2793, 2028, 4101, 3909, 8753, 4390, 1560, 1232]
    time_skipfuzz_go_nd_pyfunc =[5073, 1444, 1132, 1191, 6900, 2901, 414, 531, 6737, 3828, 2275, 2946, 2410, 2195, 4091, 3886, 319, 88, 10000, 77]
    time_skipfuzz_go_bb_ninv_pyfunc = [107, 3260, 107, 2502, 917, 2952, 2972, 1193, 920, 506, 9239, 9964, 1066, 7419, 1333, 1307, 1333, 6354, 441, 1475]
    time_skipfuzz_go_bb_max_pyfunc = [1515, 334, 10000, 151, 694, 10000, 10000, 206, 404, 38, 3222, 647, 734, 10000, 10000, 10000, 4993, 1009, 722, 10000]
    time_skipfuzz_go_bb_ns_pyfunc = [199, 4381, 4313, 1535, 1540, 1787, 887, 540, 2326, 727, 652, 53, 2549, 1513, 1421, 107, 257, 2962, 2189, 661]

    time_skipfuzz_go_scatter = [91, 20, 31, 16, 30, 2, 67, 37, 5, 18, 3, 0, 33, 7, 11, 54, 32, 1, 0, 11]
    time_skipfuzz_scatter = [24, 49, 10, 40, 27, 10, 7, 5, 0, 19, 20, 4, 4, 37, 12, 36, 10, 19, 4, 11]
    time_skipfuzz_scatter_2 = [242, 75, 80, 126, 233, 76, 89, 338, 75, 77, 125, 163, 87, 107, 99, 90, 154, 98, 275, 246]
    time_skipfuzz_go_ninv_scatter = [0, 9, 1, 23, 59, 30, 3, 4, 7, 1, 49, 47, 2, 5, 1, 10, 11, 3, 34, 49]
    #time_skipfuzz_go_ninv_pyfun_2 = [171, 109, 272, 143, 76, 259, 140, 117, 96, 90, 99, 157, 154, 215, 208, 111, 83, 128, 236, 132]
    time_skipfuzz_go_ns_scatter= [4, 11, 83, 35, 13, 16, 12, 3, 43, 22, 20, 59, 31, 22, 10, 44, 28, 2, 3, 8]
    time_skipfuzz_go_bb_max_inv_scatter = [11, 29, 2, 5, 11, 15, 12, 11, 26, 16, 3, 46, 10, 1, 1, 50, 1, 24, 17, 5]
    time_skipfuzz_go_nd_scatter= [49, 44, 2, 2, 24, 40, 30, 21, 8, 34, 1, 2, 6, 73, 7, 20, 30, 16, 13, 65]
    time_skipfuzz_go_bb_maxall_scatter = [106, 81, 3600, 89, 97, 3600, 3600, 82, 93, 76, 140, 93, 94, 3600, 3600, 3600, 168, 109, 109, 3600]

    
    estimate_time_pyfunc, magnitude_time_pyfunc = VD_A(time_skipfuzz_go_bb_ns_pyfunc, time_skipfuzz_pyfunc)
    print("A12-time pyfunc: ", 1 - estimate_time_pyfunc)

    estimate_time_scatter, magnitude_time_scatter = VD_A(time_skipfuzz_go_bb_max_inv_scatter, time_skipfuzz_scatter)
    print("A12-time scatter: ", 1 - estimate_time_scatter)

   

    print("pyfunc: ",ss.mannwhitneyu(x = time_skipfuzz_go_bb_ns_pyfunc, y = time_skipfuzz_pyfunc, alternative='less'))

    print("scatter: ",ss.mannwhitneyu(x = time_skipfuzz_go_bb_max_inv_scatter, y = time_skipfuzz_scatter, alternative='less'))
