from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    email =models.CharField(max_length=100)
