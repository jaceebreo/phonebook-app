from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.base import Model as Model
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    TemplateView,
    View,
)
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import redirect
from django.db.models import Q
from .models import REGION_CHOICES
import openpyxl
from django.http import HttpResponse, JsonResponse
from io import BytesIO
import json


class ExportView(View):
    def post(self, request, *args, **kwargs):
        # Read the data from the request
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data format"}, status=400)

        # Create a workbook and select the active worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Add headers
        headers = ["ID", "Name", "Company", "Region", "Telephone", "Mobile"]
        sheet.append(headers)

        # Append data to the worksheet
        for row in data:
            sheet.append(row)

        # Save the workbook to an in-memory stream
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        # Set the response content type and headers
        response = HttpResponse(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=data.xlsx"

        return response


class AboutView(TemplateView):
    template_name = "phonebook/about.html"


class DeleteContactView(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy("homepage")


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "phonebook/phonebook_detail.html"

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise Exception("Contact with this detail does not exists")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region_choices"] = dict(REGION_CHOICES)
        return context


class UpdateContactView(LoginRequiredMixin, UpdateView):

    model = Contact
    form_class = UpdateContactForm
    template_name = "phonebook/update_contact.html"

    def get_success_url(self):
        contact = self.object
        return reverse_lazy("detail-contact", kwargs={"pk": contact.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region_choices"] = dict(REGION_CHOICES)
        return context


class CreateContactView(CreateView):
    model = Contact
    template_name = "phonebook/create_user_contact_form.html"
    success_url = reverse_lazy("homepage")
    form_class = CreateContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region_choices"] = dict(REGION_CHOICES)
        return context


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "phonebook/register.html"
    success_url = reverse_lazy("login")


class CreateUserContactView(LoginRequiredMixin, CreateView):
    template_name = "phonebook/create_user_contact_form.html"
    success_url = reverse_lazy("homepage")
    form_class = CreateUserContactForm

    def dispatch(self, request, *args, **kwargs):
        if Contact.objects.filter(user=self.request.user.id).first():
            return redirect(reverse_lazy("homepage"))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            contact = form.save(commit=False)
            contact.user = self.request.user
            contact.first_name = self.request.user.first_name
            contact.last_name = self.request.user.last_name
            contact.save()

            user = get_user_model().objects.get(pk=self.request.user.pk)
            user.has_contact_details = True
            user.save()
            return super().form_valid(form)
        except:
            raise Exception("You already have an existing record")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["region_choices"] = dict(REGION_CHOICES)
        return context


class PhonebookLoginView(LoginView):
    template_name = "phonebook/login.html"
    redirect_authenticated_user = reverse_lazy("create-user-contact")


class PhonebookLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class HomePageView(LoginRequiredMixin, ListView):
    login_url = "/login"
    template_name = "phonebook/phonebook_homepage.html"

    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_contact_details"] = self.request.user.has_contact_details
        context["region_choices"] = dict(REGION_CHOICES)
        context["fullname"] = (
            f"{self.request.user.first_name} {self.request.user.last_name}"
        )
        if self.request.GET.get("region_filter") != "None":
            context["region_choices_value"] = str(self.request.GET.get("region_filter"))

        # TODO FIX SEARCHING if self.request.GET.get("region_filter")

        return context
