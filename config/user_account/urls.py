from django.urls import path
from .views import *


urlpatterns = [
    path('profile-list/', ProfileListApiView.as_view()),
    path('info-profile/<int:pk>/', ProfileView.as_view()),
]
