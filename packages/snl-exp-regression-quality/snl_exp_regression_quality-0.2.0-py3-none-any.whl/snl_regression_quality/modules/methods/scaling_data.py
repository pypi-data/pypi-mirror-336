#=========================================================================
#libraries:

import matplotlib.pyplot as plt 

#=========================================================================


class ScalingData:
    def __init__(self,data_x_mean, data_y_mean):

        self.data_XM = data_x_mean
        self.data_YM = data_y_mean
        

    def run(self):        
        self.x_scaling = (self.data_XM-self.data_XM.min())/(self.data_XM.max()-self.data_XM.min())
        self.y_scaling = (self.data_YM-self.data_YM.min())/(self.data_YM.max()-self.data_YM.min())

        return self.x_scaling, self.y_scaling


    def visualization(self):    

        # Dispersion of x and y
        plt.scatter(self.x_scaling,self.y_scaling)
        plt.xlabel('x - Scaling', fontsize=18)
        plt.ylabel('y- Scaling', fontsize=18)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.show()