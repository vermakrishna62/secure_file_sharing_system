
from django.urls import path

from .views import get_csrf_token,user_login,upload_file,signup,verify_email,download_file,list_uploaded_files

urlpatterns = [
    path("get-token/",get_csrf_token),
    path("login/",user_login),
    path("upload/",upload_file),
    path("signup/",signup),
    path("verify-email/<str:uidb64>/<str:token>",verify_email,name='verify-email'),
    path('download-file/<int:file_id>/', download_file, name='download-file'),
    path("list-uploaded-files/",list_uploaded_files)
]
