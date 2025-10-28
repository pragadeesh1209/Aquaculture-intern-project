from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="user_login"),
    path("signup/", views.user_signup, name="user_signup"),
    path('suggestions/', views.user_suggestion_page, name='user_suggestion_page'),
    path("vendor/signup/", views.vendor_signup, name="vendor_signup"),
    path("vendor/login/", views.vendor_login, name="vendor_login"),
    path("vendor/dashboard/", views.vendor_dashboard, name="vendor_dashboard"),

]

