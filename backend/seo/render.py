"""
Renders the crawlable versions of "/" and "/galerie/".

The SPA ships an empty <div id="root">, so search engines and social scrapers
see nothing without JavaScript. This module takes the deployed build's
index.html (copied into SEO_DIR by the nginx container at startup), injects
per-page meta tags plus the actual joke content, and writes the result back
into SEO_DIR where nginx serves it in front of the plain build output.

React mounts with createRoot (not hydrateRoot), so the injected markup is
simply replaced on mount - no hydration mismatch.
"""

import html
import logging
import os
import re
from datetime import date
from typing import List, Optional

from django.conf import settings

from jokes.joke_of_the_day.joke_of_the_day import get_latest_joke_of_the_day
from jokes.joke_picture.variants import variant_urls
from jokes.models import Joke

logger = logging.getLogger(__name__)

TEMPLATE_NAME = "template.html"
GALLERY_PATH = "/galerie/"
GALLERY_PAGE_SIZE = 10  # matches the frontend default in main/archive/archive.tsx
GALLERY_PRERENDERED_PAGES = 10
SITE_NAME = "Der Witz des Tages"
LOGO_PATH = "/witz-des-tages-logo-light-full.svg"

STRIPPED_HEAD_TAGS = [
    re.compile(r"[ \t]*<!--\s*(SEO Meta Tags|Social|Robots)\s*-->\r?\n?", re.I),
    re.compile(r"[ \t]*<title>.*?</title>\r?\n?", re.I | re.S),
    re.compile(r'[ \t]*<meta\s+name="description"[^>]*>\r?\n?', re.I),
    re.compile(r'[ \t]*<meta\s+name="robots"[^>]*>\r?\n?', re.I),
    re.compile(r'[ \t]*<link\s+rel="canonical"[^>]*>\r?\n?', re.I),
    re.compile(r'[ \t]*<meta\s+property="og:[^"]*"[^>]*>\r?\n?', re.I),
    re.compile(r'[ \t]*<meta\s+name="twitter:[^"]*"[^>]*>\r?\n?', re.I),
]


def site_origin() -> str:
    return (getattr(settings, "SITE_ORIGIN", "") or "").rstrip("/")


def absolute(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return site_origin() + path


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def truncate(text: str, length: int = 155) -> str:
    text = " ".join((text or "").split())
    if len(text) <= length:
        return text
    return text[: length - 1].rsplit(" ", 1)[0] + "…"


def joke_picture_url(joke: Joke) -> Optional[str]:
    picture = getattr(joke, "joke_picture", None)
    if not picture:
        return None
    variants = variant_urls(picture.image)
    return absolute(variants.get("w800_jpg") or picture.image.url)


def joke_thumbnail_url(joke: Joke) -> Optional[str]:
    picture = getattr(joke, "joke_picture", None)
    if not picture:
        return None
    variants = variant_urls(picture.image)
    return absolute(variants.get("w400_webp") or variants.get("w800_jpg") or picture.image.url)


def share_image_url(joke: Joke) -> str:
    shareable = getattr(joke, "shareable_image", None)
    if shareable:
        return absolute(shareable.image.url)
    return joke_picture_url(joke) or absolute(LOGO_PATH)


def gallery_jokes(page: int = 1, page_size: int = GALLERY_PAGE_SIZE) -> List[Joke]:
    offset = (page - 1) * page_size
    return list(
        Joke.objects.filter(joke_of_the_day__isnull=False, joke_picture__isnull=False)
        .select_related("created_by", "joke_picture", "shareable_image")
        .prefetch_related("joke_of_the_day")
        .order_by("-joke_of_the_day__created_at")[offset : offset + page_size]
    )


def gallery_joke_count() -> int:
    return Joke.objects.filter(
        joke_of_the_day__isnull=False, joke_picture__isnull=False
    ).count()


def joke_author(joke: Joke) -> str:
    username = joke.created_by.username
    return "jomi" if username == "admin" else username


def joke_date(joke: Joke) -> Optional[date]:
    entry = joke.joke_of_the_day.first()
    return entry.created_at.date() if entry else None


# --------------------------------------------------------------------------
# head tags
# --------------------------------------------------------------------------


def head_tags(
    *,
    title: str,
    description: str,
    canonical: str,
    image: str,
    noindex: bool = False,
    extra: str = "",
) -> str:
    tags = [
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(description)}" />',
        f'<link rel="canonical" href="{esc(canonical)}" />',
        f'<meta name="robots" content="{"noindex, nofollow" if noindex else "index, follow"}" />',
        '<meta property="og:type" content="website" />',
        f'<meta property="og:site_name" content="{SITE_NAME}" />',
        '<meta property="og:locale" content="de_DE" />',
        f'<meta property="og:url" content="{esc(canonical)}" />',
        f'<meta property="og:title" content="{esc(title)}" />',
        f'<meta property="og:description" content="{esc(description)}" />',
        f'<meta property="og:image" content="{esc(image)}" />',
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{esc(title)}" />',
        f'<meta name="twitter:description" content="{esc(description)}" />',
        f'<meta name="twitter:image" content="{esc(image)}" />',
    ]
    return "\n".join(f"  {tag}" for tag in tags) + "\n" + extra


def json_ld(payload: dict) -> str:
    import json

    return f'  <script type="application/ld+json">{json.dumps(payload, ensure_ascii=False)}</script>\n'


def preload_image(url: Optional[str]) -> str:
    """The joke picture is the LCP element - start it before the JS bundle runs."""
    if not url:
        return ""
    return f'  <link rel="preload" as="image" href="{esc(url)}" fetchpriority="high" />\n'


# --------------------------------------------------------------------------
# body markup
# --------------------------------------------------------------------------

FONT_STACK = (
    "Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
)


def shell(inner: str, align: str = "center") -> str:
    return (
        f'<div style="max-width:960px;margin:0 auto;padding:40px 24px;'
        f'font-family:{FONT_STACK};text-align:{align}">{inner}</div>'
    )


def wordmark() -> str:
    return (
        f'<a href="/"><img src="{LOGO_PATH}" alt="{SITE_NAME}" width="320" height="80" '
        'style="max-width:100%;height:auto" /></a>'
    )


def footer_links() -> str:
    return (
        '<p style="font-size:0.8rem"><a href="/galerie/">Galerie</a> · '
        '<a href="/witz-einreichen/">Witz einreichen</a> · '
        '<a href="/kontakt/">Kontakt</a> · '
        '<a href="/datenschutzerklaerung/">Datenschutzerklärung</a> · '
        '<a href="/impressum/">Impressum</a></p>'
    )


def joke_figure(joke: Joke, *, width: int, eager: bool) -> str:
    url = joke_picture_url(joke) if eager else joke_thumbnail_url(joke)
    if not url:
        return ""
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (
        f'<img src="{esc(url)}" alt="Illustration zum Witz: {esc(joke.text)}" '
        f'width="{width}" height="{width}" {loading} decoding="async" '
        'style="max-width:100%;height:auto;border-radius:12px" />'
    )


def home_markup(joke: Joke) -> str:
    published = joke_date(joke) or date.today()
    return shell(
        "".join(
            [
                wordmark(),
                f'<h1 style="font-size:2rem;margin:32px 0 16px">{esc(joke.text)}</h1>',
                f'<h2 style="font-size:1rem;font-weight:400;margin:0 0 24px">Witz des Tages vom '
                f'{published.strftime("%d.%m.%Y")} – eingereicht von {esc(joke_author(joke))}</h2>',
                joke_figure(joke, width=800, eager=True),
                '<p style="margin:32px 0 24px"><a href="/galerie/" style="display:inline-block;'
                'padding:12px 32px;border-radius:10px;background:#7b3ff2;color:#fff;'
                'text-decoration:none">Alle Witze in der Galerie</a></p>',
                '<p style="margin:0 0 32px;font-size:0.9rem">Jeden Morgen ein neuer Flachwitz – '
                'kostenlos als Newsletter oder hier auf der Seite. '
                '<a href="/witz-einreichen/">Reiche deinen eigenen Witz ein.</a></p>',
                footer_links(),
            ]
        )
    )


def gallery_markup(jokes: List[Joke], page: int, has_next: bool) -> str:
    heading = "Witze Galerie" if page == 1 else f"Witze Galerie – Seite {page}"
    articles = []

    for joke in jokes:
        published = joke_date(joke)
        articles.append(
            "<article style=\"margin:0 0 40px\">"
            + joke_figure(joke, width=400, eager=False)
            + f'<h2 style="font-size:1.15rem;margin:12px 0 4px">{esc(joke.text)}</h2>'
            + '<p style="font-size:0.85rem;margin:0">'
            + (f'{published.strftime("%d.%m.%Y")} – ' if published else "")
            + f"eingereicht von {esc(joke_author(joke))}</p>"
            + "</article>"
        )

    nav = []
    if page > 1:
        previous = "/galerie/" if page == 2 else f"/galerie/?page={page - 1}"
        nav.append(f'<a href="{previous}">← Seite {page - 1}</a>')
    if has_next:
        nav.append(f'<a href="/galerie/?page={page + 1}">Seite {page + 1} →</a>')

    return shell(
        "".join(
            [
                f'<div style="margin:0 0 32px">{wordmark()}</div>',
                f'<h1 style="font-size:1.75rem;margin:0 0 24px">{esc(heading)}</h1>',
                "".join(articles)
                or "<p>Aktuell sind noch keine Witze des Tages in der Galerie.</p>",
                f'<p style="margin:24px 0">{" · ".join(nav)}</p>' if nav else "",
                footer_links(),
            ]
        ),
        align="left",
    )


# --------------------------------------------------------------------------
# page assembly & writing
# --------------------------------------------------------------------------


def seo_dir() -> str:
    return str(settings.SEO_DIR)


def read_template() -> Optional[str]:
    """The deployed build's index.html, copied here by the nginx container."""
    path = os.path.join(seo_dir(), TEMPLATE_NAME)
    if not os.path.isfile(path):
        logger.warning("No %s in %s - skipping SEO render", TEMPLATE_NAME, seo_dir())
        return None

    with open(path, "r", encoding="utf-8") as template:
        return template.read()


def build_page(template: str, head: str, markup: str) -> str:
    stripped = template
    for pattern in STRIPPED_HEAD_TAGS:
        stripped = pattern.sub("", stripped)

    with_head = stripped.replace("</head>", f"{head}</head>", 1)
    return with_head.replace('<div id="root"></div>', f'<div id="root">{markup}</div>', 1)


def write_file(relative_path: str, content: str) -> str:
    target = os.path.join(seo_dir(), relative_path)
    os.makedirs(os.path.dirname(target), exist_ok=True)

    temporary = f"{target}.tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(content)
    os.replace(temporary, target)

    return target


def render_home(template: str) -> Optional[str]:
    entry = get_latest_joke_of_the_day()
    if entry is None:
        logger.warning("No joke of the day yet - skipping home render")
        return None

    joke = entry.joke
    published = joke_date(joke) or entry.created_at.date()
    title = f"{truncate(joke.text, 60)} – Witz des Tages"
    description = truncate(
        f"{joke.text} Der Witz des Tages vom {published.strftime('%d.%m.%Y')} – "
        "täglich ein neuer Flachwitz mit passendem Bild."
    )
    canonical = site_origin() + "/"
    picture = joke_picture_url(joke)

    structured = json_ld(
        {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": truncate(joke.text, 60),
            "text": joke.text,
            "image": picture,
            "datePublished": published.isoformat(),
            "inLanguage": "de-DE",
            "author": {"@type": "Person", "name": joke_author(joke)},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": site_origin()},
            "url": canonical,
        }
    )

    head = head_tags(
        title=title,
        description=description,
        canonical=canonical,
        image=share_image_url(joke),
        extra=preload_image(picture) + structured,
    )

    return write_file("index.html", build_page(template, head, home_markup(joke)))


def render_gallery(template: str) -> List[str]:
    total = gallery_joke_count()
    total_pages = max(1, -(-total // GALLERY_PAGE_SIZE))
    written = []

    for page in range(1, min(total_pages, GALLERY_PRERENDERED_PAGES) + 1):
        jokes = gallery_jokes(page)
        has_next = page < total_pages
        canonical = site_origin() + GALLERY_PATH + (f"?page={page}" if page > 1 else "")
        title = "Witze Galerie – alle Witze des Tages" + (f" – Seite {page}" if page > 1 else "")
        description = truncate(
            "Alle bisherigen Witze des Tages mit ihren Bildern: durchstöbere die Galerie "
            f"({total} Witze) und finde deinen Lieblingswitz."
            if page == 1
            else f"Seite {page} der Witze Galerie – alle bisherigen Witze des Tages mit Bildern."
        )

        structured = json_ld(
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": title,
                "url": canonical,
                "numberOfItems": len(jokes),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index + 1,
                        "item": {
                            "@type": "CreativeWork",
                            "text": joke.text,
                            "image": joke_thumbnail_url(joke),
                            "inLanguage": "de-DE",
                        },
                    }
                    for index, joke in enumerate(jokes)
                ],
            }
        )

        head = head_tags(
            title=title,
            description=description,
            canonical=canonical,
            image=share_image_url(jokes[0]) if jokes else absolute(LOGO_PATH),
            extra=structured,
        )

        content = build_page(template, head, gallery_markup(jokes, page, has_next))

        # nginx maps ?page=N onto page-N.html and the bare URL onto index.html
        written.append(write_file(f"galerie/page-{page}.html", content))
        if page == 1:
            written.append(write_file("galerie/index.html", content))

    return written


def render_sitemap() -> str:
    latest = get_latest_joke_of_the_day()
    latest_date = (latest.created_at.date() if latest else date.today()).isoformat()
    total_pages = max(1, -(-gallery_joke_count() // GALLERY_PAGE_SIZE))
    origin = site_origin()

    urls = [
        (f"{origin}/", latest_date, "daily", "1.0"),
        (f"{origin}/galerie/", latest_date, "daily", "0.8"),
    ]
    urls += [
        (f"{origin}/galerie/?page={page}", latest_date, "weekly", "0.6")
        for page in range(2, min(total_pages, GALLERY_PRERENDERED_PAGES) + 1)
    ]
    urls += [
        (f"{origin}/witz-einreichen/", latest_date, "yearly", "0.5"),
        (f"{origin}/kontakt/", latest_date, "yearly", "0.3"),
        (f"{origin}/datenschutzerklaerung/", latest_date, "yearly", "0.1"),
        (f"{origin}/impressum/", latest_date, "yearly", "0.1"),
    ]

    entries = []
    for location, lastmod, changefreq, priority in urls:
        entries.append(
            "  <url>\n"
            f"    <loc>{esc(location)}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )

    # joke pictures are worth their own image entries for Google Images
    for joke in gallery_jokes(page=1, page_size=GALLERY_PAGE_SIZE):
        image = joke_thumbnail_url(joke)
        if not image:
            continue
        entries.append(
            "  <url>\n"
            f"    <loc>{origin}/galerie/</loc>\n"
            "    <image:image>\n"
            f"      <image:loc>{esc(image)}</image:loc>\n"
            f"      <image:title>{esc(truncate(joke.text, 90))}</image:title>\n"
            "    </image:image>\n"
            "  </url>"
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )

    return write_file("sitemap.xml", sitemap)


def render_all() -> List[str]:
    template = read_template()
    if template is None:
        return []

    written = []
    home = render_home(template)
    if home:
        written.append(home)
    written.extend(render_gallery(template))
    written.append(render_sitemap())

    logger.info("Rendered %s SEO files into %s", len(written), seo_dir())
    return written
