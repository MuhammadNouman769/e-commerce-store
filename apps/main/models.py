from django.db import models
from apps.utilities.models import BaseModel


# Create your models here.
class Banners(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='banners/%Y/%m/%d')
    is_active = models.BooleanField(default=True)




