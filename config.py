# Flask Configuration
from os import environ

DEBUG = True

# SQLAlchemy Configuration

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "postgresql://postgres:mysecretpassword@localhost:5432/money")
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SSO_URL = environ.get("SSO_URL", "https://guard.timmorgner.de")
