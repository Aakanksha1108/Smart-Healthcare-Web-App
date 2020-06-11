import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.create_database import pd_predictions
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask("hc_app", template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """
    print("Index function")
    try:
        #input = db.session.query(pd_predictions).limit(app.config["MAX_ROWS_SHOW"]).all()
        #logger.debug("Index page accessed")
        prediction = db.session.query(pd_predictions).limit(1)
        return render_template('index.html', predictions=prediction)
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """
    try:
        age_int = int(request.form['age'])
        sex_int = int(request.form['sex'])
        chest_pain_int = int(request.form['chest_pain'])
        fasting_blood_sugar_int = int(request.form['fasting_blood_sugar'])
        electrocardiographic_int = int(request.form['electrocardiographic'])
        induced_angina_int = int(request.form['induced_angina'])
        thal_int = int(request.form['thal'])
        prediction = db.session.query(pd_predictions).filter(pd_predictions.age == age_int,
                                                             pd_predictions.sex == sex_int,
                                                             pd_predictions.chest_pain == chest_pain_int,
                                                             pd_predictions.fasting_blood_sugar == fasting_blood_sugar_int,
                                                             pd_predictions.electrocardiographic == electrocardiographic_int,
                                                             pd_predictions.induced_angina == induced_angina_int,
                                                             pd_predictions.thal == thal_int)

        return render_template('index.html',predictions=prediction)
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])