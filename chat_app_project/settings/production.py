import environ
from .development import *


env = environ.Env(DEBUG=(bool, False))

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

DATABASES = {"default": env.db("DATABASE_URL")}

ALLOWED_HOSTS = tuple(env.list("ALLOWED_HOSTS", default=[]))
