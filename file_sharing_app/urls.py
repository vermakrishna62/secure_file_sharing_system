
from django.urls import path

from .views import *

urlpatterns = [
    path("get-token/",get_csrf_token),
    path("login/",user_login),
    path("upload/",upload_file),
    path("signup/",signup),
    path("verify-email/<str:uidb64>/<str:token>",verify_email)
]
