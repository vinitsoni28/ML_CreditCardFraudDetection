import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

#Loading the dataset
data = pd.read_csv('creditcard.csv')

#Exploring dataset
print(data.columns)
print(data.shape)
print(data.describe())

data = data.sample(frac=0.1, random_state=1)
print(data.shape)

#Plotting histogram
data.hist(figsize=(20, 20))
plt.show()
plt.close()

#Determing number of fraud cases in the credit card dataset
fraud = data[data['Class'] == 1]
valid = data[data['Class'] == 0]

outlier_fraction = len(fraud) / float(len(valid))
print(outlier_fraction)
print('Fraud Cases: {}'.format(len(fraud)))
print('Valid Cases: {}'.format(len(valid)))

#Corelating matrix
corrmat = data.corr()
fig = plt.figure(figsize=(8, 8))
sns.heatmap(corrmat, vmax=.8, square=True)
plt.show()
plt.pause(5)
plt.close()

#Getting all the columns from the dataframe
columns = data.columns.tolist()

#Filtering the columns to omit the data not required
columns = [c for c in columns if c not in ["Class"]]

#Storing the data that used for further prediction
target = "Class"
X = data[columns]
Y = data[target]

#Printing the shapes of X and Y
print(X.shape)
print(Y.shape)

#Defining the random state
state = 1

#Defining the outlier detection methods
classifiers = {
    "Isolation Forest": IsolationForest(max_samples=len(X), contamination=outlier_fraction, random_state=state),
    "Local Outlier Factor": LocalOutlierFactor(n_neighbors=20, contamination=outlier_fraction)
}

#Fitting the Model
n_outliers = len(fraud)

for i, (clf_name, clf) in enumerate(classifiers.items()):
    #fitting the data and tagging outliers
    if clf_name == "Local Outlier Factor":
        y_pred = clf.fit_predict(X)
        scores_pred = clf.negative_outlier_factor_
    else:
        clf.fit(X)
        scores_pred = clf.decision_function(X)
        y_pred = clf.predict(X)

    #Reshaping the prediction values to 0 for valid and 1 for fraud
    y_pred[y_pred == 1] = 0
    y_pred[y_pred == -1] = 1

    n_errors = (y_pred != Y).sum()

    #Running classification metrics
    print('{}: {}'.format(clf_name, n_errors))
    print(accuracy_score(Y, y_pred))
    print(classification_report(Y, y_pred))


