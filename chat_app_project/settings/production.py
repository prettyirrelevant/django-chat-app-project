import environ
from .development import *

environ.Env.read_env()

env = environ.Env(DEBUG=(bool, False))

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

DATABASES = {"default": env.db("SQLITE_URL")}
