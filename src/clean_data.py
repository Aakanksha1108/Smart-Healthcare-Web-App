import os
import logging

logger = logging.getLogger(__name__)

# Adding column names to data
def clean_data(df, col_names):
    """
        Cleans the data and makes it ready for modeling
        Input:
            Dataframe: Raw dataset downloaded from s3
            col_names: list of column names
        Returns:
            Cleaned data
    """

    try:
        df.columns = col_names
    except Exception as e:
        logger.error("Mismatch in the size of dataframe columns and column_names specified in YAML")
        raise SystemExit()

    # Orchestrates all the steps of data cleaning
    temp = check_columns_datatypes(df)
    df2 = missing_value_treatment(df)
    df3,temp = age_impute_invalid_values(df2)
    df4,temp = sex_impute_invalid_values(df3)
    df5,temp = cp_impute_invalid_values(df4)
    df6,temp = bp_impute_invalid_values(df5)
    df7,temp = sc_impute_invalid_values(df6)
    df8,temp = fbs_impute_invalid_values(df7)
    df9,temp = ecg_impute_invalid_values(df8)
    df10,temp = mhr_impute_invalid_values(df9)
    df11,temp = ia_impute_invalid_values(df10)
    df12,temp = std_impute_invalid_values(df11)
    df13,temp = slope_impute_invalid_values(df12)
    df14,temp = nov_impute_invalid_values(df13)
    df15,temp = thal_impute_invalid_values(df14)
    df16,temp = diag_impute_invalid_values(df15)

    logger.info("Data is clean and ready to use")
    return df16


def check_columns_datatypes(df):
    """
        Function to check if the datatypes of all columns are correct
        Input: Dataframe
        Returns: Flag that indicates that the datatypes of all columns are correct
    """
    temp = 0
    if (len(df.select_dtypes(include=["float64", "int64", "int", "float"]).columns) == 14):
        logger.info("The datatypes of all columns in the dataset are valid")
        temp = 1
    else:
        logger.warning("The datatype of one or columns in the dataset are invalid")
        raise SystemExit()
    return temp


def missing_value_treatment(df):
    """
        Function that imputes missing values
        Input: Dataframe
        Returns:
            Dataframe with imputed missing values
    """
    try:
        df_mode = df.mode()
        for x in df.columns.values:
            df[x] = df[x].fillna(value=df_mode[x].iloc[0])
        logger.info("Missing values in the data have been removed or imputed successfully")
    except Exception as e:
        logger.warning("An error occurred while trying to impute missing values")
    return df


def age_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['age'].mode()[0]
        df['age'].values[df['age'] > 120] = mode_val
        df['age'].values[df['age'] < 1] = mode_val
    except KeyError:
        logger.warning("Column 'age' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'age' could not be replaced")
        temp = 1
    return df,temp

def sex_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['sex'].mode()[0]
        df['sex'].values[df['sex'] > 1] = mode_val
        df['sex'].values[df['sex'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'sex' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'sex' could not be replaced")
        temp = 1
    return df,temp

def cp_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['chest_pain'].mode()[0]
        df['chest_pain'].values[df['chest_pain'] > 3] = mode_val
        df['chest_pain'].values[df['chest_pain'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'chest_pain' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'chest_pain' could not be replaced")
        temp = 1
    return df,temp

def bp_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['blood_pressure'].mode()[0]
        df['blood_pressure'].values[df['blood_pressure'] > 250] = mode_val
        df['blood_pressure'].values[df['blood_pressure'] < 50] = mode_val
    except KeyError:
        logger.warning("Column 'blood_pressure' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'blood_pressure' could not be replaced")
        temp = 1
    return df, temp

def sc_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['serum_cholesterol'].mode()[0]
        df['serum_cholesterol'].values[df['serum_cholesterol'] > 750] = mode_val
        df['serum_cholesterol'].values[df['serum_cholesterol'] < 50] = mode_val
    except KeyError:
        logger.warning("Column 'serum_cholesterol' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'serum_cholesterol' could not be replaced")
        temp = 1
    return df, temp

def fbs_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['fasting_blood_sugar'].mode()[0]
        df['fasting_blood_sugar'].values[df['fasting_blood_sugar'] > 1] = mode_val
        df['fasting_blood_sugar'].values[df['fasting_blood_sugar'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'fasting_blood_sugar' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'fasting_blood_sugar' could not be replaced")
        temp = 1
    return df, temp

def ecg_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['electrocardiographic'].mode()[0]
        df['electrocardiographic'].values[df['electrocardiographic'] > 2] = mode_val
        df['electrocardiographic'].values[df['electrocardiographic'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'electrocardiographic' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'electrocardiographic' could not be replaced")
        temp = 1
    return df, temp

def mhr_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['max_heart_rate'].mode()[0]
        df['max_heart_rate'].values[df['max_heart_rate'] > 250] = mode_val
        df['max_heart_rate'].values[df['max_heart_rate'] < 50] = mode_val
    except KeyError:
        logger.warning("Column 'max_heart_rate' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'max_heart_rate' could not be replaced")
        temp = 1
    return df, temp

def ia_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['induced_angina'].mode()[0]
        df['induced_angina'].values[df['induced_angina'] > 2] = mode_val
        df['induced_angina'].values[df['induced_angina'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'induced_angina' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'induced_angina' could not be replaced")
        temp = 1
    return df, temp

def std_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['ST_depression'].mode()[0]
        df['ST_depression'].values[df['ST_depression'] > 250] = mode_val
        df['ST_depression'].values[df['ST_depression'] < 50] = mode_val
    except KeyError:
        logger.warning("Column 'ST_depression' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'ST_depression' could not be replaced")
        temp = 1
    return df, temp

def slope_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['slope'].mode()[0]
        df['slope'].values[df['slope'] > 2] = mode_val
        df['slope'].values[df['slope'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'slope' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'slope' could not be replaced")
        temp = 1
    return df, temp

def nov_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['no_of_vessels'].mode()[0]
        df['no_of_vessels'].values[df['no_of_vessels'] > 4] = mode_val
        df['no_of_vessels'].values[df['no_of_vessels'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'no_of_vessels' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'no_of_vessels' could not be replaced")
        temp = 1
    return df,temp

def thal_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['thal'].mode()[0]
        df['thal'].values[df['thal'] > 3] = mode_val
        df['thal'].values[df['thal'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'thal' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'thal' could not be replaced")
        temp = 1
    return df,temp

def diag_impute_invalid_values(df):
    """
       Replaces the invalid values in the column with mode
       Input: dataframe
       Returns: Dataset with the invalid values replaced with the mode of that column
    """
    temp = 0
    try:
        mode_val = df['diagnosis'].mode()[0]
        df['diagnosis'].values[df['diagnosis'] > 1] = mode_val
        df['diagnosis'].values[df['diagnosis'] < 0] = mode_val
    except KeyError:
        logger.warning("Column 'diagnosis' does not exist")
        temp = 1
    except Exception as e:
        logger.warning("The invalid values in the column 'diagnosis' could not be replaced")
        temp = 1
    return df,temp