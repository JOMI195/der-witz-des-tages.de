from django.core.management.base import BaseCommand

from seo.render import render_all


class Command(BaseCommand):
    help = "Renders the crawlable versions of / and /galerie/ plus the sitemap into SEO_DIR."

    def handle(self, *args, **options):
        written = render_all()

        if not written:
            self.stdout.write(
                self.style.WARNING(
                    "Nothing rendered - is template.html present in SEO_DIR and a joke of the day set?"
                )
            )
            return

        for path in written:
            self.stdout.write(f"wrote {path}")
        self.stdout.write(self.style.SUCCESS(f"rendered {len(written)} files"))
