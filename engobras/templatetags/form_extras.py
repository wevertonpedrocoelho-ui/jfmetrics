from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(bound_field, css_classes: str):
    """
    Usa: {{ form.campo|add_class:"w-full ..." }}
    Mantém classes existentes do widget e acrescenta as novas.
    """
    if not hasattr(bound_field, "as_widget"):
        return bound_field
    existing = bound_field.field.widget.attrs.get("class", "")
    attrs = dict(bound_field.field.widget.attrs)
    attrs["class"] = (existing + " " + css_classes).strip() if existing else css_classes
    return bound_field.as_widget(attrs=attrs)

@register.filter(name="attr")
def add_attr(bound_field, arg: str):
    """
    Define um atributo qualquer no widget.
    Usa: {{ form.campo|attr:"placeholder:Digite aqui" }}
    """
    if not hasattr(bound_field, "as_widget"):
        return bound_field
    try:
        key, val = arg.split(":", 1)
    except ValueError:
        return bound_field
    attrs = dict(bound_field.field.widget.attrs)
    attrs[key] = val
    return bound_field.as_widget(attrs=attrs)
