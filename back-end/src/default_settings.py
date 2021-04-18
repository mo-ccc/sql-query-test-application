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
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{get_from_env('USERNAME')}:"
        f"{get_from_env('PASSWORD')}@{get_from_env('HOST')}:"
        f"{get_from_env('PORT')}/{get_from_env('DB_NAME')}"
    )
    SQLALCHEMY_BINDS = {
        "secondary_schema": (
            f"postgresql+psycopg2://interactor:"
            f"{get_from_env('PASSWORD')}@{get_from_env('HOST')}:"
            f"{get_from_env('PORT')}/{get_from_env('DB_NAME')}"
        )
    }

class Development(Config):
    DEBUG = True
    
class Testing(Config):
    TESTING = True

class Production(Config):
    pass

environment = get_from_env('FLASK_ENV')

if environment == 'development':
    configuration = Development()
elif environment == 'testing':
    configuration = Testing()
elif environment == 'production':
    configuration = Production()
else:
    raise ValueError('FLASK_ENV is not set properly. use development, testing or production')

if __name__ == "__main__":
    pass