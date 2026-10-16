from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from portfolio import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="portfolio/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("requests/new/", views.create_private_request, name="create_private_request"),
    path("requests/<int:request_id>/", views.private_request_detail, name="private_request_detail"),
    path("projects/<int:project_id>/order/", views.create_order, name="create_order"),
    path("orders/<int:order_id>/preview/", views.download_order_preview, name="download_order_preview"),
    path("orders/<int:order_id>/final/", views.download_order_final, name="download_order_final"),
]
