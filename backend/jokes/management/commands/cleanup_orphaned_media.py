import os

from django.conf import settings
from django.core.management.base import BaseCommand

from jokes.joke_picture.variants import variant_names
from jokes.models import JokePicture, ShareableImage

MEDIA_SUBDIRS = ("joke_pictures", "shareable_images")


class Command(BaseCommand):
    help = (
        "Finds media files that no JokePicture or ShareableImage references, e.g. left "
        "behind by an image generation that failed midway. Reports only, unless --delete."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Remove the orphans instead of only listing them.",
        )

    def handle(self, *args, **options):
        delete = options["delete"]
        referenced = self._referenced_names()

        orphaned_files = self._orphaned_files(referenced)
        empty_dirs = self._directories_left_empty(set(orphaned_files))

        for path in orphaned_files:
            self.stdout.write(f"orphaned file {path}")
            if delete:
                os.remove(path)

        for path in empty_dirs:
            self.stdout.write(f"empty directory {path}")
            if delete:
                os.rmdir(path)

        summary = (
            f"{len(orphaned_files)} orphaned files / {len(empty_dirs)} empty directories "
            f"{'removed' if delete else 'found, re-run with --delete to remove them'}"
        )

        if not orphaned_files and not empty_dirs:
            self.stdout.write(self.style.SUCCESS("nothing to clean up"))
        else:
            self.stdout.write(
                self.style.SUCCESS(summary) if delete else self.style.WARNING(summary)
            )

    def _referenced_names(self) -> set:
        referenced = set()

        for name in JokePicture.objects.exclude(image="").values_list("image", flat=True):
            referenced.add(name)
            referenced.update(variant_names(name))

        referenced.update(
            ShareableImage.objects.exclude(image="").values_list("image", flat=True)
        )

        return referenced

    def _orphaned_files(self, referenced: set) -> list:
        orphaned = []

        for subdir in MEDIA_SUBDIRS:
            root = os.path.join(settings.MEDIA_ROOT, subdir)
            for current, _, filenames in os.walk(root):
                for filename in sorted(filenames):
                    path = os.path.join(current, filename)
                    name = os.path.relpath(path, settings.MEDIA_ROOT).replace(os.sep, "/")
                    if name not in referenced:
                        orphaned.append(path)

        return orphaned

    def _directories_left_empty(self, doomed_files: set) -> list:
        """Directories that hold nothing but orphans, children first so rmdir can follow."""
        empty = []

        for subdir in MEDIA_SUBDIRS:
            root = os.path.join(settings.MEDIA_ROOT, subdir)
            for current, dirnames, filenames in os.walk(root, topdown=False):
                if current == root:
                    continue

                keeps_a_file = any(
                    os.path.join(current, name) not in doomed_files for name in filenames
                )
                keeps_a_dir = any(
                    os.path.join(current, name) not in empty for name in dirnames
                )

                if not keeps_a_file and not keeps_a_dir:
                    empty.append(current)

        return empty
