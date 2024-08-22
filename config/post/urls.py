from .views import *
from rest_framework import routers
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('posts', PostListCreateApiView, basename='posts')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('update', UpdatePostViewSet, basename='post_update')

urlpatterns = router.urls + post_router.urls
