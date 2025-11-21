from django.contrib import admin
from .models import hotel

# Register your models here.
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'rating', 'is_featured')
    list_filter = ('is_featured', 'location')
    search_fields = ('name', 'location')
    
admin.site.register(hotel)