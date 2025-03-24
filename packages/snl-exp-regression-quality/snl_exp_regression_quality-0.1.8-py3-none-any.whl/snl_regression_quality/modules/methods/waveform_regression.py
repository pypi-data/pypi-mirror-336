#==========================================================================================
# libraries: 

import numpy as np 

#=============================================================================================


def function_concave_increasing(data_x, constant_m, constant_c, constant_b):
    return -1*np.exp((-constant_m * data_x) + constant_c) + constant_b

def function_convex_increasing(data_x, constant_m, constant_c, constant_b):
    return np.exp((constant_m * data_x) - constant_c) + constant_b

def function_concave_decreasing(data_x, constant_m, constant_c, constant_b):
    return -1*np.exp((constant_m * data_x) - constant_c) + constant_b

def function_convex_decreasing(data_x, constant_m, constant_c, constant_b):
    return np.exp((-constant_m * data_x) + constant_c) + constant_b