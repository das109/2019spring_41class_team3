import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import csv

#### Import csv file

data = pd.read_csv("recommendation_system\\ratings.data")

#### Setup the imported data
ratings = np.transpose(data.values)
R = np.copy(ratings)
#### Array where [i, j] i corresponds to a item and j each users rating of the item
#### This is a one-hot matrix where if the user has rated a item, the value in the
#### corresponding index equals 1
R[R != 0] = 1

#### Convenient numbers to know
n_items, n_users = ratings.shape

#### Hyperparameter, defines how many "classification" classes algorithm optimizes.
#### The more items and users there are, the higher this value should be.
n_features = 2

#### Initialize weight matrices using the variables set up above.
itemFeatures = np.random.rand(n_items, n_features)
userPreferences = np.random.rand(n_users, n_features)

#### PARAMETERS >>
#   itemFeatures   np.array of size ("number of items", "number of feature classes")
#   userPreferences np.array of size ("number of users", "number of feature classes")
#   ratings         np.array of imported data
#   lam             Float for regularization purposes
####
#### RETURNS >>
#   loss            Float of calculated loss for the current weights
#   userPreferences_grad    np.array of the same size as userPreferences,
#                           contains gradients for every user's preference weights
#   itemFeatures_grad      np.array of the same size as itemFeatures,
#                           contains gradients for every items' feature weights
####
####
#### ////   Calculates loss, and gradients of the current weight values
####
def lossFunction(itemFeatures, userPreferences, ratings, lam):
    #### Calculates loss
    scores = np.square(np.dot(itemFeatures, np.transpose(userPreferences)) - ratings)
    loss = np.sum(scores[R == 1])/2 + ((np.sum(np.square(userPreferences)) + np.sum(np.square(itemFeatures)))/2*lam)

    #### Calculates gradients for both weight matrices
    scores = np.multiply(np.dot(itemFeatures, np.transpose(userPreferences)) - ratings, R)
    userPreferences_grad = np.dot(np.transpose(scores), itemFeatures) + lam*userPreferences
    itemFeatures_grad = np.dot(scores, userPreferences) + lam*itemFeatures

    return loss, userPreferences_grad, itemFeatures_grad


#### HYPERPARAMETERS >>
#### Number of training loops
loops = 500
#### Regularization hyperparamater, should be over 0
lam = 0
#### Learning rate alpha
alpha = 0.01

#### Initialize array to keep track if loss is decreasing or not
losses = []

#### Training loop, every loop calculates the gradients for itemFeatures and
#### userPreferences arrays and updates them with a learning rate of alpha
for i in range(loops):
    loss, userPreferences_grad, itemFeatures_grad = lossFunction(itemFeatures, userPreferences, ratings, lam)
    losses.append(loss)
    itemFeatures = itemFeatures - alpha * itemFeatures_grad
    userPreferences = userPreferences - alpha * userPreferences_grad


#### Calculate the predictions
scores = np.dot(itemFeatures, np.transpose(userPreferences))
#### We don't need predictions for items that user has already rated
scores[R==1] = 0
scores = np.transpose(scores)

itemIds = data.columns.tolist()
userIds = data.index.tolist()
sortedScores = []
for i in range(len(scores)):
    zips = sorted(zip(scores[i, :], itemIds), reverse=True)
    userItems = [userIds[i]]
    for j, k in zips:
        if (j > 0.0):
            userItems.append(k)
        else:
            break
    sortedScores.append(userItems)


#### Write to csv
with open('recommendation_system\\recommendations.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    #### Write a line for every user
    for i in sortedScores:
        writer.writerow(i)
