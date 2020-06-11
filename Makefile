S3_DOWNLOAD_PATH=data/raw_data
CLEAN_DATA_PATH=data/interim_files
MODEL_FILES=data/interim_files
SCORED_DATA_PATH=data/interim_files
TRUNCATE_FLAG=0
s3_upload: config/config.yaml
	docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="`pwd`",target=/app/ pseudo_doc run.py upload --config=config/config.yaml

s3_download: config/config.yaml
	docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="`pwd`",target=/app/ pseudo_doc run.py download --config=config/config.yaml --output=${S3_DOWNLOAD_PATH}

step_clean: config/config.yaml
	docker run --mount type=bind,source="`pwd`",target=/app/ pseudo_doc run.py clean_data --input=$(S3_DOWNLOAD_PATH)/heart.csv --config=config/config.yaml --output=${CLEAN_DATA_PATH}/clean_data.csv

step_model: step_clean config/config.yaml
	docker run --mount type=bind,source="`pwd`",target=/app/ pseudo_doc run.py build_models --input=${CLEAN_DATA_PATH}/clean_data.csv --config=config/config.yaml --output=${MODEL_FILES}/model_results.csv

step_score: step_model
	docker run --mount type=bind,source="`pwd`",target=/app/ pseudo_doc run.py score_data --input=data/external/to_be_scored.csv --output=${SCORED_DATA_PATH}/scored_data.csv --model=${MODEL_FILES}/finalized_model.sav

create_database: step_score
	docker run -e SQLALCHEMY_DATABASE_URI -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_HOST -e MYSQL_PORT -e DATABASE_NAME --mount type=bind,source="`pwd`",target=/app/ pseudo_doc run.py database --input=${SCORED_DATA_PATH}/scored_data.csv --truncate=${TRUNCATE_FLAG}

run_app:
	docker run -e SQLALCHEMY_DATABASE_URI -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_HOST -e MYSQL_PORT -e DATABASE_NAME -p 5000:5000 --name test app app.py

tests:
	docker run pseudo_doc -m pytest test/*

all: s3_download step_clean step_model step_score create_database tests

.PHONY: s3_download step_clean step_model step_score create_database tests all