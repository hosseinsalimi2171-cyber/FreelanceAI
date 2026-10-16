
from django.contrib import admin
from .models import Project, AIProvider


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price_usd",
        "delivery_days",
        "is_published",
        "created_at",
    )
    list_filter = ("category", "is_published")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)


@admin.register(AIProvider)
class AIProviderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "provider",
        "model_id",
        "role",
        "status",
        "is_enabled",
        "is_primary",
    )
    list_filter = ("provider", "role", "status", "is_enabled")
    search_fields = ("name", "provider", "model_id")
    list_editable = ("status", "is_enabled", "is_primary")

from .models import PrivateProjectRequest, ProjectOrder

@admin.register(PrivateProjectRequest)
class PrivateProjectRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "owner__username", "owner__email", "brief")
    readonly_fields = ("created_at", "updated_at")

@admin.register(ProjectOrder)
class ProjectOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "title_snapshot", "customer", "amount_usd", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title_snapshot", "customer__username", "customer__email")
    readonly_fields = ("created_at", "updated_at")
