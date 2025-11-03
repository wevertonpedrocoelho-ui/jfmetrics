# common/models.py
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(models.Model):
    slug = models.SlugField("Slug", unique=True) 
    name = models.CharField("Nome", max_length=120)
    is_active = models.BooleanField("Ativo", default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Collaborator(models.Model):
    # Identidade
    user  = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="collaborator", verbose_name="Usuário do sistema"
    )
    name  = models.CharField("Nome", max_length=120)
    email = models.EmailField("E-mail", blank=True, null=True)  # <- opcional

    phone = models.CharField("Telefone", max_length=30, blank=True)
    photo = models.ImageField("Foto", upload_to="collaborators/", blank=True, null=True)

    # Organização
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="Departamento")
    is_manager = models.BooleanField("Gestor do departamento?", default=False)
    is_active  = models.BooleanField("Ativo", default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        constraints = [
            # e-mail único APENAS quando não nulo
            models.UniqueConstraint(
                fields=["email"],
                condition=Q(email__isnull=False),
                name="uq_common_collaborator_email_not_null",
            ),
        ]
        indexes = [
            models.Index(fields=["department", "is_active"]),
            models.Index(fields=["is_manager"]),
        ]

    def __str__(self):
        return f"{self.name} — {self.department}"
