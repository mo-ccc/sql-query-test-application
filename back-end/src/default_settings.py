import psycopg2
import dotenv
import os

dotenv.load_dotenv()


class Config():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    class Development(Config):
    DEBUG = True
    if os.getenv("DB_URI"):
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{get_from_env('DB_URI')}/developmentdb"

    class Testing(Config):
        TESTING = True
        if os.getenv("DB_URI"):
            SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{get_from_env('DB_URI')}/testingdb" # a separate database for tests only

    class Production(Config):
        if os.getenv("DB_URI"):
            SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{get_from_env('DB_URI')}/productiondb"

    environment = get_from_env('FLASK_ENV')
    
    if environment == 'development':
        configuration = Development()
    elif environment == 'testing':
        configuration = Testing()
    elif environment == 'production':
        configuration = Production()
    else:
        raise ValueError('FLASK_ENV is not set properly. use development, testing or production')