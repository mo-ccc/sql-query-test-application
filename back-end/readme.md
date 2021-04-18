# Instructions for Backend Deployment
## Dependencies
- Python3
- Python3 venv
- Postgresql

## Steps (Linux)
- Have postgresql running with an empty database and a role with full permissions for that database.
- Clone the repository to your machine: `git clone https://mo-ccc/sql-query-test-application.git`.
- Change directories to src: `cd sql-query-test-application/back-end/src`.
- Initialize a python virtual environment: `python3 -m venv venv`.
- Activate virtual environment: `source venv/bin/activate`.
- Install PIP dependencies: `pip install -r requirements.txt`.
- Make a copy of .env.example and rename to .env: `cp .env.example .env`.
- Edit the contents of .env to contain database connection details.
- Set flask to production `export FLASK_ENV=production`
- Set flask to run main.py `export FLASK_APP=main.py`
- initialize private schema for db `flask db_custom initialize_schema`
- create the models within the db `flask db upgrade`
- seed the questions (optional) `flask db_custom seed_question`
- seed the secondary tables (optional) `flask db_custom seed_secondary_tables`
- run `flask run`

## Steps (Windows)
- Have postgresql running with an empty database and a role with full permissions for that database.
- Clone the repository to your machine: `git clone https://mo-ccc/sql-query-test-application.git`.
- Change directories to src: `cd sql-query-test-application/back-end/src`.
- Initialize a python virtual environment: `python3 -m venv venv`.
- Activate virtual environment: `./venv/bin/activate.bat`.
- Install PIP dependencies: `pip install -r requirements.txt`.
- Make a copy of .env.example and rename to .env
- Edit the contents of .env to contain database connection details.
- Set flask to production `set FLASK_ENV=production`
- Set flask to run main.py `set FLASK_APP=main.py`
- initialize private schema for db `flask db_custom initialize_schema`
- create the models within the db `flask db upgrade`
- seed the questions (optional) `flask db_custom seed_question`
- seed the secondary tables (optional) `flask db_custom seed_secondary_tables`
- run `flask run`
