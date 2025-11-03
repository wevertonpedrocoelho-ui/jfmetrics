# epe/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# -------------------------------- Projeto ------------------------------------

class Project(models.Model):
    name = models.CharField("Nome do projeto", max_length=150)
    code = models.CharField("Código interno", max_length=40, blank=True)
    cost_center = models.CharField("Centro de custo", max_length=50, blank=True)
    location = models.CharField("Local", max_length=120, blank=True)
    is_active = models.BooleanField("Ativo", default=True, db_index=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        indexes = [
            models.Index(fields=["is_active", "name"]),
        ]

    def __str__(self) -> str:
        return self.name


# -------------------- Catálogos: Atividade Geral & Tamanho -------------------

class GeneralActivity(models.Model):
    name = models.CharField("Atividade Geral", max_length=120, unique=True)
    order = models.PositiveIntegerField("Ordem", default=0)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "Atividade Geral"
        verbose_name_plural = "Atividades Gerais"

    def __str__(self) -> str:
        return self.name


class PanelSize(models.Model):
    name = models.CharField("Tamanho do painel", max_length=50, unique=True)
    order = models.PositiveIntegerField("Ordem", default=0)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "Tamanho do painel"
        verbose_name_plural = "Tamanhos de painel"

    def __str__(self) -> str:
        return self.name


# ------------------------- Jornada e Atividades ------------------------------

class Workday(models.Model):
    # Usa o colaborador central
    collaborator = models.ForeignKey(
        "common.Collaborator",
        verbose_name="Colaborador",
        on_delete=models.PROTECT,
        related_name="epe_workdays",
        related_query_name="epe_workday",
    )
    date = models.DateField("Data", default=timezone.localdate)
    started_at = models.DateTimeField("Início", auto_now_add=True)
    ended_at = models.DateTimeField("Término", blank=True, null=True)
    is_open = models.BooleanField("Aberto?", default=True)

    class Meta:
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
    # Colaborador central
    collaborator = models.ForeignKey(
        "common.Collaborator",
        verbose_name="Colaborador",
        on_delete=models.PROTECT,
        related_name="epe_activities",
        related_query_name="epe_activity",
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

    # === Campos específicos cadastráveis ===
    panel_name = models.CharField("Nome do painel", max_length=120)
    general = models.ForeignKey(
        GeneralActivity,
        verbose_name="Atividade Geral",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    panel_size = models.ForeignKey(
        PanelSize,
        verbose_name="Tamanho do painel",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    # Observações gerais
    description = models.TextField("Descrição", blank=True)

    started_at = models.DateTimeField("Início", auto_now_add=True)
    finished_at = models.DateTimeField("Término", blank=True, null=True)
    is_active = models.BooleanField("Ativa?", default=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
        indexes = [
            models.Index(fields=["is_active", "started_at"]),
            models.Index(fields=["collaborator", "started_at"]),
            models.Index(fields=["general", "panel_size"]),
        ]

    def clean(self):
        super().clean()
        if not (self.panel_name or "").strip():
            raise ValidationError("Informe o Nome do painel.")
        if not self.general_id:
            raise ValidationError("Selecione a Atividade Geral.")
        if not self.panel_size_id:
            raise ValidationError("Selecione o Tamanho do painel.")

    # --- usados pelo dashboard/UI ---
    def total_active_seconds(self) -> int:
        """Soma o tempo de todas as sessões; conta até agora se não encerradas."""
        return sum((s.duration_seconds() or 0) for s in self.sessions.all())

    def __str__(self) -> str:
        return f"{self.collaborator} — {self.panel_name} ({self.panel_size})"


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
        verbose_name = "Sessão de atividade"
        verbose_name_plural = "Sessões de atividade"
        ordering = ("-started_at",)
        indexes = [
            models.Index(fields=["activity", "started_at"]),
            models.Index(fields=["ended_at"]),
        ]

    def stop(self):
        """Encerra a sessão, se ainda estiver aberta."""
        if self.ended_at is None:
            self.ended_at = timezone.now()
            self.save(update_fields=["ended_at"])

    def duration_seconds(self) -> int:
        """Duração em segundos; retornando 0 se started_at ainda não existe (inline vazio)."""
        if not self.started_at:
            return 0
        end = self.ended_at or timezone.now()
        return max(0, int((end - self.started_at).total_seconds()))

    def __str__(self) -> str:
        state = "aberta" if self.ended_at is None else "fechada"
        return f"Sessão #{self.pk} — {self.activity} ({state})"
