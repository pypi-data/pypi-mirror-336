#================================================================================================
from snl_regression_quality.snl_regression import SnlRegression
from snl_regression_quality.modules.methods.waveform_regression import function_concave_decreasing
from snl_regression_quality.modules.utils.ram_consumption import memory_usage_psutil
import time 


import numpy as np 
import matplotlib.pyplot as plt
from snl_regression_quality.modules.methods.reading_data import ReadingData
#=================================================================================================

#--------------------------------------------------------------------------------------------------
# 1): function:
#--------------------------------------------------------------------------------------------------

def synthetic_data(x, y,size_data):
    from scipy.interpolate import interp1d 

    x_interp = np.linspace(x.min(), x.max(), size_data)   
    f_interp = interp1d(x, y, kind='cubic')  
    y_interp = f_interp(x_interp)
    return x_interp, y_interp 


#--------------------------------------------------------------------------------------------------
# 2): Initialization of input parameters:
#--------------------------------------------------------------------------------------------------
significance_level = 0.05
model_form= "concave_decreasing"

path_x_dataset = 'data_X.csv'
path_y_dataset = 'data_Y.csv'
x_values,y_values ,x_mean, y_mean = ReadingData(path_x_dataset,path_y_dataset,example=True).run()
y_mean = np.delete(y_mean, np.argmin(x_mean))
x_mean = np.delete(x_mean, np.argmin(x_mean))

x_new, y_new = synthetic_data(x_mean, y_mean ,1000)

plt.plot(x_mean, y_mean, 'o')
plt.plot(x_new, y_new, '-', label='Interpolación (1000 puntos)')
plt.legend()
plt.grid(True)
plt.show()


#--------------------------------------------------------------------------------------------------
# 3): execute code:
#--------------------------------------------------------------------------------------------------

size_data = np.arange(20,400,20)


list_time = []
list_ram = []
for i in size_data:
    x_m, y_m= synthetic_data(x_mean, y_mean ,i)

    x_values =np.column_stack([x_m,x_m,x_m])
    y_values = np.column_stack([y_m,y_m,y_m])

    start_time = time.time()
    SnlRegression(x_values,y_values,x_m,y_m,model_form,significance_level).run_without_message()
    end_time = time.time()

    elapsed_time = end_time - start_time
    ram = memory_usage_psutil()

    #save:
    list_time.append(elapsed_time)
    list_ram.append(ram)


plt.plot(list_time)
plt.show()

plt.plot(list_ram)
plt.show()

