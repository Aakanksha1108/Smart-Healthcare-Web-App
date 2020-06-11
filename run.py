import pickle
import argparse
import logging
import yaml
import pandas as pd

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger('run.py')

from src.clean_data import clean_data
from src.write_to_s3 import write_to_s3
from src.read_from_s3 import read_from_s3
from src.build_models import build_models
from src.score_data import score_data
from src.create_database import create_database_main

if __name__ == '__main__':

    # Parses the different arguments in the docker run statement
    parser = argparse.ArgumentParser(description="Acquire, create features, and build model from heart data")
    parser.add_argument('step', help='Which step to run', choices=['upload','download','clean_data','build_models',\
                                                                   'score_data','database'])
    parser.add_argument('--input', '-i', default=None, help='Path to input data')
    parser.add_argument('--config', default=None, help='Path to configuration file')
    parser.add_argument('--output', '-o', default=None, help='Path to save output CSV (optional, default = None)')
    parser.add_argument('--model', '-m', default=None, help='Path to trained model object')
    parser.add_argument("--truncate", "-t", default=None, help="If given, delete current records\
     from pd_predictions table before create_all ""so that table can be recreated without unique id issues ")

    args = parser.parse_args()
    truncate_flag = 0

    # Load configuration file for parameters and tmo path
    if args.config is not None:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

    # Picks up the input file specified in the docker run statement
    if args.input is not None:
        input = pd.read_csv(args.input)
        logger.info('Input data loaded from %s', args.input)

    # Picks up the trained model object from the location specified in docker run
    if args.model is not None:
        with open(args.model, 'rb') as file:
            input_2 = pickle.load(file)
        logger.info('Trained model object loaded from %s', args.model)

    # Runs the python files corresponding to the step mentioned in docker run
    if args.step == 'clean_data':
        output = clean_data(input, **config['clean_data'])
    elif args.step == 'upload':
        output = write_to_s3(**config['upload'])
    elif args.step == 'download':
        path = args.output
        output = read_from_s3(**config['download'], RAW_CSV_PATH=path)
    elif args.step == 'build_models':
        output, auc, confusion, accuracy, classification_report, model = build_models(input,**config['build_models'])
        path_levels = len(args.output.split('/'))
        path = ''
        for i in range(0,path_levels-1):
            path = path + args.output.split('/')[i] + '/'
        model_accuracy_file = path + 'model_accuracy.txt'
        with open(model_accuracy_file, "w") as f:
            f.write("Area under the curve\n")
            f.write(str(auc))
            f.write("\n")
            f.write("\nConfusion matrix\n")
            f.write(str(confusion))
            f.write("\n")
            f.write("\nAccuracy\n")
            f.write(str(accuracy))
            f.write("\n")
            f.write("\nClassification report\n")
            f.write(str(classification_report))
        logger.info("Model accuracy details saved successfully")
        # save the model to disk
        pickle_model_file = path +'finalized_model.sav'
        pickle.dump(model, open(pickle_model_file, 'wb'))
        logger.info("Model saved as a pickle file successfully")
    elif args.step == 'score_data':
        output = score_data(input,input_2)
    elif args.step == 'database':
        if args.truncate == '1':
            truncate_flag=1
        create_database_main(input,truncate_flag)

    # Saves output in specified location in docker run
    if args.output is not None and args.step !='download':
        output.to_csv(args.output, index=False)
        logger.info("Output saved to %s" % args.output)