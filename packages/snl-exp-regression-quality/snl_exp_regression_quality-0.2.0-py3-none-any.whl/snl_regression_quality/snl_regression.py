#================================================================================================
#libraries:
import matplotlib.pyplot as plt 


from snl_regression_quality.modules.methods.scaling_data import ScalingData
from snl_regression_quality.modules.methods.remove_outlier import OutlierData
from snl_regression_quality.modules.metrics.calculate_assumptions import Assumptions
from snl_regression_quality.modules.metrics.calculate_quality import Quality
from snl_regression_quality.modules.methods.user_messages_initial import initial_message
from snl_regression_quality.modules.utils.global_constants import GREEN, RED, YELLOW,  RESET   
from snl_regression_quality.modules.utils.ram_consumption import memory_usage_psutil
import time 
#=================================================================================================



class SnlRegression:
    def __init__(self,x_data,y_data,x_data_mean, y_data_mean, waveform,significance_level):
        self.x_data = x_data
        self.y_data = y_data
        self.x_data_mean = x_data_mean
        self.y_data_mean = y_data_mean 
        self.waveform = waveform
        self.significance_level = significance_level
        
    #---------------------------------------------------------------------------------------------------------
    def process_full(self,text=True):
        
        #1) Initialization: 
        x_mean = self.x_data_mean
        y_mean = self.y_data_mean
        y_values = self.y_data

        
        #--------------------------------------------------------------------------------------------------
        # 2): standardization
        #--------------------------------------------------------------------------------------------------

        x_scaling, y_scaling = ScalingData(x_mean, y_mean ).run()

        if text:
            #--------------------------------------------------------------------------------------------------
            # 3): remove_outlier
            #--------------------------------------------------------------------------------------------------                     

            x_deescalated, y_deescalated, indexes = OutlierData(self.waveform ,x_scaling, y_scaling,x_mean, y_mean).run()

            #--------------------------------------------------------------------------------------------------
            # 3): calculate Assumptions:
            #--------------------------------------------------------------------------------------------------
            
            self.enable_assumptions = Assumptions(y_mean,indexes,y_deescalated,self.significance_level).run()
            
            #--------------------------------------------------------------------------------------------------
            # 3): calculate Quality:
            #--------------------------------------------------------------------------------------------------
            if self.enable_assumptions:
                Quality(y_values,x_mean,y_mean,indexes,x_deescalated,y_deescalated,self.significance_level,self.waveform ).run()
            else: 
                print(RED+ f'Does not satisfies Assumption calculation!' +RESET)
        
        else:               

            x_deescalated, y_deescalated, indexes = OutlierData(self.waveform ,x_scaling, y_scaling,x_mean, y_mean).run(text=False)
            self.enable_assumptions = Assumptions(y_mean,indexes,y_deescalated,self.significance_level).run(text=False)
            if self.enable_assumptions:
                Quality(y_values,x_mean,y_mean,indexes,x_deescalated,y_deescalated,self.significance_level,self.waveform ).run(text=False)

    #---------------------------------------------------------------------------------------------------------
    def run(self):
        initial_message()
        start_time_process = time.time()  
        self.process_full()
        end_time_process = time.time()
        ram_outlier = memory_usage_psutil()
        
        elapsed_time_outlier = end_time_process - start_time_process

        print(YELLOW+ f"Elapsed time (outlier): {round(elapsed_time_outlier,2)} seconds."+ RESET)
        print(YELLOW+ f"Memory usage (outlier): {round(ram_outlier,2)} MB."+ RESET)
        print('++++'*20)
    #---------------------------------------------------------------------------------------------------------
    def run_without_message(self):
        
        self.process_full(text=False)

        return self.enable_assumptions
        




