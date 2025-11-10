from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar .env
load_dotenv(BASE_DIR / ".env")

# ============================
# Segurança
# ============================
SECRET_KEY = os.getenv("SECRET_KEY", "troque-isto")

DEBUG = True

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "72.60.57.185,127.0.0.1,localhost"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "http://72.60.57.185",
    "https://72.60.57.185",
]

# ============================
# Aplicações
# ============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Apps do projeto
    "common",
    "automation.apps.AutomationConfig",
    "epe.apps.EpeConfig",
    "engobras.apps.EngobrasConfig",


]

# ============================
# Middlewares
# ============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise para arquivos estáticos em produção
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    # Seu middleware
    "core.middleware.DepartmentAccessMiddleware",
]

ROOT_URLCONF = "jfmetrics.urls"
WSGI_APPLICATION = "jfmetrics.wsgi.application"

# ============================
# Templates
# ============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # ➕ adicione estes:
                "automation.context_processors.user_flags",
                "automation.context_processors.notifications",
            ],
        },
    },
]

# ============================
# Banco de Dados (PostgreSQL/SQLite)
# ============================
if os.getenv("DB_ENGINE", "").lower() == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "jfmetricsdb"),
            "USER": os.getenv("DB_USER", "jfmetrics"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "CONN_MAX_AGE": 60,
            "ATOMIC_REQUESTS": True,
            "OPTIONS": {"sslmode": "prefer"},
        }
    }


# ============================
# Arquivos Estáticos
# ============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # para dev
STATIC_ROOT = BASE_DIR / "staticfiles"    # para produção
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============================
# Configurações de Login
# ============================
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "login"
LOGIN_REDIRECT_URL = "/after-login/"

# ============================
# Internacionalização
# ============================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = True

# URLs de autenticação (usando suas rotas existentes)
LOGIN_URL = "login"                 # nome da URL de login (a sua está em path("login/", ... name="login"))
LOGOUT_REDIRECT_URL = "login"       # após sair, volta pro login
LOGIN_REDIRECT_URL = "/after-login/"  # após logar, vai para essa rota que você já tem
