from django.urls import path
from .views import *
from rest_framework import routers
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('posts', PostListCreateApiView, basename='posts')
router.register('likes', LikeViewSet, basename='likes')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('update', UpdatePostViewSet, basename='post_update')


app_name = 'home'
urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentCreateListApiView.as_view()),
    path('posts/<int:post_id>/update-comment/<int:pk>/', CommentDetailUpdateApiView.as_view()),
    path('post/<int:pk>/share/', SharedPostApiView.as_view(), name='share_post'),
]

urlpatterns += router.urls + post_router.urls

