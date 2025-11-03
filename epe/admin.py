# epe/admin.py
from django.contrib import admin
from django.utils import timezone

from .models import (
    Project, Workday,
    GeneralActivity, PanelSize,
    Activity, ActivitySession,
)

# (opcional) Se vários apps setarem isso, o último carregado prevalece
admin.site.site_header = "Painel administração"
admin.site.site_title  = "Admin"
admin.site.index_title = "Painel EPE"


# ----------------------------- Helpers ---------------------------------------
def _fmt_hms(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


# ----------------------------- Catálogos -------------------------------------
@admin.register(GeneralActivity)
class GeneralActivityAdmin(admin.ModelAdmin):
    list_display  = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name",)
    ordering      = ("order", "name")


@admin.register(PanelSize)
class PanelSizeAdmin(admin.ModelAdmin):
    list_display  = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name",)
    ordering      = ("order", "name")


# --------------------------------- Project -----------------------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ("name", "code", "cost_center", "location", "is_active")
    list_filter   = ("is_active",)
    search_fields = ("name", "code", "cost_center", "location")
    ordering      = ("name",)
    actions       = ["ativar", "inativar"]

    @admin.action(description="Ativar projetos selecionados")
    def ativar(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} projeto(s) ativado(s).")

    @admin.action(description="Inativar projetos selecionados")
    def inativar(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} projeto(s) inativado(s).")


# --------------------------------- Workday -----------------------------------
@admin.register(Workday)
class WorkdayAdmin(admin.ModelAdmin):
    list_display        = ("date", "collaborator", "is_open", "started_at", "ended_at")
    list_filter         = ("is_open", "date")  # evite listar todos colaboradores aqui
    search_fields       = ("collaborator__name",)
    autocomplete_fields = ("collaborator",)  # FK para common.Collaborator
    date_hierarchy      = "date"
    ordering            = ("-date", "collaborator__name")
    list_per_page       = 50

    actions = ["close_selected"]

    @admin.action(description="Fechar expedientes selecionados (encerra agora)")
    def close_selected(self, request, queryset):
        now = timezone.now()
        updated = queryset.filter(is_open=True).update(is_open=False, ended_at=now)
        self.message_user(request, f"{updated} expediente(s) fechado(s).")


# ------------------------------- Activity / Sessions --------------------------
class SessionInline(admin.TabularInline):
    model = ActivitySession
    extra = 0
    can_delete = True
    ordering = ("-started_at",)
    readonly_fields = ("duration_hms",)

    @admin.display(description="Duração")
    def duration_hms(self, obj):
        try:
            return _fmt_hms(obj.duration_seconds())
        except Exception:
            return "-"


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "collaborator",
        "project",
        "panel_name",
        "general",
        "panel_size",
        "started_at",
        "finished_at",
        "is_active",
        "hours_decimal",
        "hours_hms",
    )
    list_filter          = ("is_active", "general", "panel_size", "project")
    search_fields        = (
        "panel_name", "description",
        "general__name", "panel_size__name",
        "project__name", "collaborator__name",
    )
    date_hierarchy       = "started_at"
    ordering             = ("-id",)
    list_per_page        = 50
    list_select_related  = ("collaborator", "project", "general", "panel_size")
    autocomplete_fields  = ("collaborator", "project", "general", "panel_size")
    inlines              = [SessionInline]
    actions              = ["finish_selected", "pause_selected"]

    # Filtra os FKs no formulário para mostrar apenas opções ativas
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.filter(is_active=True).order_by("name")
        elif db_field.name == "general":
            kwargs["queryset"] = GeneralActivity.objects.filter(is_active=True).order_by("order", "name")
        elif db_field.name == "panel_size":
            kwargs["queryset"] = PanelSize.objects.filter(is_active=True).order_by("order", "name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.action(description="Concluir atividades selecionadas (encerra agora)")
    def finish_selected(self, request, queryset):
        now = timezone.now()
        ActivitySession.objects.filter(activity__in=queryset, ended_at__isnull=True).update(ended_at=now)
        updated = queryset.filter(finished_at__isnull=True).update(is_active=False, finished_at=now)
        self.message_user(request, f"{updated} atividade(s) concluída(s).")

    @admin.action(description="Pausar atividades selecionadas (não conclui)")
    def pause_selected(self, request, queryset):
        updated = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(request, f"{updated} atividade(s) pausada(s).")

    @admin.display(description="Horas (dec)")
    def hours_decimal(self, obj):
        return f"{obj.total_active_seconds()/3600:.2f}"

    @admin.display(description="Horas (HH:MM:SS)")
    def hours_hms(self, obj):
        return _fmt_hms(obj.total_active_seconds())

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("sessions")
