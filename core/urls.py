from django.contrib import admin
from django.urls import path, include
from apps.authentication.views import Error400TemplateView, Error403TemplateView, Error404TemplateView, Error500TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),                # Django admin route
    path("authentication/", include("apps.authentication.urls")),  # Auth routes - login / signup
    path("", include("apps.home.urls"))             # UI Kits Html files
]

handler404 = Error404TemplateView.as_view()
handler400 = Error400TemplateView.as_view()
handler403 = Error403TemplateView.as_view()
handler500 = Error500TemplateView.as_error_view()