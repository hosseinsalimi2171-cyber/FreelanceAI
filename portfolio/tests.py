from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import PrivateProjectRequest, Project, ProjectOrder

User = get_user_model()


class AccountAndOrderTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer-one", email="one@example.com", password="StrongTestPass123!"
        )
        self.other_customer = User.objects.create_user(
            username="customer-two", email="two@example.com", password="StrongTestPass123!"
        )
        self.project = Project.objects.create(
            title="Starter Website",
            category="web",
            short_description="A starter website project",
            description="A test project description",
            price_usd=Decimal("75.00"),
            delivery_days=5,
            is_published=True,
        )

    def test_registration_creates_account_and_logs_user_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new-customer",
                "email": "new@example.com",
                "password1": "AnotherStrongPass123!",
                "password2": "AnotherStrongPass123!",
            },
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(username="new-customer").exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="new-customer").pk)

    def test_private_request_is_visible_only_to_owner_or_staff(self):
        item = PrivateProjectRequest.objects.create(
            owner=self.customer, title="Private build", brief="Confidential customer details"
        )
        self.client.force_login(self.other_customer)
        response = self.client.get(reverse("private_request_detail", args=[item.pk]))
        self.assertEqual(response.status_code, 404)
        self.client.force_login(self.customer)
        response = self.client.get(reverse("private_request_detail", args=[item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confidential customer details")

    def test_customer_dashboard_does_not_show_other_customers_orders(self):
        own_order = ProjectOrder.objects.create(
            customer=self.customer, project=self.project,
            title_snapshot=self.project.title, amount_usd=self.project.price_usd,
        )
        other_order = ProjectOrder.objects.create(
            customer=self.other_customer, project=self.project,
            title_snapshot="Someone else's order", amount_usd=self.project.price_usd,
        )
        self.client.force_login(self.customer)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"#{own_order.pk}")
        self.assertNotContains(response, "Someone else's order")
        self.assertNotContains(response, "Someone else's order")

    def test_order_creation_requires_login(self):
        response = self.client.post(reverse("create_order", args=[self.project.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_order', args=[self.project.pk])}")
        self.assertEqual(ProjectOrder.objects.count(), 0)

    def test_customer_can_order_published_project(self):
        self.client.force_login(self.customer)
        response = self.client.post(reverse("create_order", args=[self.project.pk]))
        self.assertRedirects(response, reverse("dashboard"))
        order = ProjectOrder.objects.get(customer=self.customer)
        self.assertEqual(order.amount_usd, Decimal("75.00"))
        self.assertEqual(order.status, "pending")

    def test_customer_cannot_order_unpublished_project(self):
        self.project.is_published = False
        self.project.save()
        self.client.force_login(self.customer)
        response = self.client.post(reverse("create_order", args=[self.project.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(ProjectOrder.objects.count(), 0)

    def test_logout_requires_post(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)
