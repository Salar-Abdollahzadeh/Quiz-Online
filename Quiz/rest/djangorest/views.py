from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Track, Album
from .serializers import AlbumListSerializer, AlbumDetailSerializer, \
    TrackListSerializer, TrackDetailSerializer, TrackModelListSerializer, \
TrackUpdateDetailSerializer, TrackViewsetSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import TrackFilter

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, \
    CursorPagination

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet


class AlbumViewSet(ReadOnlyModelViewSet):
    queryset = Album.objects.all().order_by('id')
    serializer_class = AlbumListSerializer


class TrackViewSet(ReadOnlyModelViewSet):
    queryset = Track.objects.all().order_by('album', 'id')
    # serializer_class = TrackViewsetSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TrackListSerializer
        elif self.action == 'retrieve':
            return TrackDetailSerializer


class CustomizeCursorPagination(CursorPagination):
    page_size = 5


class CustomizeLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5


class CustomizePagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'


# Create your views here.
class TrackListView(ListCreateAPIView):
    pagination_class = CustomizeCursorPagination
    queryset = Track.objects.all()
    serializer_class = TrackModelListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ['name', 'singers__first_name']
    ordering_fields = ['album', 'id']
    ordering = ['name']
    # filterset_fields = ['active', 'name']
    filterset_class = TrackFilter
    # def get_queryset(self):
    #     request_params = self.request.query_params
    #     queryset = Track.objects.all().order_by('album', 'id')
    #     print(queryset)
    #     active = request_params.get('active')
    #     if active:
    #         queryset = queryset.filter(active=active)
    #     name = request_params.get('name')
    #     if name:
    #         queryset = queryset.filter(name__icontains=name)
    #
    #     return queryset


class TrackDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all().order_by('album', 'id')
    # serializer_class = TrackDetailSerializer
    serializer_class = TrackUpdateDetailSerializer


class AlbumListView(ListCreateAPIView):
    queryset = Album.objects.all().order_by('id')
    serializer_class = AlbumListSerializer


class AlbumDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all().order_by('id')
    serializer_class = AlbumDetailSerializer
