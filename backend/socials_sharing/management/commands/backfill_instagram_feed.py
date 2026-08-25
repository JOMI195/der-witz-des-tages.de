from datetime import date

from django.core.management.base import BaseCommand
from django.utils import timezone

from socials_sharing import backfill
from socials_sharing.models import InstagramShare


class Command(BaseCommand):
    help = "Reposts jokes of the day that were missed while Instagram sharing was broken."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only report what would be posted.",
        )
        parser.add_argument(
            "--status",
            action="store_true",
            help="Show backlog, daily cap, posts in the last 24h and cooldown state.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=1,
            help="Post at most this many images in this run (default 1).",
        )
        parser.add_argument(
            "--since",
            type=date.fromisoformat,
            default=None,
            help="Only consider jokes of the day from this date on (YYYY-MM-DD).",
        )
        parser.add_argument(
            "--ignore-cap",
            action="store_true",
            help="Bypass the daily rate cap for a manual catch-up.",
        )

    def handle(self, *args, **options):
        since = options["since"] or backfill.backfill_since()
        pending = backfill.candidates(since)

        if options["status"]:
            self.print_status(since, pending)
            return

        if options["dry_run"]:
            self.print_dry_run(since, pending, options["limit"])
            return

        posted = 0
        for _ in range(options["limit"]):
            result = backfill.post_next(since=since, ignore_cap=options["ignore_cap"])
            if "skipped" in result:
                self.stdout.write(f"stopped: {result['skipped']}")
                break
            posted += 1
            self.stdout.write(
                f"posted joke {result['joke_id']} from {result['day']} "
                f"({result['media_pk']}), {result['remaining']} left"
            )

        self.stdout.write(self.style.SUCCESS(f"posted {posted} image(s)"))

    def print_status(self, since, pending):
        self.stdout.write(f"since:              {since}")
        self.stdout.write(f"backlog:            {pending.count()}")
        self.stdout.write(f"daily cap:          {backfill.daily_cap()}")
        self.stdout.write(f"posted last 24h:    {backfill.posted_last_24h()}")
        self.stdout.write(f"remaining today:    {backfill.remaining_budget()}")
        self.stdout.write(
            f"cooldown:           {backfill.cooldown_until() or 'none'}"
        )
        self.stdout.write(
            f"feed shares total:  "
            f"{InstagramShare.objects.filter(kind=InstagramShare.FEED).count()}"
        )

    def print_dry_run(self, since, pending, limit):
        self.stdout.write(f"{pending.count()} joke(s) waiting since {since}")

        missing = 0
        for joke_of_the_day in pending:
            image = joke_of_the_day.joke.shareable_image
            day = timezone.localtime(joke_of_the_day.created_at).date()
            if not image.image or not self.file_exists(image):
                missing += 1
                self.stderr.write(f"{day}: image file missing ({image.image.name})")

        for joke_of_the_day in pending[:limit]:
            day = timezone.localtime(joke_of_the_day.created_at).date()
            self.stdout.write(f"would post {day} (joke {joke_of_the_day.joke_id})")

        if missing:
            self.stderr.write(self.style.WARNING(f"{missing} image file(s) missing"))

    @staticmethod
    def file_exists(shareable_image) -> bool:
        import os

        return os.path.exists(shareable_image.image.path)
