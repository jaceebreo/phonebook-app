from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from user.models import User

REGION_CHOICES = [
    ("I", "Ilocos Region"),
    ("II", "Cagayan Valley"),
    ("III", "Central Luzon"),
    ("IV-A", "CALABARZON"),
    ("IV-B", "MIMAROPA"),
    ("V", "Bicol Region"),
    ("VI", "Western Visayas"),
    ("VII", "Central Visayas"),
    ("VIII", "Eastern Visayas"),
    ("IX", "Zamboanga Peninsula"),
    ("X", "Northern Mindanao"),
    ("XI", "Davao Region"),
    ("XII", "SOCCSKSARGEN"),
    ("XIII", "Caraga"),
    ("CAR", "Cordillera Administrative Region"),
    ("NCR", "National Capital Region"),
    ("BARMM", "Bangsamoro Autonomous Region in Muslim Mindanao"),
]


class Contact(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        unique=True,
        related_name="contact",
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

    region = models.CharField(max_length=10, choices=REGION_CHOICES)

    date_created = models.DateTimeField(auto_now_add=True)
