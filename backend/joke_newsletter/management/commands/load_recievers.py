import codecs
import os
from django.core.management.base import BaseCommand
from joke_newsletter.models import NewsletterReciever
from django.conf import settings


class Command(BaseCommand):
    help = "Load newsletter recievers from a text file"

    def handle(self, *args, **kwargs):
        file_path = settings.BASE_DIR / "fixtures" / "recievers.txt"

        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))
            return

        recievers_file = codecs.open(file_path, "r", "utf-8")
        recievers = recievers_file.readlines()
        recievers_file.close()

        for line in recievers:
            reciever = line.strip()
            if reciever:
                NewsletterReciever.objects.get_or_create(email=reciever)

        self.stdout.write(self.style.SUCCESS("Successfully loaded recievers."))
