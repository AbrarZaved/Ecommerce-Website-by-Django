from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("sign_out", views.sign_out, name="sign_out"),
    path("profile", views.profile_view, name="profile"),
    path("delete_address/<int:boom>", views.delete_address, name="delete_address"),
    path("profile_attributes", views.profile_attributes, name="profile_attributes"),
    path("sign_in", csrf_exempt(views.sign_in), name="sign_in"),
    path("sign_up", csrf_exempt(views.sign_up), name="sign_up"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
