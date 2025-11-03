# automation/forms.py
from django import forms
from .models import Activity, Milestone, GeneralActivity, SpecificActivity, Project
from common.models import Collaborator  # <- aqui é o ajuste

# -------------------- Widgets --------------------

class DataAttrSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        self.option_attrs_map = kwargs.pop("option_attrs_map", {}) or {}
        super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        key = "" if value is None else str(value)
        if key in self.option_attrs_map:
            option["attrs"].update(self.option_attrs_map[key])
        return option

# -------------------- ChoiceFields --------------------

class ProjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: Project) -> str:
        cc = (obj.cost_center or "").strip()
        return f"{cc} – {obj.name}" if cc else obj.name

class MilestoneChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: Milestone) -> str:
        return obj.name

class GeneralChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: GeneralActivity) -> str:
        return obj.name

class SpecificChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: SpecificActivity) -> str:
        return obj.name

# -------------------- Form principal --------------------

class ActivityForm(forms.ModelForm):
    project   = ProjectChoiceField(queryset=Project.objects.none(), required=False)
    milestone = MilestoneChoiceField(queryset=Milestone.objects.none(), required=False, widget=DataAttrSelect())
    general   = GeneralChoiceField(queryset=GeneralActivity.objects.none(), required=False, widget=DataAttrSelect())
    specific  = SpecificChoiceField(queryset=SpecificActivity.objects.none(), required=False, widget=DataAttrSelect())

    class Meta:
        model = Activity
        fields = [
            "project",
            "milestone", "general", "specific",
            "custom_milestone", "custom_general", "custom_specific",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ms_qs = Milestone.objects.filter(is_active=True).order_by("order", "name")
        ga_qs = (GeneralActivity.objects
                 .filter(is_active=True)
                 .select_related("milestone")
                 .order_by("milestone__order", "order", "name"))
        sp_qs = (SpecificActivity.objects
                 .filter(is_active=True)
                 .select_related("general", "general__milestone")
                 .order_by("general__milestone__order", "general__order", "order", "name"))

        self.fields["project"].queryset   = Project.objects.all().order_by("name")
        self.fields["milestone"].queryset = ms_qs
        self.fields["general"].queryset   = ga_qs
        self.fields["specific"].queryset  = sp_qs

        self.fields["project"].empty_label   = "Selecione…"
        self.fields["milestone"].empty_label = "Selecione o marco…"
        self.fields["general"].empty_label   = "Selecione a atividade geral…"
        self.fields["specific"].empty_label  = "Selecione a atividade específica…"

        base_select = "w-full appearance-none border border-slate-200 rounded-xl pl-9 pr-9 py-2"
        self.fields["project"].widget.attrs.setdefault("class", base_select)
        self.fields["milestone"].widget.attrs.setdefault("class", base_select + " js-select-milestone")
        self.fields["general"].widget.attrs.setdefault("class", base_select + " js-select-general")
        self.fields["specific"].widget.attrs.setdefault("class", base_select + " js-select-specific")

        text_input = "w-full border border-slate-200 rounded-xl px-3 py-2"
        self.fields["custom_milestone"].widget.attrs.setdefault("class", text_input + " js-adhoc-milestone")
        self.fields["custom_general"].widget.attrs.setdefault("class", text_input + " js-adhoc-general")
        self.fields["custom_specific"].widget.attrs.setdefault("class", text_input + " js-adhoc-specific")
        self.fields["description"].widget.attrs.setdefault("class", "w-full border border-slate-200 rounded-xl px-3 py-2 min-h-[90px]")

        gen_widget = self.fields["general"].widget
        if isinstance(gen_widget, DataAttrSelect):
            gen_widget.option_attrs_map = {str(g.id): {"data-milestone": str(g.milestone_id)} for g in ga_qs}

        spec_widget = self.fields["specific"].widget
        if isinstance(spec_widget, DataAttrSelect):
            spec_widget.option_attrs_map = {str(s.id): {"data-general": str(s.general_id)} for s in sp_qs}

# -------------------- Form de Configurações do Colaborador --------------------

class CollaboratorSettingsForm(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ["name", "email", "phone"]
