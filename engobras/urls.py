# engobras/urls.py
from django.urls import path
from . import views

app_name = "engobras"

urlpatterns = [
    # Dashboard / expediente
    path("", views.dashboard, name="dashboard"),
    path("workday/start/",  views.start_workday,  name="start_workday"),
    path("workday/close/",  views.close_workday,  name="close_workday"),

    # Atividades
    path("activity/new/",             views.activity_create, name="activity_create"),
    path("activity/<int:pk>/start/",  views.activity_start,  name="activity_start"),
    path("activity/<int:pk>/pause/",  views.activity_pause,  name="activity_pause"),
    path("activity/<int:pk>/resume/", views.activity_resume, name="activity_resume"),
    path("activity/<int:pk>/finish/", views.activity_finish, name="activity_finish"),

    # Páginas simples
    path("profile/",   views.profile,  name="profile"),
    path("settings/",  views.settings, name="settings"),

    # Projetos / EAP
    path("projetos/", views.project_list, name="project_list"),
    path("eap/",      views.eap_view,     name="eap"),

    # Colaboradores & relatórios
    path("colaboradores/",                    views.collaborator_list,        name="collaborator_list"),
    path("relatorios/",                       views.reports_entry,            name="reports_entry"),
    path("colaboradores/<int:pk>/dashboard/", views.collaborator_dashboard,   name="collaborator_dashboard"),

    # Tempo real
    path("tempo-real/",           views.realtime,          name="realtime"),
    path("tempo-real/fragment/",  views.realtime_fragment, name="realtime_fragment"),

    # Relatórios / exports
    path("relatorios/geral/",                 views.department_report,          name="department_report"),
    path("relatorios/geral/pdf/",             views.department_report_pdf,      name="department_report_pdf"),
    path("relatorios/colaborador/<int:pk>/xlsx/", views.collaborator_report_xlsx, name="collaborator_report_xlsx"),
    path("reports/global/xlsx/",              views.global_report_xlsx,         name="global_report_xlsx"),
]
