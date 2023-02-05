############################################################################
#
# Assignment 1
#
# Purpose: Data preprocessing, logistic regression and decision tree
#
# Author: Timur Dzhafari
# Contact: tdzhafar@uncc.edu tdzhafari@gmail.com
#
############################################################################

############################################################################
#                           Dependencies
############################################################################

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor

#############################################################################
#                           Main logic
############################################################################


def main_func():
    """
    This function will drive the logic, which can be split into 3 parts:
    1) preprocessing of the data, 2) logistic regression building
    3) decision tree building.
    """

    # creating a path to the csv file with the dataset
    path_to_inq2015_file = Path(__file__).parent / 'inq2015.csv'

    try:
        df_td = pd.read_csv(path_to_inq2015_file)
    except FileNotFoundError:
        print('Please make sure inq2015.csv is named correctly and located in the same folder with this script or provide a full path to the file.')

    preprocess_data('logistic regression', df_td)

############################################################################
#                           Helper functions
############################################################################


def preprocess_data(model_type, inq_df_td):
    """
    This function will preprocess the dataframe and prepare it for the model
    building.
    """
    if model_type == 'logistic regression':
        inq_df_td.describe()
        df_desc_td = inq_df_td.describe().transpose()

        df_dtypes_td = pd.DataFrame({'Data Type': inq_df_td.dtypes})

        df_dtypes_td.index = inq_df_td.columns
        df_desc_td = df_desc_td.join(df_dtypes_td)

        # print(df_desc_td)
        # print(df_desc_td.shape)

        df_desc_rounded_td = df_desc_td[[
            'mean', 'std', 'min', '25%', '50%', '75%', 'max']].round(4)

        # Calculate the variable descriptions

        desc_td = df_desc_td
        desc_td = df_desc_rounded_td

        # Plot the variable descriptions using Matplotlib
        fig, ax = plt.subplots(figsize=(18, 16))
        ax.axis('tight')
        ax.axis('off')

        # The table content
        the_table = ax.table(cellText=desc_td.values,
                             rowLabels=desc_td.index,
                             colLabels=desc_td.columns,
                             cellLoc='center',
                             loc='center')

        # plt.show()

        # analysis to see which variables to reject
        # I need first to see if I have any NULL values in the dataset

        missing_values_td = inq_df_td.isnull().mean() * 100

        # Print the results
        #print(missing_values_td[missing_values_td > 25])
        #print('the columns above are to be omitted due to high count of missing values')

        missing_values_td = inq_df_td.isnull().sum()/len(inq_df_td)
        print(missing_values_td[missing_values_td != 0])

        # imputation
        col_names_for_imputation = [
            'TERRITORY', 'sex', 'avg_income', 'distance']

        inq_df_td[col_names_for_imputation] = inq_df_td[col_names_for_imputation].fillna(
            inq_df_td[col_names_for_imputation].mean())
        inq_df_td.describe(include='all')

        # important note: Ethnicity has the top value to be "C" I will impute NA's based on that.
        # imputing nominal variable
        inq_df_td['ETHNICITY'] = inq_df_td['ETHNICITY'].fillna('C')

        # removing the columns that have missing values over the set threshold of 25%
        inq_df_td = inq_df_td.drop(['ACADEMIC_INTEREST_1', 'ACADEMIC_INTEREST_2',
                                    'satscore', 'telecq', 'IRSCHOOL', 'CONTACT_CODE1', 'CONTACT_DATE'], axis=1)
        inq_df_td.columns

        # next I will generate dummy variables from ethnicity column
        # print(inq_df_td['ETHNICITY'].unique())

        dummy_data_td = pd.get_dummies(inq_df_td[['ETHNICITY']])
        # print(dummy_data_td.describe())
        # print(dummy_data_td)

        dummy_data_td = dummy_data_td.set_index(inq_df_td.index)

        # now I will join those tables together
        X_td = pd.concat([inq_df_td, dummy_data_td], axis=1)

        # dop the ethnicity column as I have added dummy vars, I will also drop a random variable among the Enthnicity ones
        # to avoid multicollinearity.
        X_td = X_td.drop(['ETHNICITY', 'ETHNICITY_I'], axis=1)

        # eliminate negative values from distance
        #X_td['distance'] = X_td['distance'].apply(combine)
        skewness_df_td = X_td.skew(skipna=True)

        # print(skewness_df_td.columns())

        skewed_cols = []

        #print(X_td.hist(bins=X_td.shape[1], figsize=(15, 10)))
        print(X_td['distance'].describe(include='all'))
        print(X_td.head().to_string())

        # will prob need to drop this column
        print(X_td['TERRITORY'].unique())

        # plt.show()


def combine(x):
    """
    helper function that will be used to eliminate negative values for a column in the dataset.
    """
    if x > 0:
        return 1
    else:
        return 0


main_func()