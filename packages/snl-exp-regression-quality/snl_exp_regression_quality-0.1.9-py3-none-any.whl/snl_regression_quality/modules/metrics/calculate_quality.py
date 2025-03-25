#================================================================================================
#libraries:
import numpy as np 

from snl_regression_quality.modules.utils.global_constants import GREEN, RED, BLUE,  RESET   

from scipy.stats import f_oneway
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
import math
from scipy.optimize import curve_fit
from snl_regression_quality.modules.methods.waveform_regression import *
#=================================================================================================

class Quality:
    def __init__(self,y_original,x_mean,y_mean,indexes,x_deescalated,y_deescalated,significance_level,waveform):
        self.y_original = y_original
        self.y_mean = y_mean
        self.x_mean = x_mean
        self.indexes = indexes
        self.x_deescalated = x_deescalated
        self.y_deescalated = y_deescalated
        self.alpha = significance_level
        self.name_waveform = waveform

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


    def dynamic_range(self,text):
        #initialization:
        indices = self.indexes
        YM = self.y_mean 
   
        R2=max(YM[indices])
        R1=min(YM[indices])
        Rang=abs(R2-R1)
        if text:
            print(f'2.1) Dynamic range:' +GREEN+ f'{round(Rang,6)}'+RESET)

    def max_sensitivity(self,text):

        #initialization: 
        xD = self.x_deescalated 
        yD = self.y_deescalated

        #main: 
        OptData=np.concatenate((xD.reshape(-1,1), yD.reshape(-1,1)), axis=1)
        IndexOr=[B[0] for B in sorted(enumerate(OptData[:,0]),key=lambda i:i[1])]
        OptDataOrden=OptData[IndexOr]
        sensib=max(abs(np.diff(OptDataOrden[:,1])/np.diff(OptDataOrden[:,0])))
        if text:
            print(f'2.2) Max. Sensitivity :' +GREEN+ f'{round(sensib,6)}'+RESET)


    def resolution(self,text):
        
        #initialization:
        indices = self.indexes
        YM = self.y_mean
        Y = self.y_original  
        alpha=self.alpha
   

        ySour=Y[indices]

        ## Resolution
        sy=np.sort(YM[indices], axis=None) # y Orden de menor a mayor
        dsy=np.diff(sy)# Diferncia consecutiva
        odsy=np.sort(dsy, axis=None) # dsy Orden de menor a mayor

        i=0        
        for x in odsy:
            indexmin=np.where(dsy == odsy[i])[0]
            a=ySour[np.where(YM[indices] == sy[indexmin])[0],:].T.tolist()
            b=ySour[np.where(YM[indices] == sy[indexmin+1])[0],:].T.tolist()
            i=i+1
            if f_oneway(a, b).pvalue<alpha:
                Reso=odsy[i-1]
                if text:
                    print(f'2.3) Resolution value:' +GREEN+ f'{round(Reso,6)}'+RESET)
                break

    
    def accuracy(self,text):
        
        #initialization: 
        XM = self.x_mean 
        YM = self.y_mean
        indices = self.indexes
        funcG4 = self.function_fit

        #main: 
        kf=KFold(n_splits=10, shuffle = True, random_state = 2)
 
        Results_RMSESt = np.zeros(kf.get_n_splits()) 

        i=-1
        XA=XM[indices]
        yA=YM[indices]
        for  train_indices, test_indices in kf.split(XA):
            i=i+1
            
            #print("training indexes: ", train_indices, "test indexes: ", test_indices)
            X_train, X_test = XA[train_indices], XA[test_indices]
            y_train, y_test = yA[train_indices], yA[test_indices]
            XStTrain=(X_train-X_train.min())/(X_train.max()-X_train.min())
            yStTrain=(y_train-y_train.min())/(y_train.max()-y_train.min())        
            XStTest=(X_test-X_train.min())/(X_train.max()-X_train.min())
            yStTest=(y_test-y_train.min())/(y_train.max()-y_train.min())
            #### Curve fitting
            popt, pcov = curve_fit(funcG4, XStTrain, yStTrain)
            y_predTest=funcG4(XStTest, *popt)*(y_train.max()-y_train.min())+y_train.min()
            #print("RMSECV: ", math.sqrt(mean_squared_error(y_predTest, y_test)))
            Results_RMSESt[i]=math.sqrt(mean_squared_error(y_predTest, y_test))
                    
        RMSECV = Results_RMSESt.mean()

        if text:
            print(f'2.4) Accuracy value:'+GREEN+ f'{round(RMSECV ,6)}'+RESET)
   



    def run(self, text=True):

        if text:
            print(BLUE+'===='*20+RESET)
            print(BLUE+'part 2, Regression quality: '+RESET)
            print(BLUE+'===='*20+RESET)

            print('----'*20)

            # 1) dynamic_range
            self.dynamic_range(text)
            # 2) max_sensitivity
            self.max_sensitivity(text)
            # 3) resolution
            self.resolution(text)
            # 4) accuracy
            self.accuracy(text)
            print('----'*20)
        else: 
          

            # 1) dynamic_range
            self.dynamic_range(text)
            # 2) max_sensitivity
            self.max_sensitivity(text)
            # 3) resolution
            self.resolution(text)
            # 4) accuracy
            self.accuracy(text)
           

        

        
        
       
        
    


