from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("portfolio", "0002_aiprovider"),
    ]
    operations = [
        migrations.CreateModel(
            name="PrivateProjectRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("brief", models.TextField()),
                ("budget_usd", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("desired_delivery_days", models.PositiveIntegerField(blank=True, null=True)),
                ("status", models.CharField(choices=[("submitted", "Submitted"), ("reviewing", "Under review"), ("quoted", "Quote provided"), ("accepted", "Accepted"), ("in_progress", "In progress"), ("preview_ready", "Preview ready"), ("revision_requested", "Revision requested"), ("completed", "Completed"), ("cancelled", "Cancelled")], db_index=True, default="submitted", max_length=24)),
                ("staff_notes", models.TextField(blank=True, help_text="Internal notes; never shown to the customer.")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="private_project_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ProjectOrder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title_snapshot", models.CharField(max_length=200)),
                ("amount_usd", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("in_progress", "In progress"), ("preview_ready", "Preview ready"), ("revision_requested", "Revision requested"), ("awaiting_payment", "Awaiting payment"), ("paid", "Paid"), ("delivered", "Delivered"), ("cancelled", "Cancelled")], db_index=True, default="pending", max_length=24)),
                ("preview_file", models.FileField(blank=True, upload_to="order_previews/%Y/%m/")),
                ("final_file", models.FileField(blank=True, upload_to="order_deliveries/%Y/%m/")),
                ("customer_feedback", models.TextField(blank=True)),
                ("staff_notes", models.TextField(blank=True, help_text="Internal notes; never shown to the customer.")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="project_orders", to=settings.AUTH_USER_MODEL)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to="portfolio.project")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
