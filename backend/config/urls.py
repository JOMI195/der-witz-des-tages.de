from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # general
    path("api/admin/", admin.site.urls),
    # path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("authentication.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # apps
    # path("api/", include("user_accounts.urls")),
    path("api/", include("jokes.urls")),
    path("api/", include("joke_newsletter.urls")),
    path("api/", include("contactMe.urls")),
    path("api/", include("workflows.urls")),
    path("api/", include("socials_sharing.urls")),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(
        path("api/schema/docs/", SpectacularAPIView.as_view(), name="schema")
    )
    urlpatterns.append(
        path("api/schema/", SpectacularSwaggerView.as_view(url_name="schema"))
    )
