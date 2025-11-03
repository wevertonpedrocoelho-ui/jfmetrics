from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def ns_url(context, viewname, *args, **kwargs):
    """
    Resolve 'viewname' no namespace da rota atual (fallback: 'epe').
    Uso: {% ns_url 'activity_pause' a.id %}
    """
    req = context.get("request")
    ns = getattr(getattr(req, "resolver_match", None), "namespace", None) or "epe"
    return reverse(f"{ns}:{viewname}", args=args, kwargs=kwargs)
