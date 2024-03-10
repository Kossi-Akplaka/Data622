# -*- coding: utf-8 -*-
"""Data622_Assignement 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZJj4WLandjKpuIjvqhNSj5LE-cwWQqJC

## Essay

As a Population Health Analyst at a hospital, I am continuously seeking ways to improve patient outcomes for patients. One area of particular interest is the early detection and management of chronic conditions such as diabetes, which can significantly impact patient health and well-being. In this essay, I explore the application of predictive modeling techniques to datasets containing information on patients' characteristics and diabetes diagnosis. Specifically, I analyze two datasets: one small with 2768 observations and another large with 100,000 observations. My goal is to understand how different algorithms perform in predicting diabetes and to identify the most influential features contributing to diabetes diagnosis.

The small dataset comprises ten columns, including patient characteristics such as pregnancies, glucose levels, and BMI, as well as the diabetes outcome. Initial analysis reveals no clear correlation between blood pressure values and diabetes, while BMI exhibits a significant association with diabetes risk. Similarly, the large dataset shows similar characteristics, with age and BMI standing out as significant predictors of diabetes. Particularly in the large dataset, individuals show increased risk of diabetes once their BMI surpasses 20, as people age, leading to higher BMIs and increased likelihood of diabetes diagnosis across genders. Notably, age and BMI emerge as significant predictors of diabetes in both datasets.

Logistic regression is initially chosen for its simplicity, interpretability, and suitability for binary classification tasks like diabetes prediction. It provides a baseline performance metric and helps understand linear relationships between features and the likelihood of diabetes. However, as decision tree and ensemble models outperform logistic regression in both datasets with accuracies of 97% and 96.72% respectively, they become the primary focus. Decision trees capture complex relationships and interactions between features, while ensemble methods like random forest and gradient boosting further enhance predictive accuracy by reducing overfitting and improving generalization performance. Overall, the choice of these algorithms is driven by their ability to handle complex relationships in the data and their superior performance in predicting diabetes risk.

Feature importance analysis reveals that glucose, BMI, and pregnancies are significant predictors of diabetes across both datasets. Moreover, age emerges as a crucial predictor in the large dataset, underscoring the impact of demographic factors on diabetes risk. Notably, the correlation between features varies between datasets, emphasizing the importance of dataset-specific analysis in predictive modeling.

In a business context, the choice of algorithm depends on the trade-off between interpretability and predictive accuracy. While logistic regression offers interpretability, decision tree-based algorithms provide superior predictive performance. For critical decision-making, such as identifying high-risk individuals for diabetes prevention programs, models with higher accuracy, such as gradient boosting, would be preferred.

Both using too much, and too little data can lead to errors in analysis. While using too much data may introduce noise and overfitting, using too little data may result in underfitting and limited model generalization. Therefore, it is essential to strike a balance between data volume and model complexity to ensure robust and reliable predictions.

Predictive modeling offers valuable insights into diabetes risk prediction, enabling early intervention and personalized healthcare strategies. By leveraging patient characteristics and diagnostic information, we demonstrate the effectiveness of decision tree-based algorithms in accurately predicting diabetes risk. Moreover, feature importance analysis highlights the critical role of glucose, BMI, and age in predicting diabetes across diverse datasets. Overall, this study underscores the importance of leveraging predictive modeling techniques to improve healthcare outcomes and inform decision-making in diabetes management.

## Pre-work

In this assignment, we want to perform various analyses and build predictive models to understand factors influencing diabetes and predict patients with diabetes based on the given features using 2 datasets from Kaggle https://www.kaggle.com/datasets

The datasets share identical structures. The data is structed in a table and have patient attributes like age, gender, and diabetes status.

Small data: https://www.kaggle.com/datasets/nanditapore/healthcare-diabetes

Big data: https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset/data

The sizes of the data differ significantly, with the smaller dataset containing around 3000 rows and the larger dataset containing 100,000 rows.

This makes logistic regression an appropriate starting point for analysis, while more advanced algorithms like Random Forest or Gradient Boosting could be advantageous for the larger dataset.

## Import libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
warnings.filterwarnings("ignore")

"""## Load data into dataframe

"""

## Load the small data: Added the data to my GitHub for reproducibility
dataS = pd.read_csv('https://raw.githubusercontent.com/Kossi-Akplaka/Data622/main/Assignment%201/Healthcare-Diabetes%20-%20Small%20Data.csv')

## Load the big data
dataB = pd.read_csv('https://raw.githubusercontent.com/Kossi-Akplaka/Data622/main/Assignment%201/diabetes_prediction_dataset%20-%20Big%20Data.csv')

"""## Small data

Let's perform data analysis on the small data.

### Data understanding
"""

dataS.head()

# Shape of the data
dataS.shape

dataS.columns

dataS.nunique()

dataS.describe()

dataS.Outcome.unique()

"""The small dataset contains 2768 rows and 10 columns. The column 'Id' is unique for each patient and identifies patients.

The 'BMI' stands out with an average value of 8. The patients' ages range from 21 to 81 years, covering a significant span of adulthood.

There are two distinct outcomes represented in the 'Outcome' column, with 0 for patients without diabetes and 1 indicating patients diagnosed with diabetes.

### Data cleaning
"""

#  Data type
dataS.dtypes

# Missing values
dataS.isna().sum()

"""The small dataset is clean and has no missing data.

### Features relationship
"""

# Let's plot the relationship between a patient's blood pressure value and the presence or absence of diabetes.

# Create a scatter plot for outcome 0
plt.figure(figsize=(10, 6))
plt.scatter(dataS.index[dataS['Outcome'] == 0], dataS.loc[dataS['Outcome'] == 0, 'BloodPressure'], color='black', s = 1, label='No diabetes')

# Create a scatter plot for outcome 1
plt.scatter(dataS.index[dataS['Outcome'] == 1], dataS.loc[dataS['Outcome'] == 1, 'BloodPressure'], color='red', s = 1, label='Diabetes')

# Add legend
plt.title('Scatter Plot of Blood Pressure Values by Outcome')
plt.xlabel('Index')
plt.ylabel('Blood Pressure')
plt.legend()
plt.show()

"""Based on the plotted data, there doesn't seem to be a discernible pattern indicating that blood pressure values alone directly correlate with the presence of diabetes.

This lack of correlation may be attributed to the variability in blood pressure levels throughout the day, which can fluctuate significantly based on factors such as stress levels.
"""

# Let's plot the relationship between a patient's BMI and the presence or absence of diabetes.

# Create a scatter plot for BMI with outcome 0
plt.figure(figsize=(10, 6))
plt.scatter(dataS.index[dataS['Outcome'] == 0], dataS.loc[dataS['Outcome'] == 0, 'BMI'], color='blue', s=1, label='No diabetes')

# Create a scatter plot for BMI with outcome 1
plt.scatter(dataS.index[dataS['Outcome'] == 1], dataS.loc[dataS['Outcome'] == 1, 'BMI'], color='red', s=1, label='Diabetes')

plt.title('Scatter Plot of BMI Values by Outcome')
plt.xlabel('Index')
plt.ylabel('BMI')
plt.legend()
plt.show()

"""The plot suggests a clear trend between BMI values and diabetes outcomes. Patients with a BMI higher than 30 have a higher likelihood of having diabetes.

Moreover, as a patient's BMI increases, their likelihood of having diabetes also rises. This trend underscores the significance of BMI as a predictive factor for diabetes risk.

### Features correlation

Let's create a heatmap of the correlation between the features in the small dataframe
"""

correlation = dataS.corr()
sns.heatmap(correlation, annot=True)

"""- The correlation analysis reveals that the glucose level is strongly correlated with the diabetes outcome. Additionally, features such as the number of pregnancies, BMI, age, and diabetes pedigree function show positive correlations with the diabetes outcome.

-  Age and the number of pregnancies are positively correlated with each other by 46%.

### Build a model
Based on the data, logistic regression is an appropriate machine learning to predict the outcome for patient. However, we will explore further models like decision tree model
"""

# Splitting the data into features X and target variable Y
X = dataS.drop('Outcome', axis = 'columns')
y = dataS.Outcome

# Scale the features X so that no single feature dominates the learning algorithm
from sklearn.preprocessing import StandardScaler
X_scaled =StandardScaler().fit_transform(X)

# Splitting the data into test and train
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_scaled,y,test_size = 0.2)

"""### Logistic Regression"""

np.random.seed(398)
#Logistic Regression
lr = LogisticRegression().fit(X_train, y_train)
lr.score(X_test,y_test)

# Use K-Fold to cross validate our logistic model
cross_val_score(LogisticRegression(), X,y,cv=ShuffleSplit(n_splits=5, test_size=0.2, random_state=0))

# Interpret coefficients to understand the impact of different features on the likelihood of having diabetes
for feature, coef in zip(X.columns, lr.coef_[0]):
    print(f'{feature}: {coef}')

"""Based on these coefficients, the features that have the greatest impact on the likelihood of having diabetes are Glucose, BMI, and Pregnancies, as they have the largest absolute coefficient values.

These features are the most important predictors of diabetes according to the logistic regression model.

### Decision Tree
"""

np.random.seed(398)
dtc = DecisionTreeClassifier().fit(X_train,y_train)
dtc.score(X_test,y_test)

"""The decision tree model perform a lot better than the logistic regression.

## Large data

Let's perform data analysis on the large data.

### Data understanding
"""

## Head of the data
dataB.head()

# Shape of the data
dataB.shape

dataB.nunique()

dataB.describe()

"""The large dataset contains 100,000 rows and 9 columns.

The 'BMI' stands out with an average value of 27. Just like the small data, There are two distinct outcomes represented in the 'Diabetes' column, with 0 for patients without diabetes and 1 indicating patients diagnosed with diabetes.

### Data cleaning
"""

#  Data type
dataB.dtypes

# Find the range of the Age in the data
min(dataB['age'])

"""The min of the age is 0.08 which is not quite right.

After researching, I found that Neonatal diabetes mellitus is a rare form of diabetes that occurs within the first 6 months of life.This can explained why the minimum age is 0.08 years old or 3 weeks after birth.
"""

dataB['age']

# Missing values
dataB.isna().sum()

"""After cleaning the data, we can visualize the data

### Features relationship
"""

dataB.head()

# Plot the relationship between bmi and age for diabetes outcome and gender.
g = sns.FacetGrid(dataB, col="gender", hue="diabetes")
g.map(sns.scatterplot, "age", "bmi", s = 5)
g.add_legend()

"""The plot above indicates that individuals are more prone to be diagnosed with diabetes once their BMI exceeds 20. Age also significantly influences this trend, as people age, their BMI tends to increase, further contributing to the likelihood of diabetes diagnosis for all genders.

### Features correlation
"""

# Let's create a heatmap of the correlation
correlation = dataB.corr()
sns.heatmap(correlation, annot=True)

"""The correlation analysis reveals that the glucose level and HBA1C level are strongly correlated with the diabetes outcome. Additionally, features such as the number of BMI, age, and whether or not you have hypertension show positive correlations with the diabetes outcome.

BMI and Hypertension outcomes are positively correlated to the age.

### Label Encoding with OneHotEncoding
"""

# Use One Hot Encoding to transform the object column 'gender'
dummies = pd.get_dummies(dataB.gender)
# Drop the smoking history column
dataB2 = pd.concat([dataB,dummies], axis = 'columns').drop(['gender', 'smoking_history'], axis = 'columns')
dataB2.head()

"""### Building the model

Based on the data, we will explore models like logistic regression, decision tree model, Random Forest and Gradient Boosting.
"""

# Splitting the data into features X and target variable Y
X = dataB2.drop('diabetes', axis = 'columns')
y = dataB2.diabetes

# Scale the features X so that no single feature dominates the learning algorithm
from sklearn.preprocessing import StandardScaler
X_scaled =StandardScaler().fit_transform(X)

# Splitting the data into test and train
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_scaled,y,test_size = 0.2)

"""### Logistic Regression"""

# Logistic regression
np.random.seed(398)
#Logistic Regression
lr = LogisticRegression().fit(X_train, y_train)
lr.score(X_test,y_test)

# Interpret coefficients to understand the impact of different features on the likelihood of having diabetes
for feature, coef in zip(X.columns, lr.coef_[0]):
    print(f'{feature}: {coef}')

"""Based on these coefficients, the features that have the greatest impact on the likelihood of having diabetes are Hemoglobin A1C level, Glucose, BMI, and the age, as they have the largest absolute coefficient values.

These features are the most important predictors of diabetes according to the logistic regression model.

### Random Forest
"""

reg = RandomForestClassifier()
reg.fit(X_train,y_train)
reg.score(X_test,y_test)

"""Random Forest does better than the logistic regression model

### Gradient boosting
"""

gb = GradientBoostingClassifier().fit(X_train,y_train)
gb.score(X_test,y_test)