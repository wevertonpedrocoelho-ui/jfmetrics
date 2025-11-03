# settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "troque-isto")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "72.60.57.185,127.0.0.1,localhost"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "http://72.60.57.185",
    "https://72.60.57.185",
]

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "django.contrib.humanize",
    "common",
    "automation.apps.AutomationConfig",
    "epe.apps.EpeConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise precisa vir logo após SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "core.middleware.DepartmentAccessMiddleware",
]

ROOT_URLCONF = "jfmetrics.urls"
WSGI_APPLICATION = "jfmetrics.wsgi.application"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = True

# URLs de autenticação (usando suas rotas existentes)
LOGIN_URL = "login"                 # nome da URL de login (a sua está em path("login/", ... name="login"))
LOGOUT_REDIRECT_URL = "login"       # após sair, volta pro login
LOGIN_REDIRECT_URL = "/after-login/"  # após logar, vai para essa rota que você já tem
