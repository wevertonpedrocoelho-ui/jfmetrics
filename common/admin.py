from django.contrib import admin
from .models import Department, Collaborator

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display  = ("name", "email", "department", "is_active", "is_manager", "user")
    list_filter   = ("department", "is_active", "is_manager")
    search_fields = ("name", "email", "phone", "user__username")
    autocomplete_fields = ("user",)
    list_select_related = ("department", "user")
