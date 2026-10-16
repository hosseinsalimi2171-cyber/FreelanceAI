from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("web", "Web Development"), ("wordpress", "WordPress"),
        ("django", "Django"), ("ai", "Artificial Intelligence"),
        ("rag", "RAG Systems"), ("data", "Data Analysis"),
        ("automation", "Workflow Automation"), ("mcp", "MCP Tools"),
        ("llmops", "LLMOps"), ("support", "AI Support Agents"), ("other", "Other"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="web", db_index=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days = models.PositiveIntegerField(default=7)
    technologies = models.CharField(max_length=500, blank=True)
    image_url = models.URLField(max_length=1000, blank=True)
    is_published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            candidate, counter = base_slug, 2
            while Project.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate, counter = f"{base_slug}-{counter}", counter + 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AIProvider(models.Model):
    STATUS_CHOICES = [("planned", "Planned"), ("configured", "Configured"), ("tested", "Tested"), ("error", "Error")]
    ROLE_CHOICES = [("orchestrator", "Orchestration"), ("coding", "Coding"), ("research", "Research"), ("review", "Quality Review"), ("multimodal", "Multimodal"), ("general", "General Purpose")]
    name = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=100)
    model_id = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="general")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    is_enabled = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    fallback_model = models.CharField(max_length=200, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["provider", "name"]
        verbose_name = "AI Provider"
        verbose_name_plural = "AI Providers"

    def __str__(self):
        return f"{self.provider} — {self.name}"


class PrivateProjectRequest(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"), ("reviewing", "Under review"),
        ("quoted", "Quote provided"), ("accepted", "Accepted"),
        ("in_progress", "In progress"), ("preview_ready", "Preview ready"),
        ("revision_requested", "Revision requested"), ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="private_project_requests")
    title = models.CharField(max_length=200)
    brief = models.TextField()
    budget_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desired_delivery_days = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default="submitted", db_index=True)
    staff_notes = models.TextField(blank=True, help_text="Internal notes; never shown to the customer.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Request #{self.pk}: {self.title} ({self.owner})"


class ProjectOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"), ("in_progress", "In progress"),
        ("preview_ready", "Preview ready"), ("revision_requested", "Revision requested"),
        ("awaiting_payment", "Awaiting payment"), ("paid", "Paid"),
        ("delivered", "Delivered"), ("cancelled", "Cancelled"),
    ]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_orders")
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="orders")
    title_snapshot = models.CharField(max_length=200)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default="pending", db_index=True)
    preview_file = models.FileField(upload_to="order_previews/%Y/%m/", blank=True)
    final_file = models.FileField(upload_to="order_deliveries/%Y/%m/", blank=True)
    customer_feedback = models.TextField(blank=True)
    staff_notes = models.TextField(blank=True, help_text="Internal notes; never shown to the customer.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}: {self.title_snapshot}"
