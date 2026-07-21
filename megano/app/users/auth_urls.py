from django.urls import path

from app.users.views import SignInAPIView, SignOutAPIView, SignUpAPIView

app_name = "auth"

urlpatterns = [
    path("sign-in/", SignInAPIView.as_view(), name="sign-in"),
    path("sign-up/", SignUpAPIView.as_view(), name="sign-up"),
    path("sign-out/", SignOutAPIView.as_view(), name="sign-out"),
]
