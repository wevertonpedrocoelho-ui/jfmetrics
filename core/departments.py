# core/departments.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from common.models import Collaborator

@dataclass(frozen=True)
class Dept:
    namespace: str
    slug: str
    label: str
    dashboard_urlname: str

DEPARTMENTS: List[Dept] = [
    Dept(
        namespace="engauto",  # <- bate com o namespace do include(...)
        slug="engauto",       # <- bate com Department.slug no banco
        label="Engenharia de Automação",
        dashboard_urlname="engauto:dashboard",
    ),
    Dept(
        namespace="epe",
        slug="epe",
        label="Engenharia de Painéis Elétricos",
        dashboard_urlname="epe:dashboard",
    ),

    Dept(
        namespace="engobras",           
        slug="engobras",                 
        label="Engenharia de Obras",     
        dashboard_urlname="engobras:dashboard", 
    ),

]

def get_memberships(user) -> List[dict]:
    if not user or not getattr(user, "is_authenticated", False):
        return []
    user_slugs = set(
        Collaborator.objects.filter(
            user=user, is_active=True, department__is_active=True
        ).values_list("department__slug", flat=True)
    )
    out = []
    for d in DEPARTMENTS:
        if d.slug in user_slugs:
            is_manager = Collaborator.objects.filter(
                user=user, is_active=True, department__slug=d.slug, is_manager=True
            ).exists()
            out.append({
                "namespace": d.namespace,
                "slug": d.slug,
                "label": d.label,
                "dashboard_urlname": d.dashboard_urlname,
                "is_manager": is_manager,
            })
    return out

def get_dept_by_namespace(ns: str) -> Optional[dict]:
    for d in DEPARTMENTS:
        if d.namespace == ns:
            return {
                "namespace": d.namespace,
                "slug": d.slug,
                "label": d.label,
                "dashboard_urlname": d.dashboard_urlname,
            }
    return None
