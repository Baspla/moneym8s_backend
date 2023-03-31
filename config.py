# Flask Configuration

DEBUG = True

# SQLAlchemy Configuration

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5432/money'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SSO_URL = "https://guard.timmorgner.de/sso"
