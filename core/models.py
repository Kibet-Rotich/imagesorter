from django.db import models
import os
import uuid

def image_upload_path(instance, filename):
    # Save to media/sessions/<session_id>/<filename>
    return os.path.join('sessions', str(instance.session.id), filename)

class UploadSession(models.Model):
    """Tracks a user's upload session"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class_names = models.TextField(help_text="Comma-separated class labels")
    is_completed = models.BooleanField(default=False)

    def get_class_list(self):
        return [cls.strip() for cls in self.class_names.split(',')]

    def __str__(self):
        return f"Session {self.id} ({self.created_at.date()})"


class UploadedImage(models.Model):
    """Stores each uploaded image"""
    session = models.ForeignKey(UploadSession, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.image.name)

    def __str__(self):
        return f"Image {self.id} from Session {self.session.id}"


class LabeledImage(models.Model):
    """Stores the label assignment for an uploaded image"""
    image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name='label')
    label = models.CharField(max_length=255)
    labeled_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.label} -> {self.image.filename()}"
