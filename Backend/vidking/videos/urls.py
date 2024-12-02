from django.urls import path
from .views import UploadVideoView, VideoListView, VideoDownloadView


urlpatterns = [
    path('upload/', UploadVideoView.as_view(), name='upload_video'),
    path('list/', VideoListView.as_view(), name='list_video'),
    path('download/<int:pk>/', VideoDownloadView.as_view(), name='download_video'),
]


