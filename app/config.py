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
