from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('send-email/', views.send_email, name='send_email'),
    ]