from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import redirect
from django.db.models import Q


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "phonebook/register.html"
    success_url = reverse_lazy("create-user-contact")


class CreateUserContactForm(CreateView):
    model = Contact
    template_name = "phonebook/create_user_contact_form.html"
    success_url = "/admin/phonebook/contact/"
    form_class = CreateUserContactForm

    def dispatch(self, request, *args, **kwargs):
        try:
            Contact.objects.get(user=self.request.user)
            return redirect(reverse_lazy("homepage"))
        except:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            contact = form.save(commit=False)
            contact.user = self.request.user
            contact.first_name = self.request.user.first_name
            contact.last_name = self.request.user.last_name
            contact.save()
            return super().form_valid(form)
        except:
            raise Exception("You already have an existing record")


class PhonebookLoginView(LoginView):
    template_name = "phonebook/login.html"


class HomePageView(LoginRequiredMixin, ListView):
    login_url = "/admin"
    template_name = "phonebook/phonebook_homepage.html"

    model = Contact
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search_query")
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(company__icontains=search_query)
            )

        return queryset


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "phonebook/phonebook_detail.html"

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise Exception("Contact with this detail does not exists")
