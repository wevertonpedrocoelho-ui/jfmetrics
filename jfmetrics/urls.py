# jfmetrics/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views import after_login, choose_department_submit

urlpatterns = [
    path("admin/", admin.site.urls),

    path("login/",  auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    path("engauto/", include(("automation.urls", "automation"), namespace="engauto")),
    path("epe/",     include(("epe.urls",        "epe"),        namespace="epe")),

    path("after-login/", after_login, name="after_login"),
    path("choose-department/", choose_department_submit, name="choose_department_submit"),

    # só a raiz → /engauto/
    path("", RedirectView.as_view(url="/engauto/", permanent=False)),
]
