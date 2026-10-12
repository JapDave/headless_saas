"""Isolated SQLite settings for fast local tests. Production uses PostgreSQL."""
from .settings import *

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
SECRET_KEY = "test-only-key-not-for-deployment"
