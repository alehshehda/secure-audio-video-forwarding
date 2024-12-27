import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

# Ensure that the media directory exists
def ensure_media_directory_exists(path):
    """Ensures the directory exists where the file will be stored."""
    if not os.path.exists(path):
        os.makedirs(path)

def dynamic_upload_path(instance, filename):
    """
    Determines the upload path dynamically based on the user ID and file extension.
    Files are saved in: /media/user_id/extension/filename.
    """
    # Get file extension
    file_extension = filename.split('.')[-1]  # Get the file extension from the filename
    user_id = instance.user.id  # Get the user's ID

    # Construct the file path based on user_id and file_extension
    upload_path = os.path.join(str(user_id), file_extension, filename)

    # Ensure the directory exists
    ensure_media_directory_exists(os.path.join(settings.MEDIA_ROOT, str(user_id), file_extension))

    return upload_path

class UserFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=dynamic_upload_path)  # Save file based on dynamic path
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_type = models.CharField(max_length=50, blank=True, null=True)  # Optional field for file type (extension)

    def save(self, *args, **kwargs):
        # Set the file type based on the file extension
        if not self.file_type and self.file:
            self.file_type = self.file.name.split('.')[-1]  # Get the file extension from the filename

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} uploaded {self.file.name} on {self.uploaded_at}"

    from django.conf import settings
    import os

    def delete_file(file_path):
        try:
            # Check if file exists
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
            else:
                print(f"File not found at {full_path}")
                return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False


