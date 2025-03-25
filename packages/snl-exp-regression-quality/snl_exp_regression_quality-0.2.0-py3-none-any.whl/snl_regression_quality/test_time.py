#================================================================================================
from snl_regression_quality.snl_regression import SnlRegression
from snl_regression_quality.modules.methods.waveform_regression import function_concave_decreasing
from snl_regression_quality.modules.utils.ram_consumption import memory_usage_psutil
import time 
from tqdm import tqdm
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from snl_regression_quality.modules.methods.reading_data import ReadingData
from snl_regression_quality.load_data import load_example
#=================================================================================================



def run_test():
    #--------------------------------------------------------------------------------------------------
    # 1): Initialization of input parameters:
    #--------------------------------------------------------------------------------------------------

    path_x_dataset = 'test_X.csv'
    path_y_dataset = 'test_Y.csv'
    significance_level = 0.05

    model_form= "concave_decreasing"


    path_full_x = load_example(path_x_dataset)
    path_full_y = load_example(path_y_dataset)
    #--------------------------------------------------------------------------------------------------
    # 2): Load and read data:
    #--------------------------------------------------------------------------------------------------

    x_values,y_values ,x_mean, y_mean = ReadingData(path_full_x,path_full_y,example=False).run()

    #--------------------------------------------------------------------------------------------------
    # 3): execute code:
    #--------------------------------------------------------------------------------------------------

    size_data = np.arange(60,12000,10)


    list_time = []
    list_ram = []
    list_size = []

    for i in tqdm(size_data, desc="Procesando"):

        x_values = x_values[:i,:]
        y_values = y_values[:i,:]
        x_mean = x_mean[:i]
        y_mean = y_mean[:i]
        
        start_time = time.time()
        enable_ok = SnlRegression(x_values,y_values,x_mean,y_mean ,model_form,significance_level).run_without_message()
        end_time = time.time()

        elapsed_time = end_time - start_time
        ram = memory_usage_psutil()

        #save:
        if enable_ok:
            list_time.append(elapsed_time)
            list_ram.append(ram)
            list_size.append(i)



    df_time = pd.DataFrame(np.column_stack([list_size,list_time]), columns=["# sample", "Time(s)"])

    df_time.to_csv("test_time.csv", index=False)

    df_time = pd.DataFrame(np.column_stack([list_size,list_ram]), columns=["# sample", "RAM(MB)"])

    df_time.to_csv("test_ram.csv", index=False)

if __name__ == "__main__":
    run_test()



