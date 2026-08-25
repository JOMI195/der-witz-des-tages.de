import io
import os
import shutil
import tempfile
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from PIL import Image

from jokes.joke_picture.joke_picture import save_image_to_model
from jokes.joke_picture.variants import has_all_variants, variant_names
from jokes.models import Joke, JokePicture, ShareableImage
from jokes.sharableImage.sharableImage import save_shareable_image_to_model


def jpeg_bytes(size=(20, 10)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", size, (200, 30, 30)).save(buffer, format="JPEG")
    return buffer.getvalue()


def raise_once_the_image_is_set(model):
    """Fails the save that follows the file write, not the one from get_or_create."""
    original_save = model.save

    def save(self, *args, **kwargs):
        if self.image.name:
            raise RuntimeError("boom")
        return original_save(self, *args, **kwargs)

    return patch.object(model, "save", save)


class ImageStorageTestCase(TestCase):
    def setUp(self):
        media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media_root, ignore_errors=True)
        overridden = override_settings(MEDIA_ROOT=media_root)
        overridden.enable()
        self.addCleanup(overridden.disable)

        self.media_root = media_root
        self.user = get_user_model().objects.create(
            email="test@example.com", username="tester"
        )
        self.joke = Joke.objects.create(text="Ein Witz", created_by=self.user)

    def absolute(self, name: str) -> str:
        return os.path.join(self.media_root, name)

    def stored_entries(self, subdir: str) -> list:
        root = os.path.join(self.media_root, subdir)
        if not os.path.isdir(root):
            return []
        return sorted(os.listdir(root))


class JokePictureStorageTests(ImageStorageTestCase):
    def test_creates_first_picture_for_joke_without_image(self):
        joke_picture = save_image_to_model(joke=self.joke, image_data=jpeg_bytes())

        self.assertTrue(joke_picture.image.name)
        self.assertTrue(os.path.isfile(self.absolute(joke_picture.image.name)))
        self.assertTrue(has_all_variants(joke_picture.image))

    def test_replacing_picture_removes_old_file_variants_and_directory(self):
        old_name = save_image_to_model(
            joke=self.joke, image_data=jpeg_bytes()
        ).image.name

        with self.captureOnCommitCallbacks(execute=True):
            new_picture = save_image_to_model(
                joke=self.joke, image_data=jpeg_bytes((30, 20))
            )

        self.assertNotEqual(new_picture.image.name, old_name)
        self.assertTrue(os.path.isfile(self.absolute(new_picture.image.name)))
        self.assertTrue(has_all_variants(new_picture.image))

        self.assertFalse(os.path.exists(self.absolute(old_name)))
        for variant in variant_names(old_name):
            self.assertFalse(os.path.exists(self.absolute(variant)))
        self.assertFalse(os.path.isdir(os.path.dirname(self.absolute(old_name))))

    def test_failed_save_leaves_no_orphan_file(self):
        with patch(
            "jokes.joke_picture.joke_picture.generate_variants",
            side_effect=RuntimeError("boom"),
        ):
            with self.assertRaises(RuntimeError):
                save_image_to_model(joke=self.joke, image_data=jpeg_bytes())

        self.assertFalse(JokePicture.objects.exists())
        self.assertEqual(self.stored_entries("joke_pictures"), [])

    def test_delete_removes_file_variants_and_directory(self):
        joke_picture = save_image_to_model(joke=self.joke, image_data=jpeg_bytes())
        name = joke_picture.image.name

        with self.captureOnCommitCallbacks(execute=True):
            joke_picture.delete()

        self.assertFalse(os.path.exists(self.absolute(name)))
        for variant in variant_names(name):
            self.assertFalse(os.path.exists(self.absolute(variant)))
        self.assertEqual(self.stored_entries("joke_pictures"), [])


class ShareableImageStorageTests(ImageStorageTestCase):
    def test_creates_first_shareable_image(self):
        shareable_image = save_shareable_image_to_model(
            joke=self.joke, image_data=jpeg_bytes()
        )

        self.assertTrue(shareable_image.image.name)
        self.assertTrue(os.path.isfile(self.absolute(shareable_image.image.name)))

    def test_replacing_shareable_image_removes_old_file_and_directory(self):
        old_name = save_shareable_image_to_model(
            joke=self.joke, image_data=jpeg_bytes()
        ).image.name

        with self.captureOnCommitCallbacks(execute=True):
            new_image = save_shareable_image_to_model(
                joke=self.joke, image_data=jpeg_bytes((30, 20))
            )

        self.assertNotEqual(new_image.image.name, old_name)
        self.assertTrue(os.path.isfile(self.absolute(new_image.image.name)))
        self.assertFalse(os.path.exists(self.absolute(old_name)))
        self.assertFalse(os.path.isdir(os.path.dirname(self.absolute(old_name))))

    def test_failed_save_leaves_no_orphan_file(self):
        with raise_once_the_image_is_set(ShareableImage):
            with self.assertRaises(RuntimeError):
                save_shareable_image_to_model(joke=self.joke, image_data=jpeg_bytes())

        self.assertFalse(ShareableImage.objects.exists())
        self.assertEqual(self.stored_entries("shareable_images"), [])


class CleanupOrphanedMediaTests(ImageStorageTestCase):
    def orphan(self, subdir: str) -> str:
        directory = os.path.join(self.media_root, subdir, "left-over-uuid")
        os.makedirs(directory)
        path = os.path.join(directory, "joke_99.jpg")
        with open(path, "wb") as orphan_file:
            orphan_file.write(jpeg_bytes())
        return path

    def cleanup(self, *args) -> str:
        output = StringIO()
        call_command("cleanup_orphaned_media", *args, stdout=output)
        return output.getvalue()

    def test_reports_orphans_without_removing_them(self):
        path = self.orphan("joke_pictures")

        output = self.cleanup()

        self.assertIn(path, output)
        self.assertIn("--delete", output)
        self.assertTrue(os.path.isfile(path))

    def test_delete_removes_orphan_and_its_directory(self):
        path = self.orphan("joke_pictures")
        shareable_orphan = self.orphan("shareable_images")

        self.cleanup("--delete")

        self.assertFalse(os.path.exists(path))
        self.assertFalse(os.path.isdir(os.path.dirname(path)))
        self.assertFalse(os.path.exists(shareable_orphan))
        self.assertEqual(self.stored_entries("joke_pictures"), [])
        self.assertEqual(self.stored_entries("shareable_images"), [])

    def test_delete_keeps_referenced_images_and_their_variants(self):
        joke_picture = save_image_to_model(joke=self.joke, image_data=jpeg_bytes())
        shareable_image = save_shareable_image_to_model(
            joke=self.joke, image_data=jpeg_bytes()
        )
        self.orphan("joke_pictures")

        output = self.cleanup("--delete")

        self.assertTrue(os.path.isfile(self.absolute(joke_picture.image.name)))
        self.assertTrue(has_all_variants(joke_picture.image))
        self.assertTrue(os.path.isfile(self.absolute(shareable_image.image.name)))
        self.assertIn("1 orphaned files", output)

    def test_reports_nothing_when_media_is_clean(self):
        save_image_to_model(joke=self.joke, image_data=jpeg_bytes())

        self.assertIn("nothing to clean up", self.cleanup())
