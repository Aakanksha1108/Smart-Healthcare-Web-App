# MSiA423 Template Repository

<!-- toc -->

[TOC]

## Project Charter

Developer: **Aakanksha Sah**  <br/>
QA: **Jing Ren**

### Vision: 'Empowering Patients. Protecting Lives'

The **Smart Healthcare App** will improve the lives and well-being of people by predicting their risk of potential disease conditions, from the comfort of their homes.

### Mission

The **Smart Healthcare App** is committed to producing the finest algorithms to sensitively and accurately detect diseases from easily measurable attributes or observable symptoms. Currently, it caters only to heart diseases and is built using a dataset obtained from [Kaggle](https://www.kaggle.com/ronitf/heart-disease-uci/kernels), but will be expanded to other conditions as well in the future. The key market segment is users from the age group of 15 to 85, who have an access to a phone. The app design facilitates simplicity and ease of use for users at either ends of the age spectrum. 

### Success criteria

 1. **For the business:** 

    A. *User downloads:* In the first month, the app should see a minimum of at least 1000 user downloads and a user-base growth of ~1% for the next 3 months. (Numbers decided based on the download patterns of similar apps in the market)

    B.  *Monthly Usage:* For the users who have downloaded the app, monthly usage should be ~2000 visits (Roughly, 2 visits per user per month)

 2. **For the model:** 

    As the response variable (heart disease) is categorical in nature, the measure for evaluating model performance would be correct classification rate (CCR). As this is real-world data and the symptom-disease relationship could be quite fuzzy, the target CCR is 70% (threshold, below which the model/app will not be deployed)

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

## Run model pipeline and application

Please note the following before you proceed:

- Ensure that you are connected to the Northwestern VPN
- Ensure that your docker app is running

### 1. Set AWS credentials as environment variables

Please set your AWS credentials as environment variables by executing the following commands:

```
export AWS_ACCESS_KEY_ID=<enter your key here>
export AWS_SECRET_ACCESS_KEY=<enter your secret key here>
```

If the user has access to my S3 bucket, then go to the next step after exporting your details above. If not, additionally do the following:

- Go to config/config.yaml and change S3_BUCKET_NAME appropriately
- Upload data to s3 by running the command 'make s3_upload' immediately after building the docker image for the pipeline (reference to Step 3)

### 2. Set RDS or local SQLITE database details as environment variables

- If you wish to create a **local SQLITE database** in a location of your preference, export SQLALCHEMY_DATABASE_URI using the command below

  ```
  export SQLALCHEMY_DATABASE_URI =<path to local database>
  ```

  By default, the app creates a local database using SQLALCHEMY_DATABASE_URI = 'sqlite:///data/msia423_db.db'

- If you wish to create an **RDS database**, execute the following commands

  ```
  export MYSQL_USER=<enter RDS host here>
  export MYSQL_PASSWORD=<enter RDS password here>
  export MYSQL_HOST=<enter host here>
  export MYSQL_PORT=<enter port here>
  export DATABASE_NAME=<enter database name here> 
  ```


### 3. Run the model pipeline

##### Execute the following commands to run the model pipeline:

```
docker build -t pseudo_doc .
make all
```

'make all' runs the entire model pipeline - (1) downloading data from S3 bucket, (2) cleaning the raw data, (3) building a model, (4) scoring data, (5) creating a database and (6) adding all predictions to it. The pipeline also saves all interim csv files and model outputs in a default location.

Note: If you changed the S3_BUCKET_NAME above, then remember to run 'make s3_upload' here after the docker build command and then run 'make all' to run the pipeline

##### Important configurations to note:

<u>a. In order to change the paths to the interim files</u>, change the location by assigning the path to the following variables while running the 'make all' command:

- S3_DOWNLOAD_PATH - To change the location of the downloaded raw dataset from S3 bucket. The default location for this is 'data/raw_data'

- CLEAN_DATA_PATH - To change the location of the cleaned dataset. The default location is 'data/interim_files'

- MODEL_FILES - To change the location of all model related artifacts. The default location is 'data/interim_files'

- SCORED_DATA_PATH - To change the location of the final scored dataset. The default location is 'data/interim_files'

  Example: To change the location of the downloaded file from S3, I will run the model pipeline using the following command

  ```
  docker build -t pseudo_doc .
  make all S3_DOWNLOAD_PATH=<file-path>
  ```

b. <u>If you are running this code for the second time and the local SQLITE database is already created</u>. You should delete the existing database and then create a new one or else you might run into an integrity error. You can do so by setting the TRUNCATE_FLAG to 1. Exact commands are mentioned below for reference:

```
docker build -t pseudo_doc .
make all TRUNCATE_FLAG=1
```

### 4. Run unit tests (optional)

Run unit tests using the following command.

```
make tests
```

### 		5. Run the application

##### 		Build a docker image and then run the application

```
docker build -f app/Dockerfile -t app .
make run_app
```

The terminal should now display
`* Running on http://0.0.0.0:5000/`

Click on the url to be directed to the application web page. Know more about your health condition and stay safe :)





