from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsletterRecieverViewSet

# joke_newsletter_router = DefaultRouter()
# joke_newsletter_router.register(
#     r"joke-newsletter", JokeNewsletterViewSet, basename="joke_newsletter"
# )

newsletter_reciever_router = DefaultRouter()
newsletter_reciever_router.register(
    r"joke-newsletter/newsletter-reciever",
    NewsletterRecieverViewSet,
    basename="newsletter_reciever",
)

urlpatterns = [
    # path("", include(joke_newsletter_router.urls)),
    path("", include(newsletter_reciever_router.urls)),
]
