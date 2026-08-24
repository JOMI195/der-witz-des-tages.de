from config.celery import celery

from seo.render import render_all


@celery.task
def render_seo_pages(*args, **kwargs):
    """
    Re-renders the crawlable "/" and "/galerie/" pages plus the sitemap.

    Runs after the daily joke workflow (so the new joke and its shareable image
    are in place) and on a schedule, which also picks up a fresh deployment:
    the nginx container writes a new template.html with the new asset hashes.
    """
    written = render_all()
    return {"rendered": len(written)}
