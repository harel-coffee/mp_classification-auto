# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:09:51 2021

@author: scien
"""
#Sklearn modules
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier
from sklearn.base import BaseEstimator, TransformerMixin

#Imblearn modules
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline 


#Filter preprocessing
from scipy.signal import savgol_filter

#Fix seed to reproducibility
seed = 0

class Savgol_transformer(BaseEstimator, TransformerMixin):

    def __init__(self, window = 11, degree = 10):
        assert window > degree, "window must be less than poly. degree"
        self.window = window
        self.degree = degree
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform(self, X, y = None ):
        return savgol_filter(X, self.window, self.degree)
    
def build_pipe(scaler = '', 
               sav_filter = True,
               pca = True, 
               over_sample = True):
    
    prefix = ''
    
    pre_pipe =[('estimator', DummyClassifier())]
    
    if sav_filter:
        prefix += 'svfilter_'
        pre_pipe.insert(-1, ('filter', 
                             Savgol_transformer(window = 11, degree=10)))        
    
    scaler_dictionary = {
        'std' : StandardScaler(), 
        'minmax' : MinMaxScaler()
        }
    
    if(scaler in scaler_dictionary):
        
        prefix += scaler + '_'    
        pre_pipe.insert(-1, ('scaler', scaler_dictionary[scaler]))         
                
    if(pca):        
        prefix += 'pca_'        
        pre_pipe.insert(-1,
                        ('dim_red', 
                         PCA(n_components = 0.99, random_state = seed)
                         ))
    if(over_sample):
        
       prefix += 'over_'
        
       pre_pipe.insert(-1, ('over_sample',
                            RandomOverSampler(random_state = seed)) 
                             )

    return  Pipeline(pre_pipe), prefix

    