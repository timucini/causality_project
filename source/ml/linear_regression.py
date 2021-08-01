"""
This module is used to execute linear regression model.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def execute_linear_regression(data, feature_set, target_set):

    # Define variable of feature set
    X = data[feature_set]

    # Define variable of target set
    Y = data[target_set]

    # Define the linear regression model
    linear_regression = LinearRegression()

    # Fit the linear regression model
    linear_regression.fit(X, Y)

    # Perform prediction with the data
    Y_pred = linear_regression.predict(X)

    # Visualize the data set and the regression line
    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')
    plt.show()
