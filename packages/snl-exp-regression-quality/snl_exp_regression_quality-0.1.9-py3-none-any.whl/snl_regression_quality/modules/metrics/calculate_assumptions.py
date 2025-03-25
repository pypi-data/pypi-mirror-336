
#================================================================================================
#libraries:
import numpy as np 

from snl_regression_quality.modules.utils.global_constants import GREEN, RED,  RESET   

#=================================================================================================

class Assumptions:
    def __init__(self,y_mean,indexes,y_deescalated,significance_level):
        self.y_mean = y_mean
        self.indixes = indexes
        self.y_deescalated = y_deescalated
        self.alpha = significance_level

    def normality(self, text):

        #initialization: 
        from scipy import stats
        YM = self.y_mean
        indices = self.indixes
        yD = self.y_deescalated
       

        #Residuales 
        self.Res=YM[indices]-yD
        #perform Shapiro-Wilk Test
        
        stats.shapiro(self.Res)
        #p-value>0.05 Sí hay normalidad
        #Sólo para ver el histograma

        value_normality = stats.shapiro(self.Res).pvalue

        if text:
            #1) validation:
            if value_normality > self.alpha:
                print('1.1)'+GREEN+ f'Satisfies normality ({round(value_normality,4)} > p-value)'+RESET)
                enable_normality = True
            else:
                print('1.1)'+RED+ f'Does not satisfies normality ({round(value_normality,4)} > p-value)'+RESET)
                enable_normality = False
        else:
            #1) validation:
            if value_normality > self.alpha:
                
                enable_normality = True
            else:
                
                enable_normality = False

        
        return enable_normality
    
    def homocedasticity(self,text):

        #initialization: 
        import scipy.stats as stats
        Res = self.Res


        #  Los residuales se dividen en dos grupos
        G1=Res[:int(round(len(Res)/2,0))]
        G2=Res[int(round(len(Res)/2,0)):]
        
        #Bartlett's test centered at the mean (Este supone normalidad)
        _ , p  = stats.bartlett(G1, G2)


        value_homocedasticity = p
        if text:
            #1) validation:
            if value_homocedasticity > self.alpha:
                print('1.2)'+GREEN+f'Satisfies homoscedasticity ({round(value_homocedasticity,4)} > p-value )'+RESET)
                enable_homocedasticity = True
            else:
                print('1.2)'+RED+ f'Does not satisfies homoscedasticity ({round(value_homocedasticity,4)} > p-value)' +RESET)
                enable_homocedasticity = False
        else:
            #1) validation:
            if value_homocedasticity > self.alpha:                
                enable_homocedasticity = True
            else:
                
                enable_homocedasticity = False


        return enable_homocedasticity


    def independence(self,text):

        #initialization: 
        Res = self.Res

        # Tiene que haber normalidad y homocedasticidad   
        er_R=Res[1:]*Res[:-1]

        r1=sum(er_R)/sum(Res**2)#Toma esta fórmula
        # Límite
        r1L=(-1+1.96*np.sqrt(len(Res)-2))/(len(Res)-1)
        # Si |r1|<r1L, Sí hay independencia 

        if text:
            #1) validation:
            if np.abs(r1) < r1L:
                print('1.3)'+GREEN+f'Satisfies independence  ({round(np.abs(r1),4)} < {round(r1L,4)}) (|r1|<r1L)'+RESET)
                enable_independence  = True
            else:
                print('1.3)'+RED+ f'Does not satisfies independence  ({round(np.abs(r1),4)} > {round(r1L,4)}) (|r1|>r1L)' +RESET)
                enable_independence  = False

        else:

            #1) validation:
            if np.abs(r1) < r1L:                
                enable_independence  = True
            else:                
                enable_independence  = False


        return  enable_independence
    
    def run(self,text=True):


        if text:
            print('----'*20)

            # 1) normality
            # 2) homoscedasticity
            # 3) independence 
        
            enable_norm = self.normality(text)

            if enable_norm:
                enable_homo = self.homocedasticity(text)
                if enable_homo:
                    enable_inde = self.independence(text)
                    print('----'*20)
                    return enable_inde
                
                else: 
                    return False
            else: 
                return False
        else:
        
            enable_norm = self.normality(text)

            if enable_norm:
                enable_homo = self.homocedasticity(text)
                if enable_homo:
                    enable_inde = self.independence(text)
                   
                    return enable_inde
                
                else: 
                    return False
            else: 
                return False

        
        
             
    





