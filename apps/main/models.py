from django.db import models
from apps.utilities.models import BaseModel


# Create your models here.
class Banners(BaseModel):
    image = models.ImageField(upload_to='banners/%Y/%m/%d')
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title



