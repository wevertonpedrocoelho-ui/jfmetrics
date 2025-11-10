# engobras/utils.py
from uuid import uuid4
from django.utils.text import slugify
from common.models import Collaborator

def ensure_collaborator_for_user(user):
    """
    Garante que o usuário tenha um Collaborator vinculado,
    sem usar o e-mail real para formar o placeholder.
    Só usa o e-mail real para localizar/ligar registro existente.
    """
    if not user or not user.is_authenticated:
        return None

    collab = Collaborator.objects.filter(user=user).first()
    if collab:
        return collab

    # Se já existe colaborador com o e-mail real, apenas vincula
    email = (user.email or "").strip().lower()
    if email:
        existing = Collaborator.objects.filter(email=email).first()
        if existing and existing.user_id is None:
            existing.user = user
            existing.save(update_fields=["user"])
            return existing

    # Cria um placeholder neutro (sem dados reais)
    # Exemplo: collab-u6-9f2b1a2c@local.invalid
    uniq = uuid4().hex[:8]
    unique_email = f"collab-u{user.id}-{uniq}@local.invalid"

    # Nome genérico mas legível
    name = getattr(user, "get_full_name", None)() or user.first_name or user.username or "Colaborador"
    name = (name or "Colaborador").strip() or "Colaborador"

    return Collaborator.objects.create(user=user, name=name, email=unique_email)
