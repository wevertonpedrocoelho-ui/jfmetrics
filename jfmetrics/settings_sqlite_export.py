from .settings import *  # importa TUDO do settings atual

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Desativa context processors extras durante exportação para evitar ruído
for tpl in TEMPLATES:
    tpl["OPTIONS"]["context_processors"] = [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]
