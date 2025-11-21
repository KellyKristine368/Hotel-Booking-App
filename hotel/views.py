from django.shortcuts import render, get_object_or_404
from .models import hotel

# Create your views here.
def home(request):
    hotels = hotel.objects.all()
    context = {
        'hotels' : hotels
    }
    return render(request, 'hotel/home.html', context)

def find_hotel(request):
    hotels = hotel.objects.all()

    # Sorting
    sort_by_value = request.GET.get('sort_by')
    if sort_by_value == 'asc':
        hotels = hotels.order_by('hotel_price')
    elif sort_by_value == 'dsc':
        hotels = hotels.order_by('-hotel_price')

    # Filtering by budget
    amount = request.GET.get('amount')
    if amount:
        hotels = hotels.filter(hotel_price__lte=amount)

    context = {
        'hotels': hotels,
        'sort_by': sort_by_value,
        'amount': amount,
    }

    return render(request, 'hotel/find_hotel.html', context)
 
def hotel_detail(request, id):
    hotel_obj = get_object_or_404(hotel, id=id)
    return render(request, "hotel/hotel_detail.html", {"hotel": hotel_obj})

def about(request):
    return render(request, "hotel/about.html")


def contact(request):
    return render(request, "hotel/contact.html")