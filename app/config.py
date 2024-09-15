<<<<<<< HEAD
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)  # Ensure correct format
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'ksdfjlasdkjflks'
config = Config()

=======
from datetime import timedelta
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    # Set JWT expiration to 1 week (7 days)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=1)

config = Config()
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600
