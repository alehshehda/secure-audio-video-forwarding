from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from api.views import UploadFilesView, FilesListView, FilesDownloadView, FilesDeleteView

urlpatterns = [
    path('video/upload/', UploadFilesView.as_view(), name='upload'),
    path('video/list/', FilesListView.as_view(), name='list'),
    path('video/download/<int:pk>/', FilesDownloadView.as_view(), name='download'),
    path('video/delete/<int:pk>/', FilesDeleteView.as_view(), name='delete'),
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
