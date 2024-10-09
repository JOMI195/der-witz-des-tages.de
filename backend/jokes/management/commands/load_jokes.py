import codecs
import os
from django.core.management.base import BaseCommand
from jokes.models import Joke
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    help = "Load jokes from a text file"

    def handle(self, *args, **kwargs):
        file_path = settings.BASE_DIR / "fixtures" / "jokes.txt"
        user_model = get_user_model()
        default_user = user_model.objects.first()

        if not default_user:
            self.stdout.write(
                self.style.ERROR("No default user found. Please create a user first.")
            )
            return

        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))
            return

        joke_file = codecs.open(file_path, "r", "utf-8")
        jokes = joke_file.readlines()
        joke_file.close()

        for line in jokes:
            joke_text = line.strip()
            if joke_text:
                Joke.objects.get_or_create(text=joke_text, created_by=default_user)

        self.stdout.write(self.style.SUCCESS("Successfully loaded jokes."))
