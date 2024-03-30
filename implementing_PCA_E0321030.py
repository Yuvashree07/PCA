# -*- coding: utf-8 -*-
"""Untitled13.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SCzJtkQTLUayMfxJYEuJQXkUQ9Kuedlq
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.feature_selection import mutual_info_regression

# matplotlib defaults

plt.style.use("seaborn-darkgrid")
plt.rc("figure", autolayout=True)
plt.rc(
    "axes",
    labelweight="bold",
    labelsize="large",
    titleweight="bold",
    titlesize=14,
    titlepad=10,
)

car = pd.read_csv('cars-used.csv')
car

car.var()

y = car['price']
car_s=car.drop('price',axis=1)

cols=[col for col in car .columns if car[col].dtype in ['int64','float64']]

for idx, col in enumerate(cols):
  plt.figure(idx,figsize=(6,6))
  sns.scatterplot(x=col,y=y,data=car)
  plt.show

#PCA

features = ['mileage','year','mpg','tax','engineSize']
X = car_s[features]
X_norm = (X -X.mean(axis=0))/X.std(axis=0) #normalizing the features
pca = PCA()  #principal component analysis on features
X_pca = pca.fit_transform(X_norm) #fit and transformX_norm to PCA dataframe
names=[f"PC{i+1}" for i in range(X_pca.shape[1])] # converting to dataframe
X_pcadf = pd.DataFrame(X_pca, columns=names)

print(X_pcadf.head())
print("shape of pca df :" , X_pcadf.shape)

pca.singular_values_

# convert cov_matrix from the X_norm
cov_matrix = np.cov(X_norm.T)
print("Convariance matrix: ", cov_matrix)

# from COV_MATRIX calculate eigenvectors and eigenvalues
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
print("Eigenvectors:", eigenvectors)
print("Eigenvalues:", eigenvalues)

# sort the eigen values and eigen vectors in descending order
eig_pairs = [(eigenvalues[index],eigenvectors[:,index]) for index in range(len(eigenvalues))]

# sort the pairs
eig_pairs.sort()

# reverse to make it in correct order
eig_pairs.reverse()
print(eig_pairs)

# extract the sorted eiganvalues and eiganvectors
eigenvalues_sorted = [eig_pairs[index][0] for index in range(len(eigenvalues))]
eigenvectors_sorted = [eig_pairs[index][1] for index in range(len(eigenvalues))]

# print sorted eigan values
print("Sorted eigan values:", eigenvalues_sorted)

# plot the variance plots using sorted eigenvalues and eigenvectors
total = sum(eigenvalues_sorted)
var_explained = [(i/total) for i in eigenvalues_sorted]

# calculate cumulative variance
cum_var_exp = np.cumsum(var_explained)

# transforming original dataframe into PCA
vect = np.array(eigenvectors_sorted)

# dot product to create principal components analysis
X_vect_pca = np.dot(X_norm,vect.T)

pd.DataFrame(X_vect_pca)

#PLOTTING EXPLAINED VVARIANCE RATIO

evr = pca.explained_variance_ratio_
print(evr)
features = ['mileage','year','mpg','tax','engineSize']

# plot the EVR using matplotlib pyplot
plt.figure(figsize=(6,6))
sns.barplot(x=np.array(features), y=evr)
plt.xlabel("Components features")
plt.ylabel("%Explained variance ratio")
plt.show

ev = pca.explained_variance_
print(ev)

features = ['mileage','year','mpg','tax','engineSize']


plt.figure(figsize=(6,6))
sns.lineplot(x=np.array(features), y=ev)
plt.xlabel("Components features")
plt.ylabel("%Explained variance")
plt.ylim(0,2)
plt.show

evc = np.cumsum(pca.explained_variance_)
print(evc)

features = ['mileage','year','mpg','tax','engineSize']


plt.figure(figsize=(6,6))
sns.lineplot(x=np.array(features), y=evc)
plt.xlabel("Components features")
plt.ylabel("Cummulative explained variance")
plt.ylim(0,5)
plt.show

loadings = pd.DataFrame(pca.components_.T ,
                        index=np.array(features),
                        columns=names)

loadings

pca.noise_variance_

# covariance matrix of principal components
pca.get_covariance()

y = car['price']

mi_score = mutual_info_regression(X_pcadf,y, discrete_features=False)
mi_score = pd.Series(mi_score, index=X_pcadf.columns, name="MI_SCORE")

print(mi_score)
