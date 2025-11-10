# engobras/admin.py
from django.contrib import admin
from .models import (
    Project, Milestone, GeneralActivity, SpecificActivity,
    Workday, Activity, ActivitySession,
)

# Obs.: títulos do admin (site_header/site_title/index_title)
# defina em APENAS UM app do projeto para não ficar sobrescrevendo.
# Se você já definiu em automation/admin.py, pode remover daqui.

# ---------------------- Projetos ----------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "cost_center", "location", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code", "cost_center", "location")

# ---------------------- EAP ---------------------------
class SpecificInline(admin.TabularInline):
    model = SpecificActivity
    extra = 0

@admin.register(GeneralActivity)
class GeneralAdmin(admin.ModelAdmin):
    list_display   = ("name", "milestone", "order", "is_active")
    list_filter    = ("milestone",)
    list_editable  = ("order", "is_active")
    search_fields  = ("name", "milestone__name")
    inlines        = [SpecificInline]

class GeneralInline(admin.TabularInline):
    model = GeneralActivity
    extra = 0

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display   = ("name", "order", "is_active")
    list_editable  = ("order", "is_active")
    search_fields  = ("name",)
    inlines        = [GeneralInline]

@admin.register(SpecificActivity)
class SpecificAdmin(admin.ModelAdmin):
    list_display  = ("name", "general", "order", "is_active")
    list_filter   = ("general__milestone", "general")
    search_fields = ("name", "general__name", "general__milestone__name")

# ---------------------- Atividades / Jornada ----------
class SessionInline(admin.TabularInline):
    model = ActivitySession
    extra = 0
    readonly_fields = ("started_at", "ended_at")

@admin.register(Workday)
class WorkdayAdmin(admin.ModelAdmin):
    list_display   = ("date", "collaborator", "is_open", "started_at", "ended_at")
    list_filter    = ("is_open", "date")
    search_fields  = ("collaborator__name",)
    autocomplete_fields = ("collaborator",)
    date_hierarchy = "date"

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    @admin.display(description="EAP")
    def eap(self, obj):
        return obj.eap_display()

    list_display = ("id", "collaborator", "project", "eap", "started_at", "finished_at", "is_active")
    list_filter  = ("is_active", "project", "milestone", "general", "specific")
    search_fields = (
        "collaborator__name", "project__name", "description",
        "milestone__name", "general__name", "specific__name",
    )
    autocomplete_fields = ("collaborator", "project", "milestone", "general", "specific")
    inlines = [SessionInline]
    list_select_related = ("collaborator", "project", "milestone", "general", "specific")
