from django.urls import path
from .views import FilesDeleteView, FilesDownloadView, FilesListView, UploadFilesView


urlpatterns = [
    path('video/upload/',UploadFilesView .as_view(), name='upload'),
    path('video/list/',FilesListView.as_view(), name='list'),
    path('video/download/<int:pk>/', FilesDownloadView.as_view(), name='download'),
    path('video/delete/<int:pk>/', FilesDeleteView.as_view(), name='delete'),
]
