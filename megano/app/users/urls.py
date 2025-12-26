from django.urls import path

from .views import ProfileAPIView, ProfilePasswordAPIView, ProfileAvatarAPIView


app_name = "users"

urlpatterns = [
    path("", ProfileAPIView.as_view(), name="profile"),
    path("password/", ProfilePasswordAPIView.as_view(), name="change_password"),
    path("avatar/", ProfileAvatarAPIView.as_view(), name="change_avatar"),
]