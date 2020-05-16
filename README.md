# MSiA423 Template Repository

<!-- toc -->

- [Project Charter](#project-charter)
  - [Vision, Mission & Success Criteria](#mission:)
- [Directory structure](#directory-structure)
- [Acquire & ingest data](#acquire-&-ingest-data)
  * [Acquire data from source](#1.-acquire-data-from-source)
  * [Configure name of your S3 bucket](#2.-configure-the-name-of-your-s3-bucket)
  * [Initialize the database](#3.-initialize-the-database)
    * [Create a SQLITE database locally](#a.-create-a-sqlite-database-locally-(instead-of-rds):)
    * [Create a mysql database in RDS instance](#b.-create-a-mysql-database-in-rds-instance:**)
  * [Load raw dataset into S3 bucket](#4.-load-raw-dataset-into-S3-bucket)

<!-- tocstop -->

## Project Charter

Developer: **Aakanksha Sah**  <br/>
QA: **Jing Ren**

### Vision: Saving lives

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

## Acquire & ingest data

### 1. Acquire data from source

##### Download relevant data from Kaggle

This step has already been done for you, so feel free to move to the next step. This is mentioned here to enable reproducibility and ensure completeness of the document.

To acquire data for this app, visit [this](https://www.kaggle.com/ronitf/heart-disease-uci) page on Kaggle, scroll down and download the 'heart.csv' file. After downloading it, copy it from your Downloads folder and paste it in the `~/data/external`folder. 

By default, the name of the downloaded excel document is 'heart.csv' . Please do not change it.

*Note: Please connect to the Northwestern VPN for the remaining steps*

### 2. Configure the name of your S3 bucket

Go into the repository folder from your command terminal and enter the following command:

```
vi src/config.py
```

Enter the name of your S3 bucket in the line `S3_BUCKET = ""` inside double quotes. Save and close the vi editor.  

### 3. Initialize the database

You can create either a mysql database in RDS OR a SQLITE database locally. Refer to the relevant section based on your choice.

##### 		a. Create a SQLITE database locally (instead of RDS):

 1. Enter the following command from your terminal `vi src/config.py` and change the name of the variable DB_CHOICE to "SQLITE". 

 2. Build docker image using the command:

    ```
    docker build -t pseudo_doc .
    ```

 3. Use the docker image run the create_database.py file

    ```
    docker run --mount type=bind,source="$(pwd)"/data,target=/app/data pseudo_doc src/create_database.py
    ```

The SQLITE database `msia423_db.db` has now been created successfully in `~/data`. It contains a table `pd_predictions` which will be used later in the process to hold predictions for different parameter values.

Note: If for some reason, you are running this section again, add `--truncate` to the end of the last docker run --mount command. This will delete the table created from the previous iteration and create another one with the table schema

​	**b. Create a mysql database in RDS instance:**

1. Enter the following command from your terminal `vi .mysqlconfig` and change the credentials corresponding to the RDS instance where the database need to be created.
   Note: Please ensure that the name of the database in RDS is msia423_db.db

   ```
    ​	Set MYSQL_USER to the “master username” of your database server. 
    ​	Set MYSQL_PASSWORD to the “master password” of your database server. 
    ​	Set MYSQL_HOST to be the RDS instance endpoint from the console
    ​	Set MYSQL_PORT to be 3306
   ```

 2. Set the environment variables in your ~/.bashrc, by entering the following commands:

    ```
    echo 'source .mysqlconfig' >> ~/.bashrc
    source ~/.bashrc
    ```

 3. Build docker image

    ```
    docker build -t pseudo_doc .
    ```

 4. Run the docker container & initialize database

    ```
    sh run_docker.sh
    ```

The RDS database `msia423_db.db` has now been created successfully. It contains a table `pd_predictions` which will be used later in the process to hold predictions for different parameter values.

### 4. Load raw dataset into S3 bucket

Replace <aws_key> and <secret_key> in the command below based on your AWS credentials and run the command in the terminal

```
docker run -e AWS_ACCESS_KEY_ID=<aws_key> -e AWS_SECRET_ACCESS_KEY=<secret_key> pseudo_doc src/load_data_to_s3.py
```

The raw dataset has been uploaded to your S3 bucket successfully.







