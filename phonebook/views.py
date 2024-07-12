from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.base import Model as Model
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    TemplateView,
)
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import redirect
from django.db.models import Q
from .models import REGION_CHOICES


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
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search_query")
        region_filter_value = self.request.GET.get("region_filter")

        if search_query and region_filter_value != "None":
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(company__icontains=search_query),
                region=region_filter_value,
            )
        elif search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(company__icontains=search_query)
            )
        elif region_filter_value:
            queryset = queryset.filter(region=region_filter_value)

        return queryset.order_by("-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_contact_details"] = self.request.user.has_contact_details
        context["region_choices"] = dict(REGION_CHOICES)

        if self.request.GET.get("region_filter") != "None":
            context["region_choices_value"] = str(self.request.GET.get("region_filter"))

        # TODO FIX SEARCHING if self.request.GET.get("region_filter")

        return context
