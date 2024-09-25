from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('register', views.UserRagistrationViewSet, basename='register')


app_name = 'auth'
urlpatterns = router.urls
