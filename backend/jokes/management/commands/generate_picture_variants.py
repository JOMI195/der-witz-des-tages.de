from django.core.management.base import BaseCommand

from jokes.joke_picture.variants import generate_variants, has_all_variants
from jokes.models import JokePicture


class Command(BaseCommand):
    help = "Generates the resized variants (400/800 WebP, 800 JPEG) for existing joke pictures."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate variants even when they already exist.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only report what would be generated.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Process at most this many pictures (to batch through a large backlog).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        dry_run = options["dry_run"]
        limit = options["limit"]

        pictures = JokePicture.objects.select_related("joke").order_by("id")
        if limit:
            pictures = pictures[:limit]

        created = skipped = failed = 0

        for picture in pictures:
            label = f"joke {picture.joke_id} ({picture.image.name})"

            try:
                if not force and has_all_variants(picture.image):
                    skipped += 1
                    continue

                if dry_run:
                    self.stdout.write(f"would generate variants for {label}")
                    created += 1
                    continue

                variants = generate_variants(picture.image, overwrite=force)
                if variants:
                    created += 1
                    self.stdout.write(f"generated {len(variants)} variants for {label}")
                else:
                    failed += 1
                    self.stderr.write(f"no variants generated for {label}")
            except Exception as error:  # keep going, one bad file must not abort the run
                failed += 1
                self.stderr.write(f"failed for {label}: {error}")

        summary = f"created {created} / skipped {skipped} / failed {failed}"
        self.stdout.write(self.style.SUCCESS(summary) if not failed else self.style.WARNING(summary))
