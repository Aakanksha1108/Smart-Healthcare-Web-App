import pandas as pd
import logging
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)

def build_models( df, target_column, columns_for_modeling, test_size=0.3, n_estimators=10, max_depth=3):
    """
    Wrapper function that orchestrates all the different steps of modeling
    Input: df - Input dataframe with features and target
           target_column - Specifies which one is the target variable
           columns_for_modeling - Specifies which variables should be used as features
           test_size - Specifies the fraction of the dataset that should be used for testing
           n_estimators - This is a hyperparameter specific to the random forest model
           max_depth - This is a hyperparameter specific to the random forest model
    Returns: fi - Feature importances as a dataframe
             auc, confusion, accuracy, classification_model - Accuracy metrics
             model_fit - Fitted model object
    """

    # Checks if input dataset is a dataframe
    if type(df) is not pd.DataFrame:
        logger.error("Input data is not a dataframe")
        raise SystemExit()

    # Orchestration of the different steps involved in modeling
    features, target, temp = split_features_target(df, target_column, columns_for_modeling)
    X_train, X_test, y_train, y_test = split_test_train(features, target, test_size)
    X_train, X_test = stan_norm(X_train, X_test)
    model_fit = rf_model(X_train, y_train,n_estimators, max_depth)
    ypred_proba_test, ypred_bin_test = fit_test(model_fit, X_test)
    auc, confusion, accuracy, classification_report = compute_accuracy(y_test, ypred_proba_test, ypred_bin_test)
    fi = feature_importances(columns_for_modeling, model_fit)

    return fi, auc, confusion, accuracy, classification_report, model_fit



def split_features_target(df, target_column, columns_for_modeling):
    """
        Splits the dataframe into two datasets (Features and target)
        Input: df - Dataframe
                target_column - Specifies the target column
                columns_for_modeling - List of columns to be used as features during modeling
        Returns:
            features - dataframe with features only
            target - dataframe with target only
            temp - This is a flag that indicates a KeyError during function execution
    """

    temp = 0
    try:
        features = df[columns_for_modeling]
        target = df[target_column]
    except KeyError:
        logger.warning("One or more of the referenced columns in the dataframe does not exist")
        temp = 1
        raise SystemExit()
    return (features, target, temp)



def split_test_train(features, target, test_size):
    """
        Splits dataset into test and train
        Input: features, target - dataframes with independent and dependent variables respectively
                test_size - fraction of the dataframe to be used as test dataset
        Returns:
            X_train, X_test, y_train, y_test - train and test independent variables dataset, train and test response var
    """
    try:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_size, random_state=1408)
    except ValueError as e1:
        logger.error(e1)
        raise SystemExit()
    except Exception as e2:
        logger.error(e2)
        raise SystemExit()
    return (X_train, X_test, y_train, y_test)



def stan_norm(X_train,X_test):
    """
        Standardize and normalize the independent features dataframe
        Input:
            X_train, X_test - train and test independent features dataframe
        Returns:
            X_train, X_test - Standardized and normalized version of the train and test independent features dataframe
    """
    try:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    except Exception as e:
        logger.error("Unable to standardize or normalize data")
        raise SystemExit()
    return (X_train,X_test)



def rf_model(X_train, y_train,n_estimators, max_depth):
    """
        Build a random forest model on the train dataset
        Inpyt:
            X_train, y_train - Train dataset
            n_estimators, max_depth - model hyperparameters
        Returns:
            model_fit: Fitted model object
    """
    try:
        model = sklearn.ensemble.RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, \
                                                        random_state=1408)
        model_fit = model.fit(X_train, y_train)
    except Exception as e:
        logger.error("Unable to build random forest classification model")
        raise SystemExit()
    logger.info("Random forest model to identify patients with heart risk built successfully")
    return (model_fit)



def fit_test(model_fit, X_test):
    """
        Fitting trained model object to the test dataset
        Input:
            model_fit - Fitted model object
            X_test - Test dataset
        Returns:
            ypred_proba_test, ypred_bin_test - Predicted y values
    """
    try:
        ypred_proba_test = model_fit.predict_proba(X_test)[:, 1]
        ypred_bin_test = model_fit.predict(X_test)
    except Exception as e:
        logger.error("Unable to fit test data on the trained model")
        raise SystemExit()
    return (ypred_proba_test, ypred_bin_test)



def compute_accuracy(y_test, ypred_proba_test,ypred_bin_test):
    """
        Computed accuracy of model on the test dataset
        Input:
            y_test - Actual response variable values
            ypred_proba_test,ypred_bin_test - Predicted response variable values
        Returns:
               auc, confusion, accuracy, classification_report - Accuracy metrics
    """
    try:
        auc = sklearn.metrics.roc_auc_score(y_test, ypred_proba_test)
        confusion = sklearn.metrics.confusion_matrix(y_test, ypred_bin_test)
        accuracy = sklearn.metrics.accuracy_score(y_test, ypred_bin_test)
        classification_report = sklearn.metrics.classification_report(y_test, ypred_bin_test)
        logger.info("Computed accuracy metrics successfully")
    except Exception as e:
        logger.error("Could not compute accuracy metrics")
        raise SystemExit()
    return (auc, confusion, accuracy, classification_report)



def feature_importances(columns_for_modeling,model_fit):
    """
        Computes feature importances
        Inputs:
            columns_for_modeling - List of features
            model_fit - Fitted model object
        Returns:
            feature importances - as a dataset
    """
    try:
        fi = pd.DataFrame({'feature': list(columns_for_modeling),'importance': model_fit.feature_importances_}). \
            sort_values('importance', ascending=False)
        logger.info("Estimated feature importances successfully")
    except Exception as e:
        logger.error("Could not compute feature importances")
        raise SystemExit()
    return fi