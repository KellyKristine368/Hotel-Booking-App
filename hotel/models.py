from django.db import models

# Create your models here.
class hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    hotel_description = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    image = image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    def __str__(self):
        return self.hotel_name
    