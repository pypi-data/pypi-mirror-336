#================================================================================================
#Libraries: 
import matplotlib.pyplot as plt 
import numpy as np 
from numpy.linalg import inv
from scipy.optimize import curve_fit
from snl_regression_quality.modules.methods.waveform_regression import *
from snl_regression_quality.modules.utils.global_constants import GREEN, RED,BLUE,  RESET   
#=================================================================================================




class OutlierData:
    def __init__(self,waveform,x_scaling,y_scaling,x_mean,y_mean):
        
        self.name_waveform = waveform.lower()
        self.x_scaling = x_scaling
        self.y_scaling = y_scaling
        self.x_mean = x_mean
        self.y_mean = y_mean

    def curve_fitting(self, visualization=False):

        
        if self.name_waveform == "concave_increasing":
            self.function_fit = function_concave_increasing
        elif self.name_waveform == "convex_increasing":
            self.function_fit = function_convex_increasing
        elif self.name_waveform == "concave_decreasing":
            self.function_fit = function_concave_decreasing
        elif self.name_waveform == "convex_decreasing" : 
            self.function_fit = function_convex_decreasing
        else: 
            raise ValueError(f"Function '{self.name_waveform}' is not recognized. Uses 'concave_increasing', 'convex_increasing', 'concave_decreasing' or 'convex_decreasing'.")


        # Curve fitting
        self.popt_values, self.pcov_values = curve_fit(self.function_fit, self.x_scaling, self.y_scaling)
        
        if visualization:

            plt.plot(self.x_scaling, self.y_scaling, 'o', color ='red', label ="data")
            plt.plot(self.x_scaling, self.function_fit(self.x_scaling, *self.popt_values), '--', color ='blue', label ="optimized data")
            plt.legend()
            plt.show()


    def jacobian_matrix(self,visualization=False):
        
        #initialization:
        popt =   self.popt_values
        xS =  self.x_scaling 
        yS =   self.y_scaling

        # Jacobian Matrix
        J1=-xS*np.exp(popt[0]*xS - popt[1])
        J2=np.exp(popt[0]*xS - popt[1])
        J3=np.ones(len(J1))
        J=np.array([J1, J2, J3]).transpose()

        # Hat Matrix
        JTr=J.transpose()
        JM=np.dot(JTr,J)
        JiM=inv(JM)
        JMxi=np.dot(J, JiM)
        H=np.dot(JMxi,JTr)#Hat Matrix
        # Leverage
        L=np.diag(H)
        p=3 #Número de parámetros a optimizar

        # Cook distance según leverage (ocuparé éste D)
        Er=yS-self.function_fit(xS, *popt)
        MS=(1/(len(xS)-p))*sum(Er**2)
        self.D=(Er**2/(p*MS))*(L/((1-L)**2))
        self.threshold=3*(self.D.mean())


        if visualization:
            plt.plot(np.arange(1, len(xS)+1), self.D, 'o', color ='red', label ="Distance Cook")
            plt.plot(np.arange(1, len(xS)+1),np.ones(len(xS))*self.threshold, label ="Threshold")
            plt.legend()
            plt.show()



    def eliminate_outliers(self,visualization=False):
        #initialization:
        # popt =   self.popt_values
        xS =  self.x_scaling 
        yS =   self.y_scaling
        D = self.D
        threshold = self.threshold



        # Elimicación de Outliers
        self.indices = np.where( (np.array(D) < threshold) )[0].tolist()
        self.indices_eliminated = np.where( (np.array(D) > threshold) )[0].tolist()
        self.xSOutlier=xS[self.indices]
        self.ySOutlier=yS[self.indices]



        # Curve fitting a OCUPAR (Ya no hay outlier)
        self.popt_eliminate_outliers, pcov = curve_fit(self.function_fit, self.xSOutlier, self.ySOutlier)
       

        if visualization:
            # Checar qué datos quedaron
            # Distacia cook < 3*(D.mean()). Esos no son Outliers
            plt.plot(np.arange(1, len(self.xSOutlier)+1), D[self.indices], 'o', color ='red', label ="Distance Cook")
            plt.plot(np.arange(1, len(self.xSOutlier)+1),np.ones(len(self.xSOutlier))*threshold, label ="Threshold")
            plt.legend()
            plt.show()

            plt.plot(self.xSOutlier, self.ySOutlier, 'o', color ='red', label ="data")
            plt.plot(self.xSOutlier, self.function_fit(self.xSOutlier, *self.popt_eliminate_outliers), '--', color ='blue', label ="optimized data")
            plt.legend()
            plt.show()

    def de_escalated_data(self, visualization=False):

        #initialization:
        YM = self.y_mean
        XM = self.x_mean
        xSOutlier = self.xSOutlier
        popt = self.popt_eliminate_outliers
        indices = self.indices



        yD=self.function_fit(xSOutlier, *popt)*(YM.max()-YM.min())+YM.min()
        xD=XM[indices]

        if visualization: 
            # plt.plot(XM, YM, 'o', color ='red', label ="data")
            plt.plot(xD, yD, 'o', color ='blue', label ="optimized data")
            plt.plot(xD, YM[indices], 'o', color ='yellow', label ="data Without Outliers")
            plt.legend()
            plt.show()
        
        return xD, yD, indices

    def run(self,text=True):

        #1) curve_fitting:
        self.curve_fitting()
        #2) jacobian_matrix:
        self.jacobian_matrix()
        #3) eliminate_outliers:
        self.eliminate_outliers()
        #4) de_escalated_data:
        x_deescalated, y_deescalated, indexes = self.de_escalated_data()


        if text:
            if  self.indices_eliminated  == []:
                print(GREEN+'Does not contain outlier'+RESET)
                
            else:
                print('Contains outlier: ')
                print(f'The following indices'+RED+ f'{ self.indices_eliminated }'+RESET +' of the data x and y are deleted.')
           


        return x_deescalated, y_deescalated, indexes
    




