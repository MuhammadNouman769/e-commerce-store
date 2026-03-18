from django.db import models
from apps.utilities.models import BaseModel
from apps.users.models import User
from cities_light.models import Country, Region, City


class Address(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.street