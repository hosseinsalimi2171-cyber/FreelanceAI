from decimal import Decimal
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse

from portfolio.models import Project, ProjectOrder

User = get_user_model()


class SecureDownloadTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="secure-customer",
            password="StrongTestPass123!",
        )
        self.other_customer = User.objects.create_user(
            username="other-customer",
            password="StrongTestPass123!",
        )
        self.staff = User.objects.create_user(
            username="secure-staff",
            password="StrongTestPass123!",
            is_staff=True,
        )
        self.project = Project.objects.create(
            title="Secure Download Test Project",
            category="web",
            short_description="Test project",
            description="Security test",
            price_usd=Decimal("75.00"),
            is_published=True,
        )
        self.order = ProjectOrder.objects.create(
            customer=self.customer,
            project=self.project,
            title_snapshot=self.project.title,
            amount_usd=Decimal("75.00"),
            status="preview_ready",
        )

    def test_anonymous_user_cannot_download_preview(self):
        response = self.client.get(
            reverse("download_order_preview", args=[self.order.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_other_customer_cannot_download_preview(self):
        self.order.preview_file.save(
            "preview.txt", ContentFile(b"private preview"), save=True
        )
        self.client.force_login(self.other_customer)
        response = self.client.get(
            reverse("download_order_preview", args=[self.order.pk])
        )
        self.assertEqual(response.status_code, 404)

    @override_settings(MEDIA_ROOT=TemporaryDirectory().name)
    def test_owner_can_download_ready_preview(self):
        self.order.preview_file.save(
            "preview.txt", ContentFile(b"preview content"), save=True
        )
        self.client.force_login(self.customer)
        response = self.client.get(
            reverse("download_order_preview", args=[self.order.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"preview content")

    def test_final_download_is_blocked_even_if_status_says_paid(self):
        self.order.final_file.save(
            "final.txt", ContentFile(b"secret final"), save=True
        )
        self.order.status = "paid"
        self.order.save()
        self.client.force_login(self.customer)
        response = self.client.get(
            reverse("download_order_final", args=[self.order.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_staff_can_download_ready_preview(self):
        self.order.preview_file.save(
            "preview.txt", ContentFile(b"staff preview"), save=True
        )
        self.client.force_login(self.staff)
        response = self.client.get(
            reverse("download_order_preview", args=[self.order.pk])
        )
        self.assertEqual(response.status_code, 200)
