import os
import logging
import numpy as np

logger = logging.getLogger(__name__)

def score_data(df, model_pickle):
    """
    Scores dataset using the model
    Input:
        Dataframe, pickle model object
    Returns:
        Scored dataframe
    """
    try:
        y_prob = model_pickle.predict_proba(df)[:, 1]
        y_bin = model_pickle.predict(df)
    except Exception as e:
        logger.error("Error in scoring data")
        raise SystemExit()

    logger.info("Data scored using trained model object successfully")

    df['y_prob'] = np.round(y_prob * 100,2)
    df['y_bin'] = y_bin

    return df