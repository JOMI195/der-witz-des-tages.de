import io
import logging
import os
from typing import Dict, List, Optional

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

# (suffix, width, pillow format, save options)
WEB_VARIANTS = [
    ("w400.webp", 400, "WEBP", {"quality": 80, "method": 6}),
    ("w800.webp", 800, "WEBP", {"quality": 80, "method": 6}),
]

# Email clients (Outlook, Windows Mail) do not render WebP, so the newsletter
# gets a JPEG variant instead of the full size original.
EMAIL_VARIANT = ("w800.jpg", 800, "JPEG", {"quality": 82, "optimize": True, "progressive": True})

ALL_VARIANTS = WEB_VARIANTS + [EMAIL_VARIANT]


def variant_name(image_name: str, suffix: str) -> str:
    """joke_pictures/<uuid>/joke_7.jpg + "w400.webp" -> joke_pictures/<uuid>/joke_7_w400.webp"""
    base, _ = os.path.splitext(image_name)
    return f"{base}_{suffix}"


def variant_names(image_name: str) -> List[str]:
    return [variant_name(image_name, suffix) for suffix, _, _, _ in ALL_VARIANTS]


def _directory_writable(image_name: str) -> bool:
    """
    Variants live next to the original, so an unwritable picture directory has
    to be reported once instead of once per variant.
    """
    try:
        directory = os.path.dirname(default_storage.path(image_name))
    except (NotImplementedError, AttributeError):
        return True  # non-filesystem storage, let the write itself decide

    return os.access(directory, os.W_OK)


def _image_name(image_field) -> Optional[str]:
    """Accepts a FieldFile or the stored name, so cleanup can work without an instance."""
    if isinstance(image_field, str):
        return image_field or None
    return getattr(image_field, "name", None) or None


def generate_variants(image_field: FieldFile, overwrite: bool = False) -> Dict[str, str]:
    """
    Writes the resized variants next to the original.

    Never raises: a missing variant degrades to the original everywhere it is
    consumed, and must not break the daily joke workflow.
    """
    created: Dict[str, str] = {}
    image_name = _image_name(image_field)

    if not image_name or not default_storage.exists(image_name):
        logger.warning("No source image to generate variants from (%s)", image_name)
        return created

    try:
        with default_storage.open(image_name, "rb") as source:
            original = Image.open(source)
            original = ImageOps.exif_transpose(original)
            original.load()
    except Exception:
        logger.exception("Could not read joke picture %s", image_name)
        return created

    if not _directory_writable(image_name):
        logger.error(
            "Cannot write variants next to %s: the directory is not writable by this user. "
            "Fix the ownership of the media volume, e.g. "
            "docker exec -u root backend chown -R app:app /home/app/backend/mediafiles",
            image_name,
        )
        return created

    for suffix, width, image_format, options in ALL_VARIANTS:
        target = variant_name(image_name, suffix)

        if default_storage.exists(target):
            if not overwrite:
                continue
            default_storage.delete(target)

        try:
            resized = original.copy()
            resized.thumbnail((width, width), Image.LANCZOS)
            if image_format == "JPEG" and resized.mode not in ("RGB", "L"):
                resized = resized.convert("RGB")

            buffer = io.BytesIO()
            resized.save(buffer, format=image_format, **options)
            default_storage.save(target, ContentFile(buffer.getvalue()))
            created[suffix] = target
        except Exception:
            logger.exception("Could not generate %s variant for %s", suffix, image_name)

    return created


def has_all_variants(image_field: FieldFile) -> bool:
    image_name = _image_name(image_field)
    if not image_name:
        return False
    return all(default_storage.exists(name) for name in variant_names(image_name))


def delete_variants(image_field: FieldFile) -> None:
    """Removes every generated variant of an image. Safe to call twice."""
    image_name = _image_name(image_field)
    if not image_name:
        return

    for name in variant_names(image_name):
        try:
            if default_storage.exists(name):
                default_storage.delete(name)
        except Exception:
            logger.exception("Could not delete variant %s", name)


def variant_urls(image_field: FieldFile) -> Dict[str, Optional[str]]:
    """URLs for the API, keyed the way the frontend consumes them."""
    image_name = _image_name(image_field)
    urls: Dict[str, Optional[str]] = {"w400_webp": None, "w800_webp": None, "w800_jpg": None}

    if not image_name:
        return urls

    for suffix, key in (("w400.webp", "w400_webp"), ("w800.webp", "w800_webp"), ("w800.jpg", "w800_jpg")):
        name = variant_name(image_name, suffix)
        if default_storage.exists(name):
            urls[key] = default_storage.url(name)

    return urls


def email_variant_path(image_field: FieldFile) -> str:
    """Absolute path of the JPEG variant used for the newsletter, original as fallback."""
    image_name = _image_name(image_field)
    if image_name:
        target = variant_name(image_name, EMAIL_VARIANT[0])
        if default_storage.exists(target):
            return default_storage.path(target)

    return image_field.path
