# core/middleware.py
from django.http import HttpResponseForbidden
from django.utils.functional import cached_property
from common.models import Collaborator
from core.departments import DEPARTMENTS, get_dept_by_namespace  # get_memberships não é mais necessário

# Mapeia namespace (urls) -> slug (Department no common)
NS_TO_SLUG = {d.namespace: d.slug for d in DEPARTMENTS}
DEPT_NAMESPACES = set(NS_TO_SLUG.keys())


class DepartmentAccessMiddleware:
    """
    Para rotas com namespace de departamento (ex.: 'automation', 'epe'):
      - Garante que o usuário pertence ao depto (via common.Collaborator).
      - Injeta:
          request.dept_ns        -> namespace da rota
          request.dept           -> dict do depto (namespace, slug, label, dashboard_urlname)
          request.collaborator   -> common.Collaborator do usuário no depto
          request.is_manager     -> bool
      - Persiste 'last_dept_ns' na sessão ao acessar uma rota do depto.
    Coloque depois de AuthenticationMiddleware no settings.MIDDLEWARE.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        rm = getattr(request, "resolver_match", None)
        ns = getattr(rm, "namespace", None)

        # defaults
        request.dept_ns = ns
        request.dept = None
        request.collaborator = None
        request.is_manager = False

        # Se a rota não tem namespace de depto, não faz nada
        if not ns or ns not in DEPT_NAMESPACES:
            return None

        # Precisa estar autenticado (as views já usam @login_required normalmente)
        if not request.user.is_authenticated:
            return None

        # Descobre o slug do depto a partir do namespace da rota
        dept_slug = NS_TO_SLUG.get(ns)
        if not dept_slug:
            return HttpResponseForbidden("Departamento desconhecido.")

        # Busca o colaborador central do usuário para este departamento
        collab = (
            Collaborator.objects
            .select_related("department", "user")
            .filter(user=request.user, is_active=True, department__slug=dept_slug, department__is_active=True)
            .first()
        )
        if not collab:
            return HttpResponseForbidden("Você não tem acesso a este departamento.")

        # Metadados do depto (usa helper para montar o dict)
        dept_info = get_dept_by_namespace(ns)
        request.dept = dept_info
        request.collaborator = collab
        request.is_manager = bool(collab.is_manager)

        # Persiste para o after_login redirecionar ao último depto acessado
        request.session["last_dept_ns"] = ns

        return None
