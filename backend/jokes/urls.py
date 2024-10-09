from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JokeViewSet

router = DefaultRouter()
router.register(r"jokes", JokeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
