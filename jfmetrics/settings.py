# settings.py
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "troque-isto"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]  # bom ter no dev

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
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # ⇩⇩ ADICIONE o middleware de acesso por departamento AQUI (depois do AuthenticationMiddleware)
    "core.middleware.DepartmentAccessMiddleware",
]

ROOT_URLCONF = "jfmetrics.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            # seus CPs:
            "automation.context_processors.user_flags",
            "automation.context_processors.notifications",   # use a versão “safe” que te passei
            "core.context_processors.department_context",
        ]
    },
}]

WSGI_APPLICATION = "jfmetrics.wsgi.application"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# URLs de auth
LOGIN_URL = "login"                    # pode ser nome da URL (resolve_url cuida disso)
LOGOUT_REDIRECT_URL = "login"          # idem
LOGIN_REDIRECT_URL = "/after-login/"   # deixe só ESTA (remova a anterior "automation:dashboard")

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = True
