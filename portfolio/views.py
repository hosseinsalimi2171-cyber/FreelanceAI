from pathlib import Path

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import RegistrationForm, PrivateProjectRequestForm
from .models import PrivateProjectRequest, Project, ProjectOrder


def home(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, "portfolio/home.html", {"projects_from_db": projects[:10]})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "portfolio/auth_form.html", {
        "form": form,
        "page_title": "Create your account",
        "submit_label": "Create account",
    })


@login_required
def dashboard(request):
    orders = ProjectOrder.objects.filter(customer=request.user).select_related("project")
    private_requests = PrivateProjectRequest.objects.filter(owner=request.user)
    return render(request, "portfolio/dashboard.html", {
        "orders": orders,
        "private_requests": private_requests,
    })


@login_required
@require_POST
def create_order(request, project_id):
    project = get_object_or_404(Project, pk=project_id, is_published=True)
    order = ProjectOrder.objects.create(
        customer=request.user,
        project=project,
        title_snapshot=project.title,
        amount_usd=project.price_usd,
    )
    messages.success(
        request,
        f"Order #{order.pk} has been created. Payment is not yet requested or verified.",
    )
    return redirect("dashboard")


@login_required
def create_private_request(request):
    form = PrivateProjectRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.save()
        messages.success(request, "Your private project request has been submitted.")
        return redirect("dashboard")
    return render(request, "portfolio/auth_form.html", {
        "form": form,
        "page_title": "Submit a private project request",
        "submit_label": "Submit request",
    })


@login_required
def private_request_detail(request, request_id):
    item = get_object_or_404(PrivateProjectRequest, pk=request_id)
    if item.owner_id != request.user.id and not request.user.is_staff:
        raise Http404
    return render(request, "portfolio/private_request_detail.html", {"item": item})


def _authorized_order(request, order_id):
    order = get_object_or_404(ProjectOrder, pk=order_id)
    if order.customer_id != request.user.id and not request.user.is_staff:
        raise Http404
    return order


@login_required
def download_order_preview(request, order_id):
    order = _authorized_order(request, order_id)
    if not order.preview_file or order.status not in {"preview_ready", "revision_requested"}:
        raise Http404
    try:
        handle = order.preview_file.open("rb")
    except (FileNotFoundError, OSError, SuspiciousFileOperation, ValueError):
        raise Http404
    filename = Path(order.preview_file.name).name or f"order-{order.pk}-preview"
    return FileResponse(handle, as_attachment=True, filename=filename)


@login_required
def download_order_final(request, order_id):
    # Final downloads remain blocked until real payment verification exists.
    _authorized_order(request, order_id)
    raise Http404
