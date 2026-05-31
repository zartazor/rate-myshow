from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.core.urls")),
    path("titles/", include("apps.titles.urls")),
    path("ratings/", include("apps.ratings.urls")),
    path("users/", include("apps.users.urls")),
    path("recommendations/", include("apps.recommendations.urls")),
]

handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
