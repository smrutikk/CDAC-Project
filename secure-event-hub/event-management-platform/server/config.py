import os


class Config:
    # VULN A05: hardcoded fallback secret + debug on by default.
    # FIX: require env vars, no defaults, DEBUG=False.
    SECRET_KEY = os.environ.get("SECRET_KEY", "devsecops-demo-secret")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "devsecops-demo-jwt")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///events.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
