from django.urls import path
from .views import ContactMeView

urlpatterns = [
    path("contactMe/", ContactMeView.as_view(), name="contact"),
]
