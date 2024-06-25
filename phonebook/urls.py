"""
URL configuration for phonebook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("phonebook", views.HomePageView.as_view(), name="homepage"),
    path("login", views.PhonebookLoginView.as_view(), name="login"),
    path("register", views.SignupView.as_view(), name="register"),
    path(
        "contact/user/new",
        views.CreateUserContactForm.as_view(),
        name="create-user-contact",
    ),
    path(
        "phonebook/<int:pk>", views.ContactDetailView.as_view(), name="phonebook-detail"
    ),
    path(
        "phonebook/<int:pk>/update",
        views.UpdateContactView.as_view(),
        name="update-contact",
    ),
]
