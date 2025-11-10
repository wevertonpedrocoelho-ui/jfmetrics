# core/context_processors.py
from typing import Optional

# map por namespace (preferencial)
NS_TO_BASE = {
    "automation": "automation/base.html",
    "engauto":    "automation/base.html",   # legado
    "epe":        "epe/base.html",
    "engobras":   "engobras/base.html", 
}

SLUG_TO_BASE = {
    "automation": "automation/base.html",
    "epe":        "epe/base.html",
    "engobras":   "engobras/base.html",  
}

def department_context(request):
    ns: str = getattr(request, "dept_ns", "") or ""
    dept: Optional[dict] = getattr(request, "dept", None)  # dict preenchido no middleware
    collab = getattr(request, "collaborator", None)
    is_manager = bool(getattr(request, "is_manager", False))

    # tenta por namespace; se não achar, tenta por slug; senão base.html
    base_template = NS_TO_BASE.get(ns)
    if not base_template and isinstance(dept, dict):
        base_template = SLUG_TO_BASE.get(dept.get("slug"))
    if not base_template:
        base_template = "base.html"

    return {
        "namespace": ns,
        "dept": dept,                              # ex.: {"namespace": "epe", "slug": "epe", "label": "...", ...}
        "dept_slug": (dept or {}).get("slug") if isinstance(dept, dict) else None,
        "department_label": (dept or {}).get("label") if isinstance(dept, dict) else None,
        "is_manager": is_manager,
        "current_collaborator": collab,
        "base_template": base_template,
    }
