
#%%==============================================================================
# ################# TITANIC SURVIVAL PREDICTION #################
# ################# TITANIC SURVIVAL PREDICTION #################
# ################# TITANIC SURVIVAL PREDICTION #################
#==============================================================================

#%%==============================================================================
# # Importing the libraries
#==============================================================================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



import os
print(os.getcwd()) #know the current working dir
os.chdir("D:\\Knowledge\\github\\titanic-survival_prediction\\data") #set working dir
print(os.getcwd())
   
#%%==============================================================================
# # Importing the dataset
#==============================================================================
train = pd.read_csv('train.csv')
train.head()
train.info()
train.columns
#%%==============================================================================
# # Data Visualization ##
#==============================================================================
sns.set_style('whitegrid')
sns.countplot('Survived', data=train)
sns.countplot('Sex', data=train, hue='Survived')
sns.countplot('Pclass', data=train, hue='Survived')
sns.distplot(train['Age'].dropna(), bins=30)
sns.countplot('SibSp', data=train, hue='Survived')


#%%==============================================================================
# # Missing Value Check ##
#==============================================================================

sns.heatmap(train.isnull(), yticklabels=False, cbar=False)

#%%==============================================================================
# # Imputing Missing data ##
#==============================================================================

plt.figure(figsize = (10,7))
sns.boxplot(x='Pclass' , y='Age', data=train)

def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]
    
    if pd.isnull(Age):
        if Pclass == 1:
            return 37
        elif Pclass == 2:
            return 29
        else:
            return 24
        
    else:
        return Age

train['Age'] = train[['Age', 'Pclass']].apply(impute_age,axis=1)

#%%==============================================================================
# # Drop Missing data ##
#==============================================================================


train.drop('Cabin', inplace=True, axis=1) # drop entire column cabin
train.dropna(inplace=True) # drop 1 row in Embarked

train.head()

#%%==============================================================================
# # Encoding categorical data
#==============================================================================

sex = pd.get_dummies(train['Sex'], drop_first=True, prefix='sex')
embark = pd.get_dummies(train['Embarked'], drop_first=True, prefix='embark')
pclass = pd.get_dummies(train['Pclass'], drop_first=True, prefix='Pclass')

train = pd.concat([train, sex,embark, pclass], axis=1)

#%%==============================================================================
# # Drop Unnecessary columns
#==============================================================================


train.drop(['Pclass','Sex', 'Embarked' , 'Name' , 'Ticket', 'PassengerId'] , axis=1, inplace=True)
train.head()

#%%==============================================================================
# # Separate Dependent and Independent columns
#==============================================================================

X = train.drop('Survived', axis=1)
y = train['Survived']

#%%==============================================================================
# # Splitting the dataset into the Training set and Test set
#==============================================================================
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4, random_state = 101)

#%%==============================================================================
# # Logistic regression Model
#==============================================================================

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

#%%==============================================================================
# # Model Validation
#==============================================================================

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

print(classification_report(y_test, y_pred))

confusion_matrix(y_test, y_pred)

# %%=============================================================================
# =============================================================================
# # ########### KAGGLE SUBMISSION ##################
# =============================================================================
# =============================================================================

#%%==============================================================================
# # Importing the dataset
#==============================================================================

test = pd.read_csv('test.csv')
test.head()

#%%==============================================================================
# # Missing Value Check ##
#==============================================================================

sns.heatmap(test.isnull(), yticklabels=False, cbar=False)

#%%==============================================================================
# # Imputing Missing data ##
#==============================================================================

plt.figure(figsize = (10,7))
sns.boxplot(x='Pclass' , y='Age', data=test)

def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]
    
    if pd.isnull(Age):
        if Pclass == 1:
            return 37
        elif Pclass == 2:
            return 29
        else:
            return 24
        
    else:
        return Age
		
test['Age'] = test[['Age', 'Pclass']].apply(impute_age,axis=1)

plt.figure(figsize = (10,17))
sns.boxplot(x='Pclass' , y='Fare', data=test)
test.groupby('Pclass').mean()

def impute_Fare(cols):
    Fare = cols[0]
    Pclass = cols[1]
    
    if pd.isnull(Fare):
        if Pclass == 1:
            return 94
        elif Pclass == 2:
            return 22
        else:
            return 12
        
    else:
        return Fare
test['Fare'] = test[['Fare', 'Pclass']].apply(impute_age,axis=1)

#%%==============================================================================
# # Drop Missing data ##
#==============================================================================

test.drop('Cabin', inplace=True, axis=1) # drop entire column cabin
#test.dropna(inplace=True)

test.head()

#%%==============================================================================
# # Encoding categorical data
#==============================================================================


sex1 = pd.get_dummies(test['Sex'], drop_first=True, prefix='sex')
embark1 = pd.get_dummies(test['Embarked'], drop_first=True, prefix='embark')
pclass1 = pd.get_dummies(test['Pclass'], drop_first=True, prefix='Pclass')

test = pd.concat([test, sex1,embark1, pclass1], axis=1)

#%%==============================================================================
# # Drop Unnecessary columns
#==============================================================================


test.drop(['Pclass','Sex', 'Embarked' , 'Name' , 'Ticket'] , axis=1, inplace=True)
test.head()

#%%==============================================================================
# # Logistic regression Model Prediction
#==============================================================================

prediction = model.predict(test.drop('PassengerId', axis=1))

test['Survived'] = model.predict(test.drop('PassengerId', axis=1))

test.to_csv('output.csv', encoding='utf-8', index=False)
