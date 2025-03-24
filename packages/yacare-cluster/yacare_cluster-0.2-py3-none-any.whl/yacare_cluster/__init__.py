# yacare.py

"""
YACARE
==========

This module implements the YACARE algorithm described in the article "Clustering data by reordering them" by Axel Descamps et al.
Eventhough it can be used in command line, it is advised to use it with the provided Jupyter notebook.
This module has been written by Nicolas Chéron and Axel Descamps.
"""

import numpy as np                                                     
import matplotlib.pyplot as plt                                        
import sklearn                                                         
from sklearn import cluster                                            
from sklearn.preprocessing import StandardScaler                       
from sklearn.metrics import confusion_matrix                           
from sklearn.metrics.cluster import adjusted_rand_score                
from sklearn.metrics.cluster import adjusted_mutual_info_score         
from sklearn.metrics.cluster import homogeneity_completeness_v_measure 
from sklearn.metrics.cluster import fowlkes_mallows_score              
from sklearn.metrics.cluster import normalized_mutual_info_score       
from sklearn.metrics.cluster import davies_bouldin_score               
from sklearn.metrics import silhouette_score                           
from datetime import datetime
import itertools
import copy
import sys

print(f"We are using Python {sys.version[0:6]}, numpy {np.version.version}, sci-kit learn {sklearn.__version__}, yacare 0.99a from 2025-03-14.")
print("For help on a given function, type for example help(yacare.perform_first_reordering).")

