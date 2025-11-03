# epe/utils.py
from uuid import uuid4
from .models import Collaborator

def ensure_collaborator_for_user(user):
    """
    Vincula/Cria Collaborator do EPE sem montar placeholder a partir do e-mail real.
    Usa o e-mail real apenas para localizar e vincular um existente.
    """
    if not user or not user.is_authenticated:
        return None

    collab = Collaborator.objects.filter(user=user).first()
    if collab:
        return collab

    email = (user.email or "").strip().lower()
    if email:
        existing = Collaborator.objects.filter(email=email).first()
        if existing and existing.user_id is None:
            existing.user = user
            existing.save(update_fields=["user"])
            return existing

    unique_email = f"collab-epe-u{user.id}-{uuid4().hex[:8]}@local.invalid"
    name = (getattr(user, "get_full_name", None)() or user.first_name or user.username or "Colaborador").strip() or "Colaborador"
    return Collaborator.objects.create(user=user, name=name, email=unique_email)
