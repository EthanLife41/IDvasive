from django.db import models
from django.forms import fields
from .models import UploadImage
from django import forms


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['location', 'image']
