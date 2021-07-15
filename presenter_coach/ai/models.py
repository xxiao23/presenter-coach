from django.db import models
from django_base64field.fields import Base64Field

# Create your models here.
class MediaBlob(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    data = Base64Field(max_length=10383360, blank=True, null=True) # Max 10MB

    class Meta:
        ordering = ['created']