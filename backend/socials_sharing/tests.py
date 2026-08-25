import os
import tempfile
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings
from django.utils import timezone

from jokes.models import Joke, JokeOfTheDay, ShareableImage
from socials_sharing import backfill
from socials_sharing import tasks
from socials_sharing.instagram import instagram
from socials_sharing.models import InstagramShare

PIXEL = (
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    b"\xff\xdb\x00C\x00" + b"\x08" * 64 + b"\xff\xd9"
)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BackfillTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create(
            email="test@example.com", username="tester"
        )

    def _joke_of_the_day(self, day: date, with_image: bool = True) -> JokeOfTheDay:
        joke = Joke.objects.create(text=f"Witz vom {day}", created_by=self.user)
        if with_image:
            image = ShareableImage(joke=joke)
            image.image.save(f"shareable_{joke.id}.jpg", ContentFile(PIXEL), save=True)
        jotd = JokeOfTheDay.objects.create(joke=joke)
        # created_at is auto_now_add, so it has to be corrected afterwards
        JokeOfTheDay.objects.filter(pk=jotd.pk).update(
            created_at=timezone.make_aware(
                timezone.datetime(day.year, day.month, day.day, 5, 0)
            )
        )
        return JokeOfTheDay.objects.get(pk=jotd.pk)

    def _mark_posted(self, jotd, *, is_backfill=True, days_ago=0):
        share = InstagramShare.objects.create(
            joke=jotd.joke,
            kind=InstagramShare.FEED,
            media_pk="1",
            is_backfill=is_backfill,
        )
        InstagramShare.objects.filter(pk=share.pk).update(
            posted_at=timezone.now() - timedelta(days=days_ago)
        )
        return share

    def test_candidates_are_newest_first(self):
        for day in (date(2026, 2, 4), date(2026, 2, 6), date(2026, 2, 5)):
            self._joke_of_the_day(day)

        candidates = backfill.candidates(since=date(2026, 2, 3))

        self.assertEqual(
            [c.created_at.date() for c in candidates],
            [date(2026, 2, 6), date(2026, 2, 5), date(2026, 2, 4)],
        )

    def test_candidates_respect_the_since_cutoff(self):
        self._joke_of_the_day(date(2024, 11, 2))
        self._joke_of_the_day(date(2026, 2, 4))

        candidates = backfill.candidates(since=date(2026, 2, 3))

        self.assertEqual([c.created_at.date() for c in candidates], [date(2026, 2, 4)])

    def test_candidates_skip_already_posted_jokes(self):
        posted = self._joke_of_the_day(date(2026, 2, 4))
        self._joke_of_the_day(date(2026, 2, 5))
        self._mark_posted(posted)

        candidates = backfill.candidates(since=date(2026, 2, 3))

        self.assertEqual([c.created_at.date() for c in candidates], [date(2026, 2, 5)])

    def test_candidates_skip_jokes_without_a_shareable_image(self):
        self._joke_of_the_day(date(2026, 2, 4), with_image=False)

        self.assertEqual(list(backfill.candidates(since=date(2026, 2, 3))), [])

    def test_a_joke_cannot_reach_the_feed_twice(self):
        jotd = self._joke_of_the_day(date(2026, 2, 4))
        self._mark_posted(jotd)

        with self.assertRaises(IntegrityError):
            InstagramShare.objects.create(
                joke=jotd.joke, kind=InstagramShare.FEED, media_pk="2"
            )

    def test_daily_cap_ramps_up_over_two_weeks(self):
        self.assertEqual(backfill.daily_cap(), 1)

        first = self._joke_of_the_day(date(2026, 2, 4))
        self._mark_posted(first, days_ago=8)
        self.assertEqual(backfill.daily_cap(), 2)

        InstagramShare.objects.all().delete()
        second = self._joke_of_the_day(date(2026, 2, 5))
        self._mark_posted(second, days_ago=20)
        self.assertEqual(backfill.daily_cap(), 3)

    def test_daily_cap_ignores_the_regular_daily_posts(self):
        jotd = self._joke_of_the_day(date(2026, 2, 4))
        self._mark_posted(jotd, is_backfill=False, days_ago=200)

        self.assertEqual(backfill.daily_cap(), 1)

    def test_budget_is_spent_after_the_cap_is_reached(self):
        jotd = self._joke_of_the_day(date(2026, 2, 4))
        self.assertEqual(backfill.remaining_budget(), 1)

        self._mark_posted(jotd)
        self.assertEqual(backfill.remaining_budget(), 0)

    def test_budget_only_counts_the_last_24_hours(self):
        jotd = self._joke_of_the_day(date(2026, 2, 4))
        self._mark_posted(jotd, days_ago=2)

        self.assertEqual(backfill.posted_last_24h(), 0)

    def test_cooldown_blocks_the_next_run(self):
        self.assertFalse(backfill.in_cooldown())

        backfill.start_cooldown(hours=24)

        self.assertTrue(backfill.in_cooldown())

    def test_failed_upload_starts_a_cooldown_and_posts_nothing(self):
        self._joke_of_the_day(date(2026, 2, 4))

        with patch("socials_sharing.backfill.login_user_to_instagram") as login:
            login.return_value.photo_upload.side_effect = Exception("467")
            with self.assertRaises(Exception):
                backfill.post_next(since=date(2026, 2, 3))

        self.assertTrue(backfill.in_cooldown())
        self.assertEqual(InstagramShare.objects.count(), 0)

    def test_post_next_uploads_the_newest_missing_joke_and_records_it(self):
        self._joke_of_the_day(date(2026, 2, 4))
        newest = self._joke_of_the_day(date(2026, 2, 5))

        with patch("socials_sharing.backfill.login_user_to_instagram") as login:
            login.return_value.photo_upload.return_value.pk = "42"
            result = backfill.post_next(since=date(2026, 2, 3))

        share = InstagramShare.objects.get()
        self.assertEqual(share.joke_id, newest.joke_id)
        self.assertEqual(share.media_pk, "42")
        self.assertTrue(share.is_backfill)
        self.assertEqual(result["joke_id"], newest.joke_id)

    def test_post_next_uses_the_original_date_in_the_caption(self):
        self._joke_of_the_day(date(2026, 2, 5))

        with patch("socials_sharing.backfill.login_user_to_instagram") as login:
            login.return_value.photo_upload.return_value.pk = "42"
            backfill.post_next(since=date(2026, 2, 3))

        caption = login.return_value.photo_upload.call_args.kwargs["caption"]
        self.assertIn("05.02.2026", caption)

    def test_post_next_no_ops_when_the_budget_is_spent(self):
        spent = self._joke_of_the_day(date(2026, 2, 4))
        self._joke_of_the_day(date(2026, 2, 5))
        self._mark_posted(spent)

        with patch("socials_sharing.backfill.login_user_to_instagram") as login:
            result = backfill.post_next(since=date(2026, 2, 3))

        login.assert_not_called()
        self.assertEqual(result["skipped"], "budget spent")

    def test_post_next_no_ops_during_cooldown(self):
        self._joke_of_the_day(date(2026, 2, 4))
        backfill.start_cooldown(hours=24)

        with patch("socials_sharing.backfill.login_user_to_instagram") as login:
            result = backfill.post_next(since=date(2026, 2, 3))

        login.assert_not_called()
        self.assertEqual(result["skipped"], "cooldown")

    def test_post_next_no_ops_when_the_backlog_is_empty(self):
        with patch("socials_sharing.backfill.login_user_to_instagram") as login:
            result = backfill.post_next(since=date(2026, 2, 3))

        login.assert_not_called()
        self.assertEqual(result["skipped"], "nothing to post")


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DailyShareTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create(
            email="daily@example.com", username="daily"
        )
        self.joke = Joke.objects.create(text="Heutiger Witz", created_by=self.user)
        image = ShareableImage(joke=self.joke)
        image.image.save(f"shareable_{self.joke.id}.jpg", ContentFile(PIXEL), save=True)
        self.jotd = JokeOfTheDay.objects.create(joke=self.joke)

    def test_daily_share_records_feed_and_story(self):
        client = MagicMock()
        client.photo_upload.return_value.pk = "10"
        client.photo_upload_to_story.return_value.pk = "11"

        instagram.upload_shareable_image(client)

        shares = InstagramShare.objects.filter(joke=self.joke)
        self.assertEqual(
            sorted(shares.values_list("kind", "media_pk")),
            [(InstagramShare.FEED, "10"), (InstagramShare.STORY, "11")],
        )
        self.assertFalse(any(share.is_backfill for share in shares))

    def test_daily_share_reports_both_failures(self):
        client = MagicMock()
        client.photo_upload.side_effect = Exception("feed boom")
        client.photo_upload_to_story.side_effect = Exception("story boom")

        with self.assertRaises(Exception) as raised:
            instagram.upload_shareable_image(client)

        self.assertIn("feed boom", str(raised.exception))
        self.assertIn("story boom", str(raised.exception))
        self.assertEqual(InstagramShare.objects.count(), 0)

    def test_daily_share_raises_when_the_image_file_is_gone(self):
        os.remove(self.joke.shareable_image.image.path)
        client = MagicMock()

        with self.assertRaises(Exception) as raised:
            instagram.upload_shareable_image(client)

        self.assertIn("missing", str(raised.exception))
        client.photo_upload.assert_not_called()


class ProductionGuardTestCase(TestCase):
    @override_settings(PRODUCTION=False)
    def test_backfill_task_is_a_no_op_outside_production(self):
        with patch("socials_sharing.backfill.post_next") as post_next:
            result = tasks.backfill_instagram_feed()

        post_next.assert_not_called()
        self.assertEqual(result["skipped"], "not production")

    @override_settings(PRODUCTION=False)
    def test_dispatcher_is_a_no_op_outside_production(self):
        with patch("socials_sharing.tasks.backfill_instagram_feed") as task:
            result = tasks.dispatch_instagram_backfill()

        task.apply_async.assert_not_called()
        self.assertEqual(result["skipped"], "not production")

    @override_settings(PRODUCTION=True)
    def test_dispatcher_schedules_with_jitter_in_production(self):
        with patch("socials_sharing.tasks.backfill_instagram_feed") as task:
            result = tasks.dispatch_instagram_backfill()

        task.apply_async.assert_called_once()
        self.assertLessEqual(result["scheduled_in_seconds"], 45 * 60)
