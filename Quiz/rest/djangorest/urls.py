from django.urls import path, include
from .views import AlbumListView, AlbumDetailView, \
    TrackListView, TrackDetailView, TrackViewSet, AlbumViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

# default_router = DefaultRouter()
# default_router.register('track-viewset', TrackViewSet)

simple_router = SimpleRouter()
simple_router.register('track', TrackViewSet)
simple_router.register('album', AlbumViewSet)

urlpatterns = [
    path('album-list/', AlbumListView.as_view(), name='album-list'),
    path('album-detail/<int:pk>/',
         AlbumDetailView.as_view(),
         name='album-detail'),
    path('track-list/', TrackListView.as_view(), name='track-list'),
    path('track-detail/<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    # path('', include(default_router.urls)),
    # path('', include(simple_router.urls))
]

urlpatterns += simple_router.urls
