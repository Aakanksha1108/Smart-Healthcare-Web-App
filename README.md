# MSiA423 Template Repository

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

<!-- tocstop -->

## Project Charter
Developer: *Aakanksha Sah*
QA: *Jing Ren*

### Vision: 
One of the primary causes of treatment failures is the late identification and diagnosis of diseases. People are often unaware of different illnesses, the associated early indicators as well as their severity. This causes them to ignore the symptoms and let the condition worsen by the time they decide to finally visit a physician.

The **Smart Healthcare app**  aims to augment the treatment process for all users. It  requires the user to select their symptoms and in turn provides a ranked list of 10 potential disease conditions that could be causing it. The app also details out some additional information about those diseases and highlights the specific ones that are time-sensitive and should be taken seriously.

### Mission:
The **Smart Healthcare app** will be built on top of a [knowledge database](http://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html) of disease-symptom associations put together by the New York Presbyterian Hospital and made available for educational purposes. 

Supervised machine learning models will then leverage this data to predict the probability of various diseases corresponding to the selected symptoms. 

### Success criteria
 1. **For the business:** 
 
      A. *User downloads:* In the first month, the app should see a minimum of at least 1000 user downloads and a user-base growth of ~1% for the next 3 months. (Numbers decided based on the download patterns of similar apps in the market)
      
      B.  *Monthly Usage:* For the users who have downloaded the app, monthly usage should be ~2000 visits (Roughly, 2 visits per user per month)
 2. **For the model:** 
 
      As the response variable (disease condition) is categorical in nature, the measure for evaluating model performance would be correct classification rate (CCR). As this is real-world data and the symptom-disease relationship could be quite fuzzy, the target CCR is 70% (threshold, below which the model/app will not be deployed)

## Planning

### Initiatives

 - Assess quality (completeness, consistency and correctness) of the
   input data and perform feature engineering, where applicable
 - Develop multinomial classification models to identify patterns in symptoms (independent variables) and estimate their relationship with the various diseases (dependent variable)
  - Build an informative and easy-to-use app in a way that helps users better understand  their condition and treat it sooner rather than later

### Epics & Stories

- **Initiative 1:** Assess quality (completeness, consistency and correctness) of the
   input data and perform feature engineering, where applicable
   
   **Epic 1:** 
   - Perform an exhaustive exploratory data analysis of the various fields
	  
	**Stories:** <br /> 
	(1) Ensure detailed understanding of the meaning and value of the different columns in the dataset <br /> 
	(2) Calculate basic statistics, plot distributions, check for missing, null values or duplicate data <br /> 
   
   **Epic 2:** 
	- Explore scope for feature engineering and data manipulation
    
	 **Stories:** <br /> 
	(1) Are there certain symptoms that can be grouped because they mean the same thing and tend to occur together in the dataset? <br /> 
	(2) Is the dataset huge and should it be subsetted in any way for the purpose of this project? If yes, how should that be done? <br /> 
	(3)  Explore the possibility to add additional datasets (such as severity of disease, information about the disease)<br /> 
 
- **Initiative 2:**  
	- Develop multinomial classification models to identify patterns in symptoms (independent variables) and estimate their relationship with the various diseases (dependent variable)
   
     **Epic 1:** 
	- Run model iterations
	
	 **Stories:** <br /> 
	(1) Study about the different type of models that work well with such datasets (all categorical variables) <br /> 
	(2) How should the dataset be split into test and train? <br /> 
	(3) Run different models, compute accuracy (CCR, AUC) and consolidate results in a table <br /> 

  **Epic 2:** 
	- Select best model and pre-compute predictions
	
	**Stories:** <br /> 
	(1) For the best model, pre-compute the predicted probabilities for all diseases for all possible input combinations and store them in a dataset <br /> 

- **Initiative 3:** Build an informative and easy-to-use app in a way that helps users better understand  their condition and treat it sooner rather than later
   
   **Epic 1:** 
   - Design and build user interface
	  
	  
	**Stories:** <br /> 
	(1) Build the app with basic functionality - which allows user to enter inputs and then view the disease predictions <br /> 
	(2) Expose app to final dataset with the pre-computed predictions <br /> 
	(3) Add additional functionalities (such as, information about disease, its severity) <br /> 
	(4) Add visualizations talking about the number of yearly cases of diseases <br /> 
		
## Backlog

Note: 1 bar = small (<1 day), 2 bar = medium (2-3 days), 3 bar = large (4-5 days)

- Initiative1.Epic1.Story1 (1 bar) - PLANNED
- Initiative1.Epic1.Story2 (2 bars) - PLANNED
- Initiative1.Epic2.Story1 (1 bar) - PLANNED
- Initiative1.Epic2.Story2 (1 bar) - PLANNED
- Initiative2.Epic1.Story1 (1 bar) - PLANNED
- Initiative2.Epic1.Story2 (1 bar) - PLANNED
- Initiative2.Epic1.Story3 (2 bars) - PLANNED
- Initiative2.Epic2.Story1 (2 bars) - PLANNED
- Initiative3.Epic1.Story1 (3 bars) - PLANNED
- Initiative3.Epic1.Story2 (2 bars) - PLANNED

## Icelog
- Initiative1.Epic2.Story3
- Initiative3.Epic1.Story3
- Initiative3.Epic1.Story4

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.

### Workaround for potential Docker problem for Windows.

It is possible that Docker will have a problem with the bash script `app/boot.sh` that is used when running on a Windows machine. Windows can encode the script wrongly so that when it copies over to the Docker image, it is corrupted. If this happens to you, try using the alternate Dockerfile, `app/Dockerfile_windows`, i.e.:

```bash
 docker build -f app/Dockerfile_windows -t pennylane .
```

then run the same `docker run` command: 

```bash
docker run -p 5000:5000 --name test pennylane
```

The new image defines the entry command as `python3 app.py` instead of `./boot.sh`. Building the sample PennyLane image this way will require initializing the database prior to building the image so that it is copied over, rather than created when the container is run. Therefore, please **do the step [Create the database with a single song](#create-the-database-with-a-single-song) above before building the image**.
