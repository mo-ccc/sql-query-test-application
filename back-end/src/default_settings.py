import psycopg2
import dotenv
import os

dotenv.load_dotenv()

def get_from_env(var_name):
    value = os.getenv(var_name)

    if not value:
        raise ValueError(f"{var_name} is not set")

    return value

class Config():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG = True
    if os.getenv("DEVELOPMENT_DB_URI"):
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{get_from_env('DEVELOPMENT_DB_URI')}"

class Testing(Config):
    TESTING = True
    if os.getenv("TESTING_DB_URI"):
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{get_from_env('TESTING_DB_URI')}/testingdb" # a separate database for tests only

class Production(Config):
    if os.getenv("PRODUCTION_DB_URI"):
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{get_from_env('PRODUCTION_DB_URI')}/productiondb"

environment = get_from_env('FLASK_ENV')

if environment == 'development':
    configuration = Development()
elif environment == 'testing':
    configuration = Testing()
elif environment == 'production':
    configuration = Production()
else:
    raise ValueError('FLASK_ENV is not set properly. use development, testing or production')