from django.db import models
from account.models import UserFiles


class Video(models.Model):
    

    """
    Video model representing a video file uploaded by a user.
    Attributes:
        user_file (OneToOneField): A one-to-one relationship to the UserFiles model, with cascade delete.
        title (CharField): The title of the video, with a maximum length of 255 characters.
        description (TextField): An optional description of the video.
        uploaded_at (DateTimeField): The date and time when the video was uploaded, automatically set to the current date and time.
    Methods:
        __str__(): Returns the title of the video.
    """
    
    user_file = models.OneToOneField(UserFiles, on_delete=models.CASCADE, related_name='video_details')
    
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
    
    
