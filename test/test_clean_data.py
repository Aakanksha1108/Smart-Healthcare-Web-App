import pytest
import pandas as pd
import src.clean_data as cd

def test_happy_columns():
    """
    Happy path to check if the columns of all datatypes is checked correctly and the codes executes smoothly
    """
    input_df = pd.DataFrame([[20, 1, 0, 80, 150, 0, 1, 180, 0, 213, 0, 0, 0, 0],
                             [170, 1, 1, 180, 500, 0, 0, 167, 1, 213, 1, 2, 1, 0],
                              [40, 0, 2, 120, 620, 1, 2, 174, 1, 227, 0, 2, 1, 1],
                              [72, 0, 0, 90, 430, 0, 1, 155, 2, 197, 1, 4, 2, 1],
                              [56, 1, 3, 60, 420, 1, 0, 150, 1, 186, 2, 3, 3, 0],
                              [86, 0, 1, 220, 220, 0, 2, 135, 0, 195, 2, 1, 3, 1]],
                            columns=['age', 'sex', 'chest_pain', 'blood_pressure', 'serum_cholesterol',
                                     'fasting_blood_sugar',
                                     'electrocardiographic', 'max_heart_rate', 'induced_angina', 'ST_depression', \
                                     'slope', 'no_of_vessels', 'thal', 'diagnosis'])
    temp = cd.check_columns_datatypes(input_df)
    assert temp==1

def test_happy_age_imputation():
    """
    Happy path to check if invalid values in age is imputed as expected
    """
    input_df = pd.DataFrame([[20, 1, 0, 80, 150, 0, 1, 180, 0, 213, 0, 0, 0, 0],
                             [170, 1, 1, 180, 500, 0, 0, 167, 1, 213, 1, 2, 1, 0],
                              [40, 0, 2, 120, 620, 1, 2, 174, 1, 227, 0, 2, 1, 1],
                              [72, 0, 0, 90, 430, 0, 1, 155, 2, 197, 1, 4, 2, 1],
                              [56, 1, 3, 60, 420, 1, 0, 150, 1, 186, 2, 3, 3, 0],
                              [86, 0, 1, 220, 220, 0, 2, 135, 0, 195, 2, 1, 3, 1]],
                            columns=['age', 'sex', 'chest_pain', 'blood_pressure', 'serum_cholesterol',
                                     'fasting_blood_sugar',
                                     'electrocardiographic', 'max_heart_rate', 'induced_angina', 'ST_depression', \
                                     'slope', 'no_of_vessels', 'thal', 'diagnosis'])
    df_output, temp = cd.age_impute_invalid_values(input_df)
    input_df['age'][1]=20
    assert df_output.equals(input_df)

def test_happy_sex_imputation():
    """
    Happy path to check if invalid values in sex is imputed as expected
    """
    input_df = pd.DataFrame([[20, 2, 0, 80, 150, 0, 1, 180, 0, 213, 0, 0, 0, 0],
                             [170, 1, 1, 180, 500, 0, 0, 167, 1, 213, 1, 2, 1, 0],
                              [40, 0, 2, 120, 620, 1, 2, 174, 1, 227, 0, 2, 1, 1],
                              [72, 0, 0, 90, 430, 0, 1, 155, 2, 197, 1, 4, 2, 1],
                              [56, 1, 3, 60, 420, 1, 0, 150, 1, 186, 2, 3, 3, 0],
                              [86, 0, 1, 220, 220, 0, 2, 135, 0, 195, 2, 1, 3, 1]],
                            columns=['age', 'sex', 'chest_pain', 'blood_pressure', 'serum_cholesterol',
                                     'fasting_blood_sugar',
                                     'electrocardiographic', 'max_heart_rate', 'induced_angina', 'ST_depression', \
                                     'slope', 'no_of_vessels', 'thal', 'diagnosis'])
    df_output, temp = cd.sex_impute_invalid_values(input_df)
    input_df['sex'][0]=0
    assert df_output.equals(input_df)

def test_happy_cp_imputation():
    """
    Happy path to check if invalid values in chest_pain is imputed as expected
    """
    input_df = pd.DataFrame([[20, 2, 10, 80, 150, 0, 1, 180, 0, 213, 0, 0, 0, 0],
                             [170, 1, 1, 180, 500, 0, 0, 167, 1, 213, 1, 2, 1, 0],
                              [40, 0, 2, 120, 620, 1, 2, 174, 1, 227, 0, 2, 1, 1],
                              [72, 0, 0, 90, 430, 0, 1, 155, 2, 197, 1, 4, 2, 1],
                              [56, 1, 3, 60, 420, 1, 0, 150, 1, 186, 2, 3, 3, 0],
                              [86, 0, 1, 220, 220, 0, 2, 135, 0, 195, 2, 1, 3, 1]],
                            columns=['age', 'sex', 'chest_pain', 'blood_pressure', 'serum_cholesterol',
                                     'fasting_blood_sugar',
                                     'electrocardiographic', 'max_heart_rate', 'induced_angina', 'ST_depression', \
                                     'slope', 'no_of_vessels', 'thal', 'diagnosis'])
    df_output, temp = cd.cp_impute_invalid_values(input_df)
    input_df['chest_pain'][0]=1
    assert df_output.equals(input_df)

def test_happy_bp_imputation():
    """
    Happy path to check if invalid values in blood_pressure is imputed as expected
    """
    input_df = pd.DataFrame([[20, 2, 1, 280, 150, 0, 1, 180, 0, 213, 0, 0, 0, 0],
                             [170, 1, 1, 180, 500, 0, 0, 167, 1, 213, 1, 2, 1, 0],
                              [40, 0, 2, 120, 620, 1, 2, 174, 1, 227, 0, 2, 1, 1],
                              [72, 0, 0, 90, 430, 0, 1, 155, 2, 197, 1, 4, 2, 1],
                              [56, 1, 3, 60, 420, 1, 0, 150, 1, 186, 2, 3, 3, 0],
                              [86, 0, 1, 220, 220, 0, 2, 135, 0, 195, 2, 1, 3, 1]],
                            columns=['age', 'sex', 'chest_pain', 'blood_pressure', 'serum_cholesterol',
                                     'fasting_blood_sugar',
                                     'electrocardiographic', 'max_heart_rate', 'induced_angina', 'ST_depression', \
                                     'slope', 'no_of_vessels', 'thal', 'diagnosis'])
    df_output, temp = cd.bp_impute_invalid_values(input_df)
    input_df['blood_pressure'][0]=60
    assert df_output.equals(input_df)

def test_unhappy_sc_imputation():
    """
    Unhappy path to check if an error is generated if the column to be imputed is missing
    """
    input_df = pd.DataFrame([[20, 1, 0, 80, 150, 0, 1, 180, 0, 213, 0, 0, 0, 0],
                             [170, 1, 1, 180, 500, 0, 0, 167, 1, 213, 1, 2, 1, 0],
                              [40, 0, 2, 120, 620, 1, 2, 174, 1, 227, 0, 2, 1, 1],
                              [72, 0, 0, 90, 430, 0, 1, 155, 2, 197, 1, 4, 2, 1],
                              [56, 1, 3, 60, 420, 1, 0, 150, 1, 186, 2, 3, 3, 0],
                              [86, 0, 1, 220, 220, 0, 2, 135, 0, 195, 2, 1, 3, 1]],
                            columns=['age', 'sex', 'chest_pain', 'blood_pressure', 'serum_cholesterol',
                                     'fasting_blood_sugar',
                                     'electrocardiographic', 'max_heart_rate', 'induced_angina', 'ST_depression', \
                                     'slope', 'no_of_vessels', 'thal', 'diagnosis'])
    input_df = input_df.drop(['serum_cholesterol'], axis=1)
    df_output, temp = cd.sc_impute_invalid_values(input_df)

    assert temp==1

def test_unhappy_fbs_imputation():
    """
    Unhappy path to check if an error is generated if the column to be imputed is missing
    """
    input_df = pd.DataFrame([[20, 1, 0, 80, 150, 0, 1, 180, 0, 213, 0, 0, 0, 0],
                             [170, 1, 1, 180, 500, 0, 0, 167, 1, 213, 1, 2, 1, 0],
                              [40, 0, 2, 120, 620, 1, 2, 174, 1, 227, 0, 2, 1, 1],
                              [72, 0, 0, 90, 430, 0, 1, 155, 2, 197, 1, 4, 2, 1],
                              [56, 1, 3, 60, 420, 1, 0, 150, 1, 186, 2, 3, 3, 0],
                              [86, 0, 1, 220, 220, 0, 2, 135, 0, 195, 2, 1, 3, 1]],
                            columns=['age', 'sex', 'chest_pain', 'blood_pressure', 'serum_cholesterol',
                                     'fasting_blood_sugar',
                                     'electrocardiographic', 'max_heart_rate', 'induced_angina', 'ST_depression', \
                                     'slope', 'no_of_vessels', 'thal', 'diagnosis'])
    input_df = input_df.drop(['fasting_blood_sugar'], axis=1)
    df_output, temp = cd.fbs_impute_invalid_values(input_df)

    assert temp==1