from django.urls import path

from app.users.views import ProfileAPIView, ProfileAvatarAPIView, ProfilePasswordAPIView

app_name = "users"

urlpatterns = [
    path("", ProfileAPIView.as_view(), name="profile"),
    path("password/", ProfilePasswordAPIView.as_view(), name="change_password"),
    path("avatar/", ProfileAvatarAPIView.as_view(), name="change_avatar"),
]
