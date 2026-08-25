import os

from django.core.management.base import BaseCommand

from jokes.joke_picture.joke_picture import get_or_create_joke_picture
from jokes.joke_picture.variants import generate_variants, has_all_variants
from jokes.models import Joke, JokeOfTheDay, JokePicture, ShareableImage
from jokes.sharableImage.screenshot import capture_screenshot
from jokes.sharableImage.sharableImage import save_shareable_image_to_model
from jokes.sharableImage.template import get_shareable_image_html_template


class Command(BaseCommand):
    help = (
        "Makes sure every joke that was joke of the day has a picture with all "
        "variants and a shareable image. A missing picture costs an image API "
        "call, so start with --dry-run."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only report what is missing.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Process at most this many jokes, most recent joke of the day first.",
        )
        parser.add_argument(
            "--skip-pictures",
            action="store_true",
            help="Never generate a missing picture, no image API calls.",
        )
        parser.add_argument(
            "--skip-shareable",
            action="store_true",
            help="Leave shareable images alone.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        limit = options["limit"]
        joke_ids = self._joke_of_the_day_ids()

        if limit:
            joke_ids = joke_ids[:limit]

        changed = complete = failed = 0

        jokes = Joke.objects.in_bulk(joke_ids)

        for joke_id in joke_ids:
            joke = jokes.get(joke_id)
            if joke is None:
                continue

            try:
                actions = []
                if not options["skip_pictures"]:
                    actions.append(self._ensure_picture(joke, dry_run))
                if not options["skip_shareable"]:
                    actions.append(self._ensure_shareable_image(joke, dry_run))

                actions = [action for action in actions if action]
                if actions:
                    changed += 1
                    self.stdout.write(f"joke {joke.id}: {', '.join(actions)}")
                else:
                    complete += 1
            except Exception as error:  # one bad joke must not abort the backlog
                failed += 1
                self.stderr.write(f"joke {joke.id} failed: {error}")

        verb = "would change" if dry_run else "changed"
        summary = f"{changed} {verb} / {complete} already complete / {failed} failed"
        self.stdout.write(
            self.style.WARNING(summary) if failed else self.style.SUCCESS(summary)
        )

    def _joke_of_the_day_ids(self) -> list:
        """Every joke that ever was joke of the day, most recent first."""
        ordered = []
        seen = set()

        for joke_id in JokeOfTheDay.objects.order_by("-created_at").values_list(
            "joke_id", flat=True
        ):
            if joke_id not in seen:
                seen.add(joke_id)
                ordered.append(joke_id)

        return ordered

    def _ensure_picture(self, joke: Joke, dry_run: bool):
        picture = JokePicture.objects.filter(joke=joke).first()

        if picture is None or not self._file_exists(picture):
            if dry_run:
                return "picture missing"
            get_or_create_joke_picture(joke=joke)
            return "picture generated"

        if not has_all_variants(picture.image):
            if dry_run:
                return "variants missing"
            generate_variants(picture.image)
            return "variants generated"

        return None

    def _ensure_shareable_image(self, joke: Joke, dry_run: bool):
        shareable_image = ShareableImage.objects.filter(joke=joke).first()

        if shareable_image is not None and self._file_exists(shareable_image):
            return None

        if dry_run:
            return "shareable image missing"

        picture = JokePicture.objects.filter(joke=joke).first()
        if picture is None or not self._file_exists(picture):
            return "shareable image skipped, no picture"

        image_data = capture_screenshot(
            get_shareable_image_html_template(joke=joke, image_field=picture.image)
        )
        if not image_data:
            raise RuntimeError("screenshot failed, is the chrome service reachable?")

        save_shareable_image_to_model(joke=joke, image_data=image_data)
        return "shareable image created"

    @staticmethod
    def _file_exists(instance) -> bool:
        return bool(instance.image.name) and os.path.isfile(instance.image.path)
