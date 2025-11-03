# jfmetrics/views.py
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from core.departments import get_memberships, get_dept_by_namespace

@login_required
def after_login(request):
    memberships = get_memberships(request.user)

    if not memberships:
        messages.error(request, "Seu usuário não está vinculado a nenhum departamento ativo.")
        return redirect("logout")  # ou para uma página explicativa

    # tenta usar o último depto escolhido (se existir e ainda válido)
    last_ns = request.session.get("last_dept_ns")
    for d in memberships:
        if d["namespace"] == last_ns:
            return redirect(d["dashboard_urlname"])

    # se só tem um, manda nele
    if len(memberships) == 1:
        d = memberships[0]
        request.session["last_dept_ns"] = d["namespace"]
        return redirect(d["dashboard_urlname"])

    # se tem mais de um, mostre uma telinha simples de escolha
    return render(request, "choose_department.html", {"memberships": memberships})


@login_required
def choose_department_submit(request):
    if request.method != "POST":
        return redirect("after_login")
    ns = request.POST.get("namespace")
    d = get_dept_by_namespace(ns)
    if not d:
        return redirect("after_login")
    # (opcional) validar que o user realmente pertence a esse depto:
    if d["namespace"] not in [m["namespace"] for m in get_memberships(request.user)]:
        return redirect("after_login")

    request.session["last_dept_ns"] = d["namespace"]
    return redirect(d["dashboard_urlname"])
