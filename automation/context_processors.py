# automation/context_processors.py
from django.apps import apps
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

def _get_collaborator(user):
    if not getattr(user, "is_authenticated", False):
        return None
    collab = getattr(user, "collaborator", None)
    if collab:
        return collab
    Collaborator = apps.get_model("common", "Collaborator")
    return Collaborator.objects.filter(user=user, is_active=True).only("id", "is_manager").first()

def user_flags(request):
    collab = _get_collaborator(request.user)
    return {"is_manager": bool(getattr(collab, "is_manager", False))}

def notifications(request):
    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", False):
        return {"notif_count": 0, "notif_list": []}

    collab = _get_collaborator(user)
    if not collab:
        return {"notif_count": 0, "notif_list": []}

    # <<< AQUI: se não existir common.Notice, não quebra
    try:
        Notice = apps.get_model("common", "Notice")
    except LookupError:
        return {"notif_count": 0, "notif_list": []}

    qs = (Notice.objects.current()
          .filter(Q(for_all=True) | Q(target=collab))
          .exclude(acks__collaborator=collab)
          .order_by("-created_at"))

    if not getattr(collab, "is_manager", False):
        qs = qs.filter(Q(only_managers=False) | Q(target=collab))

    notif_list = list(qs[:10])
    return {"notif_count": qs.count(), "notif_list": notif_list}
