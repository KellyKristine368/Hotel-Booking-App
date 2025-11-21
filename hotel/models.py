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
    
class Booking(models.Model):
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} → {self.hotel.hotel_name}"

    class Meta:
        ordering = ['-created_at']

