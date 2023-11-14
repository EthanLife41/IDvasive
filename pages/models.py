from django.db import models

class UploadImage(models.Model):
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')


