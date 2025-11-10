# engobras/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# =============================== Projetos ====================================

class Project(models.Model):
    name = models.CharField("Nome do projeto", max_length=150)
    code = models.CharField("Código interno", max_length=40, blank=True)
    cost_center = models.CharField("Centro de custo", max_length=50, blank=True)
    location = models.CharField("Local", max_length=120, blank=True)

    is_active = models.BooleanField("Ativo", default=True, db_index=True)

    class Meta:
        db_table = "engobras_project"
        ordering = ("name",)
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self) -> str:
        return self.name


# ================================ EAP ========================================

class Milestone(models.Model):
    name = models.CharField("Marco", max_length=80, unique=True)
    order = models.PositiveIntegerField("Ordem", default=0)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        db_table = "engobras_milestone"
        ordering = ("order", "name")
        verbose_name = "Marco"
        verbose_name_plural = "Marcos"

    def __str__(self) -> str:
        return self.name


class GeneralActivity(models.Model):
    milestone = models.ForeignKey(
        Milestone,
        verbose_name="Marco",
        on_delete=models.CASCADE,
        related_name="engobras_generals",
    )
    name = models.CharField("Atividade Geral", max_length=80)
    order = models.PositiveIntegerField("Ordem", default=0)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        db_table = "engobras_general_activity"
        unique_together = ("milestone", "name")
        ordering = ("milestone__order", "order", "name")
        verbose_name = "Atividade Geral"
        verbose_name_plural = "Atividades Gerais"

    def __str__(self) -> str:
        return f"{self.milestone} › {self.name}"


class SpecificActivity(models.Model):
    general = models.ForeignKey(
        GeneralActivity,
        verbose_name="Atividade Geral",
        on_delete=models.CASCADE,
        related_name="engobras_specifics",
    )
    name = models.CharField("Atividade Específica", max_length=120)
    order = models.PositiveIntegerField("Ordem", default=0)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        db_table = "engobras_specific_activity"
        unique_together = ("general", "name")
        ordering = ("general__milestone__order", "general__order", "order", "name")
        verbose_name = "Atividade Específica"
        verbose_name_plural = "Atividades Específicas"

    def __str__(self) -> str:
        return f"{self.general.milestone} › {self.general.name} › {self.name}"


# ========================== Jornada e Atividades =============================

class Workday(models.Model):
    collaborator = models.ForeignKey(
        "common.Collaborator",
        verbose_name="Colaborador",
        on_delete=models.PROTECT,
        related_name="engobras_workdays",
        related_query_name="engobras_workday",
    )
    date = models.DateField("Data", default=timezone.localdate)
    started_at = models.DateTimeField("Início", auto_now_add=True)
    ended_at = models.DateTimeField("Término", blank=True, null=True)
    is_open = models.BooleanField("Aberto?", default=True)

    class Meta:
        db_table = "engobras_workday"
        unique_together = ("collaborator", "date")
        ordering = ("-date", "collaborator__name")
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"

    def __str__(self) -> str:
        status = "aberto" if self.is_open else "fechado"
        return f"{self.collaborator} — {self.date} ({status})"

    def close(self):
        self.ended_at = timezone.now()
        self.is_open = False
        self.save(update_fields=["ended_at", "is_open"])


class Activity(models.Model):
    collaborator = models.ForeignKey(
        "common.Collaborator",
        verbose_name="Colaborador",
        on_delete=models.PROTECT,
        related_name="engobras_activities",
        related_query_name="engobras_activity",
    )
    workday = models.ForeignKey(
        Workday,
        verbose_name="Expediente",
        on_delete=models.CASCADE,
        related_name="activities",
    )

    # Projeto (opcional)
    project = models.ForeignKey(
        Project,
        verbose_name="Projeto",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # EAP (opcional)
    milestone = models.ForeignKey(
        Milestone,
        verbose_name="Marco",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    general = models.ForeignKey(
        GeneralActivity,
        verbose_name="Atividade Geral",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    specific = models.ForeignKey(
        SpecificActivity,
        verbose_name="Atividade Específica",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # Alternativa ad-hoc
    custom_milestone = models.CharField("Marco (ad-hoc)", max_length=80, blank=True)
    custom_general = models.CharField("Atividade Geral (ad-hoc)", max_length=80, blank=True)
    custom_specific = models.CharField("Atividade Específica (ad-hoc)", max_length=120, blank=True)

    description = models.TextField("Descrição", blank=True)

    started_at = models.DateTimeField("Início", auto_now_add=True)
    finished_at = models.DateTimeField("Término", blank=True, null=True)
    is_active = models.BooleanField("Ativa?", default=True)

    class Meta:
        db_table = "engobras_activity"
        ordering = ("-id",)
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

    # --- validações ---
    def clean(self):
        super().clean()
        eap_informada = any([self.milestone_id, self.general_id, self.specific_id])
        ad_hoc = any([self.custom_milestone, self.custom_general, self.custom_specific])
        if not eap_informada and not ad_hoc:
            raise ValidationError("Informe a EAP (Marco/Geral/Específica) ou descreva via campos ad-hoc.")
        if self.specific and self.general and self.specific.general_id != self.general.id:
            raise ValidationError("A Específica escolhida não pertence à Atividade Geral selecionada.")
        if self.general and self.milestone and self.general.milestone_id != self.milestone.id:
            raise ValidationError("A Atividade Geral escolhida não pertence ao Marco selecionado.")

    # --- helpers UI ---
    def total_active_seconds(self) -> int:
        return sum(s.duration_seconds() for s in self.sessions.all())

    def eap_display(self) -> str:
        if self.specific:
            return f"{self.milestone} › {self.general} › {self.specific.name}"
        if self.general:
            return f"{self.milestone} › {self.general.name}"
        if self.milestone:
            return f"{self.milestone.name}"
        parts = [p for p in [self.custom_milestone, self.custom_general, self.custom_specific] if p]
        return " / ".join(parts) or "—"

    def __str__(self) -> str:
        return f"{self.collaborator} — {self.eap_display()}"


class ActivitySession(models.Model):
    activity = models.ForeignKey(
        Activity,
        verbose_name="Atividade",
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    started_at = models.DateTimeField("Início", auto_now_add=True)
    ended_at = models.DateTimeField("Término", blank=True, null=True)

    class Meta:
        db_table = "engobras_activity_session"
        verbose_name = "Sessão de atividade"
        verbose_name_plural = "Sessões de atividade"

    def stop(self):
        if self.ended_at is None:
            self.ended_at = timezone.now()
            self.save(update_fields=["ended_at"])

    def duration_seconds(self) -> int:
        end = self.ended_at or timezone.now()
        return max(0, int((end - self.started_at).total_seconds()))

    def __str__(self) -> str:
        state = "aberta" if self.ended_at is None else "fechada"
        return f"Sessão #{self.pk} — {self.activity} ({state})"
