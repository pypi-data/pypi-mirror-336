#=========================================================================
#libraries:

import matplotlib.pyplot as plt 
import pandas as pd

from snl_regression_quality.load_data import load_example
#=========================================================================



class ReadingData:
    def __init__(self,path_data_x,path_data_y,example=True):

        #initialization:
        self.example = example

        if self.example:
            self.path_full_x = load_example(path_data_x)
            self.path_full_y = load_example(path_data_y)
            self.dataset_x = pd.read_csv(self.path_full_x)
            self.dataset_y =  pd.read_csv( self.path_full_y)

        else:
            self.dataset_x = pd.read_csv(path_data_x)
            self.dataset_y =  pd.read_csv(path_data_y)

    def run(self):

        if self.example:
            rows_limits=(0,25)
            columns_limits=(0,3)
            x_values = self.dataset_x.iloc[rows_limits[0]:rows_limits[1],columns_limits[0]:columns_limits[1]].values
            y_values = self.dataset_y.iloc[rows_limits[0]:rows_limits[1],columns_limits[0]:columns_limits[1]].values
        else:
            x_values = self.dataset_x.values
            y_values = self.dataset_y.values

         
        self.x_mean =x_values.mean(axis=1)
        self.y_mean =y_values.mean(axis=1)
        
        return  x_values,y_values , self.x_mean, self.y_mean

    def visualization(self):
        
        plt.plot(self.x_mean, self.y_mean, 'b-', label='Data mean')
        plt.legend()
        plt.show()

       
