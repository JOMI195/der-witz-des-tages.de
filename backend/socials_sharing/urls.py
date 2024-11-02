from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SocialsSharingViewSet

router = DefaultRouter()
router.register(r"socials_sharing", SocialsSharingViewSet, basename="socials_sharing")

urlpatterns = [
    path("", include(router.urls)),
]
