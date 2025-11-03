# common/utils.py
from .models import Collaborator, Department

def ensure_collaborator_for_user(user, department_slug: str) -> Collaborator | None:
    """
    Garante que o user tenha Collaborator no depto indicado, sem inventar e-mail.
    Se já existir collaborator para o user: atualiza department (se quiser travar, remova isso).
    Senão cria, reciclando o e-mail se não conflitar.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return None

    dept = Department.objects.filter(slug=department_slug).first()
    if not dept:
        dept = Department.objects.create(slug=department_slug, name=department_slug.upper())

    collab = getattr(user, "collaborator", None)
    if collab:
        # opcional: manter dept atual; ou atualizar se estiver diferente
        if collab.department_id != dept.id:
            collab.department = dept
            collab.save(update_fields=["department"])
        return collab

    # criar novo
    name  = (getattr(user, "get_full_name", None)() or user.first_name or user.username or "Colaborador").strip() or "Colaborador"
    email = (user.email or "").strip().lower() or None

    # se email conflita com outro collaborator, zera
    if email and Collaborator.objects.exclude(user=user).filter(email=email).exists():
        email = None

    return Collaborator.objects.create(user=user, name=name, email=email, department=dept, is_active=True)
