# -*- coding: utf-8 -*-
"""Results-BC.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mnaaLexmqrQwEu1j6EdBSAqMeteDNt7k
"""

# Importing Libraries
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.decomposition import PCA

import warnings
warnings.filterwarnings("ignore")

#Loading the data set
bc = pd.read_csv('Breast-Cancer.csv')
bc.dropna()
bc.shape

bc.head()

#Describing the dataset
bc.describe()

bc.apply(lambda x: x.isnull().sum())

"""## Data Cleaning"""

#Removing null valued columns

bc.drop('Unnamed: 32',axis=1, inplace=True)
bc.head(10)

"""## Data Prepocessing"""

#Converting the text 'diagnosis' to binary column
bc['diagnosis'] = np.where(bc['diagnosis']=='M', 1, 0)
bc.head()

bc['diagnosis'].value_counts()

#The data is equally distributed to perform future operations without error
sns.countplot(bc['diagnosis'])

"""## Exploratory data analysis"""

# Data Visualization for the Dataset
# Histogram for each numeric
bc.hist(figsize=(19,9), color="green")
plt.show()

# Target Variable : Diagnosis
plt.figure(figsize = (8,6))
sns.distplot(bc['diagnosis'], color='green')

"""## Relation between diagnosis and other Categorical variables"""

# diagnosis and concave points_mean
bc['concave points_mean'].hist(bins = 100, color='green')
plt.show()

# diagnosis and area_worst

sns.barplot(x ='diagnosis', y='area_worst', data = bc, palette= 'Set3' )

plt.figure(figsize =(20,6))
sns.barplot(x='radius_mean',y='texture_mean',data =bc, hue= 'diagnosis',palette='viridis')
plt.xlabel('Mean Radius of the lump')
plt.ylabel('Texture of the lump')

plt.figure(figsize =(20,6))
sns.barplot(x='perimeter_worst',y='area_worst',data =bc, hue= 'diagnosis')

plt.figure(figsize =(8,6))
sns.scatterplot(x ='texture_mean', y = 'texture_worst', data = bc, hue ='diagnosis')

"""## Correlation Score"""

# Correlation matrix
corr  = bc.corr()
plt.figure(figsize = (13,13))
sns.heatmap(corr, cbar= True, square = True, fmt = '.1f', annot = True, annot_kws = {'size':10}, cmap = 'Greens')

"""## data set Test & Train splitting"""

X = bc.drop(["diagnosis"], axis=1)  # dropping target feature from rest of features
Y = bc["diagnosis"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20, random_state=42)

"""## Using KNN Model"""

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier() # By default K = 5
knn.fit(X_train,Y_train)

Y_pred = knn.predict(X_test)

knn.score(X_train,Y_train)

knn.score(X_test,Y_test)

"""## Model Evaluation"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

print(classification_report(Y_test,Y_pred))

cm = confusion_matrix(Y_test,Y_pred)
sns.heatmap(cm,square=True,annot=True)

"""## Change K Value"""

error_rate = []
for i in range(1,40) :
    knn = KNeighborsClassifier (n_neighbors = i)
    knn.fit(X_train,Y_train)
    pred_i= knn.predict(X_test)
    error_rate.append(np.mean(pred_i != Y_test))

plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,color='blue',
         linestyle='dashed',marker='o',markerfacecolor='red',markersize=10)
plt.title('error rate vs. k vale')
plt.xlabel('k')
plt.ylabel('Error Rate')
print("Minimum error:-",min(error_rate),"at K =",error_rate.index(min(error_rate)))

acc = []
# Will take some time
from sklearn import metrics
for i in range(1,40):
    neigh = KNeighborsClassifier(n_neighbors = i).fit(X_train,Y_train)
    yhat = neigh.predict(X_test)
    acc.append(metrics.accuracy_score(Y_test, yhat))

plt.figure(figsize=(10,6))
plt.plot(range(1,40),acc,color = 'blue',linestyle='dashed',
         marker='o',markerfacecolor='red', markersize=10)
plt.title('accuracy vs. K Value')
plt.xlabel('K')
plt.ylabel('Accuracy')
print("Maximum accuracy:-",max(acc),"at K =",acc.index(max(acc)))

knn= KNeighborsClassifier(n_neighbors = 10)

knn.fit(X_train,Y_train)

Y_pred = knn.predict(X_test)

knn.score(X_train,Y_train)

knn.score(X_test,Y_test)

y_pred_proba = knn.predict_proba(X_test)[:,1]

from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(Y_test, y_pred_proba)
roc_curve(Y_test, y_pred_proba)
auc = roc_auc_score(Y_test, y_pred_proba)
print('AUC: %.3f' % auc)

plt.plot([0,1],[0,1],'k--')
plt.plot(fpr,tpr, label='Knn')
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.title('KNN = 10 ROC curve')
plt.show()

from sklearn.metrics import roc_auc_score
roc_auc_score(Y_test,y_pred_proba)

from sklearn.model_selection import GridSearchCV

param_grid = {'n_neighbors':np.arange(1,50)}

knn = KNeighborsClassifier()
knn_cv= GridSearchCV(knn,param_grid,cv=5)
knn_cv.fit(X,Y)

knn_cv.best_score_

knn_cv.best_params_

"""## Building KNN using Euclidean Distance and 10 neighbors"""

knn = KNeighborsClassifier(n_neighbors = 10, metric='minkowski', weights='distance')
knn.fit(X_train, Y_train)

Y_pred = knn.predict(X_train)

print(classification_report(Y_pred, Y_train))

acc = []
# Will take some time
from sklearn import metrics
for i in range(1,40):
    neigh = KNeighborsClassifier(n_neighbors = i).fit(X_train,Y_train)
    yhat = neigh.predict(X_test)
    acc.append(metrics.accuracy_score(Y_test, yhat))

plt.figure(figsize=(10,6))
plt.plot(range(1,40),acc,color = 'blue',linestyle='dashed',
         marker='o',markerfacecolor='red', markersize=10)
plt.title('accuracy vs. K Value')
plt.xlabel('K')
plt.ylabel('Accuracy')
print("Maximum accuracy:-",max(acc),"at K =",acc.index(max(acc)))

"""## Outlier Detection and Finding best K Value"""

corr_mat = bc.select_dtypes("number").corr()
treshold = 0.75
filter = np.abs(corr_mat["diagnosis"])>treshold
corr_feat = corr_mat.columns[filter].to_list()
sns.clustermap(bc[corr_feat].corr(), annot =True, fmt = ".2f");

columns = X.columns.to_list()

for i in bc.select_dtypes("number").columns:

    plt.figure()
    plt.title(f'{i}')
    plt.boxplot(bc[i], vert = False);

def outliers(bc, ft):
    Q1 = bc[ft].quantile(0.25)
    Q3 = bc[ft].quantile(0.75)
    IQR = Q3-Q1

    low = Q1 - 1.5 * IQR
    top = Q3 + 1.5 * IQR

    ls = bc.index[ (bc[ft] < low ) |  (bc[ft]  > top) ]
    return ls

knn = KNeighborsClassifier(n_neighbors = 10, metric='minkowski', weights='distance')
knn.fit(X_train, Y_train)
Y_pred = knn.predict(X_train)

from sklearn.model_selection import GridSearchCV
def knn_best_params(X_train,X_test,y_train,y_test):
    k_range = list(range(1,31))
    weight_options = ["uniform","distance"]
    print()
    #to grid search we need to add those values in a dict
    param_grid = dict(n_neighbors = k_range,weights = weight_options)
    knn = KNeighborsClassifier()
    grid = GridSearchCV(knn,param_grid, cv = 10, scoring = "accuracy")
    grid.fit(X_train,Y_train)
    print("Best Training Score: {} with parameters {}".format(grid.best_score_, grid.best_params_))
    print()

    knn = KNeighborsClassifier(**grid.best_params_)
    knn.fit(X_train,Y_train)

    y_pred_test = knn.predict(X_test)
    y_pred_train = knn.predict(X_train) #are there any overfitting or underfitting

    cm_test = confusion_matrix(Y_test,y_pred_test)
    cm_train = confusion_matrix(Y_train,y_pred_train)

    acc_test = accuracy_score(Y_test,y_pred_test)
    acc_train = accuracy_score(Y_train,y_pred_train)
    print("Test Score:{}, Train Score:{}".format(acc_test,acc_train))
    print()
    print("CM Test:", cm_test)
    print("CM Train:", cm_train)

    return grid

grid = knn_best_params(X_train,X_test,Y_train,Y_test)

"""## Feature Engineering"""

bc['STAGE'] = 'NULL'

# create a list of our conditions
conditions = [
    (bc['diagnosis'] == 0) & (bc['radius_worst'] <= 15),
    (bc['diagnosis'] == 0) & (bc['radius_worst'] >= 15),
    (bc['diagnosis'] == 1) & (bc['radius_worst'] > 15) & (bc['radius_worst'] <= 20),
    (bc['diagnosis'] == 1) & (bc['radius_worst'] > 20) & (bc['area_worst'] <= 2000),
    (bc['diagnosis'] == 1) & (bc['area_worst'] > 2000)
    ]

# create a list of the values we want to assign for each condition
values = ['Stage-0', 'Stage-1', 'Stage-2', 'Stage-3', 'Stage-4']

# create a new column and use np.select to assign values to it using our lists as arguments
bc['STAGE'] = np.select(conditions, values)

bc

bc['STAGE'].value_counts()

bc['Death Causing'] = 'NULL'

conditions = [
    (bc['STAGE'] == 'Stage-1') & (bc['STAGE'] == 'Stage-0') & (bc['STAGE'] == 'Stage-2'),
    (bc['STAGE'] == 'Stage-3')
    ]

# create a list of the values we want to assign for each condition
values = ['NO', 'YES']

# create a new column and use np.select to assign values to it using our lists as arguments
bc['Death Causing'] = np.select(conditions, values)

bc['Death Causing'].value_counts()

bc['Death Causing'] = bc['Death Causing'].replace('YES',1)
bc['Death Causing'].value_counts()

sns.countplot(bc['Death Causing'])

"""## Kth- Nearest Neighbour Classifier after Feature Engineering"""

X = bc.drop(["STAGE"], axis=1)  # dropping target feature from rest of features
Y = bc["STAGE"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20, random_state = 42)

knn = KNeighborsClassifier(n_neighbors = 10, metric='minkowski', weights='distance')
knn.fit(X_train, Y_train)

Y_pred = knn.predict(X_test)

knn.score(X_train,Y_train)

knn.score(X_test,Y_test)

print(classification_report(Y_test,Y_pred))

cm = confusion_matrix(Y_test,Y_pred)
sns.heatmap(cm,square=True,annot=True)

plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,color='blue',
         linestyle='dashed',marker='o',markerfacecolor='red',markersize=10)
plt.title('error rate vs. k vale')
plt.xlabel('k')
plt.ylabel('Error Rate')
print("Minimum error:-",min(error_rate),"at K =",error_rate.index(min(error_rate)))

acc = []
# Will take some time
from sklearn import metrics
for i in range(1,40):
    neigh = KNeighborsClassifier(n_neighbors = i).fit(X_train,Y_train)
    yhat = neigh.predict(X_test)
    acc.append(metrics.accuracy_score(Y_test, yhat))

plt.figure(figsize=(10,6))
plt.plot(range(1,40),acc,color = 'blue',linestyle = 'dashed',
         marker = 'o',markerfacecolor = 'red', markersize = 10)
plt.title('accuracy vs. K Value')
plt.xlabel('K')
plt.ylabel('Accuracy')
print("Maximum accuracy:-",max(acc),"at K =",acc.index(max(acc)))

grid = knn_best_params(X_train,X_test,Y_train,Y_test)
