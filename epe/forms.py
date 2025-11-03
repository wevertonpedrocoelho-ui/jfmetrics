# epe/forms.py
from django import forms
from .models import Activity, Project, GeneralActivity, PanelSize
from common.models import Collaborator

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ("project", "panel_name", "general", "panel_size", "description")
        widgets = {
            "project": forms.Select(attrs={
                "id": "id_project",
                "class": "w-full rounded-xl border border-slate-200 bg-white py-2 pl-9 pr-8 text-sm outline-none focus:border-brand/40 focus:ring-2 focus:ring-brand/30"
            }),
            "general": forms.Select(attrs={
                "id": "id_general",
                "class": "w-full rounded-xl border border-slate-200 bg-white py-2 pl-9 pr-8 text-sm outline-none focus:border-brand/40 focus:ring-2 focus:ring-brand/30"
            }),
            "panel_size": forms.Select(attrs={
                "id": "id_panel_size",
                "class": "w-full rounded-xl border border-slate-200 bg-white py-2 pl-9 pr-8 text-sm outline-none focus:border-brand/40 focus:ring-2 focus:ring-brand/30"
            }),
            "panel_name": forms.TextInput(attrs={
                "id": "id_panel_name",
                "placeholder": "Ex.: QGBT-01",
                "class": "w-full rounded-xl border border-slate-200 bg-white py-2 pl-9 pr-3 text-sm outline-none focus:border-brand/40 focus:ring-2 focus:ring-brand/30"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-brand/40 focus:ring-2 focus:ring-brand/30"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante que sempre há opções válidas nos selects
        self.fields["project"].required = False
        self.fields["project"].queryset    = Project.objects.filter(is_active=True).order_by("name")
        self.fields["general"].queryset    = GeneralActivity.objects.filter(is_active=True).order_by("order", "name")
        self.fields["panel_size"].queryset = PanelSize.objects.filter(is_active=True).order_by("order", "name")


# Opcional: caso ainda não tenha um form simples de perfil no EPE
class CollaboratorSettingsForm(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ("name", "email", "phone")
        widgets = {
            "name":  forms.TextInput(attrs={"class": "w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"}),
            "email": forms.EmailInput(attrs={"class": "w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"}),
            "phone": forms.TextInput(attrs={"class": "w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"}),
        }
