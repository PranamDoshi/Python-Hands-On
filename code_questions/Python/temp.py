#Write your code here
import pandas as pd
import numpy as np


heights_A = pd.Series([176.2, 158.4, 167.6, 156.2, 161.4], ['s1', 's2', 's3', 's4', 's5'])
print(heights_A.shape)


weights_A = pd.Series([85.1, 90.2, 76.8, 80.4, 78.9], ['s1', 's2', 's3', 's4', 's5'])
print(weights_A.dtype)


df_A = pd.DataFrame([heights_A, weights_A], columns = ['Student_height', 'Student_weight'])
print(df_A.shape)



np.random.seed(100)
heightArr_B = 25.0*np.random.randn(5) + 170.0
heights_B = pd.Series(heightArr_B, ['s1', 's2', 's3', 's4', 's5'])
np.random.seed(100)
weightArr_B =  12.0*np.random.randn(5) + 75.0
weights_B = pd.Series(weightArr_B, ['s1', 's2', 's3', 's4', 's5'])
print(round(heights_B.mean(axis = 0), 2))
#print(heights_B.mean(axis = 0))


df_B = pd.DataFrame({'Student_height' : heights_B, 'Student_weight' : weights_B})
print(list(df_B.columns))