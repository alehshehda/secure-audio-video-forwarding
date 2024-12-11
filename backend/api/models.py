from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import magic
import os

def ensure_media_directory_exists():
    # Sprawdza, czy folder 'media' istnieje
    media_path = settings.MEDIA_ROOT
    if not os.path.exists(media_path):
        os.makedirs(media_path)

class UserFiles(models.Model):
    # Powiązanie z użytkownikiem
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Przechowywanie samego pliku
    file = models.FileField(upload_to='uploads/')  # Zapis plików do folderu 'uploads/'

    # Zapisywanie czasu dodania pliku
    uploaded_at = models.DateTimeField(default=timezone.now)

    # Pole do przechowywania typu pliku
    file_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} uploaded {self.file.name} on {self.uploaded_at}"

    def save(self, *args, **kwargs):
        ensure_media_directory_exists()

        # Automatyczne przypisanie folderu na podstawie typu pliku
        if self.file:
            # Użycie python-magic do rozpoznania typu pliku
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(self.file.read(1024))  # Zaczytuje nagłówek pliku
            self.file.seek(0)  # Przywraca pozycję pliku do początku
            self.file_type = file_type  # Ustawiamy typ pliku

            # Określenie folderu użytkownika w zależności od typu pliku
            user_folder = str(self.user.id)

            if file_type.startswith('audio'):
                folder_path = f'{user_folder}/audio/'

            elif file_type.startswith('video'):
                folder_path = f'{user_folder}/video/'

            elif file_type == 'text/plain':
                folder_path = f'{user_folder}/text/'

            elif file_type == 'application/pdf':
                folder_path = f'{user_folder}/pdf/'

            else:
                folder_path = f'{user_folder}/other/'  # Domyślny folder na inne pliki

            # Sprawdzenie, czy folder istnieje, jeśli nie - tworzymy
            full_path = os.path.join(settings.MEDIA_ROOT, 'uploads', folder_path)
            os.makedirs(full_path, exist_ok=True)

            # Nadanie ścieżki pliku (relatywnej)
            self.file.name = os.path.join(folder_path, self.file.name)

        # Wywołanie metody save z rodzica, aby plik został zapisany
        super().save(*args, **kwargs)

