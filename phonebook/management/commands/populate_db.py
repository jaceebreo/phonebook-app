from django.core.management.base import BaseCommand
import faker.providers.phone_number
from phonebook.models import Contact
import faker
import faker.providers.company.fil_PH


class Command(BaseCommand):
    help = "Populates the database with sample Contact objects with Filipino company names."

    def handle(self, *args, **options):
        fake = faker.Faker()
        fake.add_provider(faker.providers.company.fil_PH.Provider)

        def fake_phone_number(fake: faker.Faker):
            return f"+639 {fake.msisdn()[4:]}"

        for i in range(30):
            first_name = fake.first_name()
            last_name = fake.last_name()
            company = fake.company()
            telephone_number = fake_phone_number(fake)
            mobile_phone_number = fake_phone_number(fake)

            contact = Contact(
                first_name=first_name,
                last_name=last_name,
                company=company,
                telephone_number=telephone_number,
                mobile_phone_number=mobile_phone_number,
            )
            contact.save()

            self.stdout.write(f"Created contact: {first_name} {last_name}")
