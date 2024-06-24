from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        unique=True,
    )
    first_name = models.CharField(
        max_length=20,
        verbose_name="First Name",
    )
    last_name = models.CharField(
        max_length=20,
        verbose_name="Last Name",
    )
    company = models.CharField(
        max_length=50,
        verbose_name="Company",
    )
    telephone_number = PhoneNumberField(
        region="PH",
        verbose_name="Telephone Number",
    )
    mobile_phone_number = PhoneNumberField(
        region="PH",
        verbose_name="Mobile Phone Number",
    )
