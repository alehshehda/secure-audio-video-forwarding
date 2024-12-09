from django.urls import path
from .views import UploadVideoView, VideoListView, VideoDownloadView, VideoDeleteView


urlpatterns = [
    path('video/upload/', UploadVideoView.as_view(), name='upload'),
    path('video/list/', VideoListView.as_view(), name='list'),
    path('video/download/<int:pk>/', VideoDownloadView.as_view(), name='download'),
    path('video/delete/<int:pk>/', VideoDeleteView.as_view(), name='delete'),
]
