from django.shortcuts import render, redirect, get_object_or_404
from .models import hotel, Booking
from django.contrib import messages
from datetime import datetime
from django.db.models import Q


# Create your views here.
def home(request):
    hotels = hotel.objects.all()

    featured_hotels = hotels.order_by('-rating')[:3]  # Top-rated
    budget_hotels = hotels.order_by('hotel_price')[:3]  # Cheapest

    context = {
        'featured_hotels': featured_hotels,
        'budget_hotels': budget_hotels
    }
    return render(request, 'hotel/home.html', context)

def find_hotel(request):
    hotels = hotel.objects.all()

    # Search by name or location
    query = request.GET.get('query')
    if query:
        hotels = hotels.filter(
            Q(hotel_name__icontains=query) |
            Q(location__icontains=query)
        )

    # Sorting by price
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
        'query': query,
        'sort_by': sort_by_value,
        'amount': amount,
    }

    return render(request, 'hotel/find_hotel.html', context)

def hotel_detail(request, id):
    hotel_obj = get_object_or_404(hotel, id=id)

    # Default values
    available = True
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    # Check availability only if both dates are provided
    if check_in and check_out:
        start_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        end_date = datetime.strptime(check_out, "%Y-%m-%d").date()

        bookings = Booking.objects.filter(
            hotel=hotel_obj,
            check_out__gte=start_date,
            check_in__lte=end_date
        )

        if bookings.exists():
            available = False

    context = {
        "hotel": hotel_obj,
        "available": available,
        "check_in": check_in,
        "check_out": check_out,
    }
    return render(request, "hotel/hotel_detail.html", context)

def about(request):
    return render(request, "hotel/about.html")


def contact(request):
    return render(request, "hotel/contact.html")

def is_available(hotel, start_date, end_date):
    bookings = Booking.objects.filter(
        hotel=hotel,
        check_out__gte=start_date,
        check_in__lte=end_date
    )
    return not bookings.exists()

def book_hotel(request, hotel_id):
    hotel_obj = get_object_or_404(hotel, id=hotel_id)

    # Pre-fill dates from query parameters if they exist
    pre_check_in = request.GET.get('check_in', '')
    pre_check_out = request.GET.get('check_out', '')

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        # Convert string to date objects
        try:
            start_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            end_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid dates selected.")
            return render(request, "hotel/book_hotel.html", {
                "hotel": hotel_obj,
                "check_in": pre_check_in,
                "check_out": pre_check_out
            })

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            hotel=hotel_obj,
            check_out__gte=start_date,
            check_in__lte=end_date
        )

        if overlapping_bookings.exists():
            messages.error(request, "Sorry, this hotel is not available for the selected dates.")
        else:
            # Create booking
            booking = Booking.objects.create(
                hotel=hotel_obj,
                full_name=full_name,
                email=email,
                phone=phone,
                check_in=start_date,
                check_out=end_date
            )

            # Save booking info in session for confirmation page
            request.session["booking_info"] = {
                "hotel_name": hotel_obj.hotel_name,
                "hotel_image": hotel_obj.image.url,
                "hotel_location": hotel_obj.location,
                "hotel_price": hotel_obj.hotel_price,
                "hotel_rating": str(hotel_obj.rating),
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "check_in": check_in,
                "check_out": check_out,
            }

            return redirect("booking_success")

    context = {
        "hotel": hotel_obj,
        "check_in": pre_check_in,
        "check_out": pre_check_out,
    }

    return render(request, "hotel/book_hotel.html", context)

def is_available(hotel_obj, start_date, end_date):
    bookings = Booking.objects.filter(
        hotel=hotel_obj,
        check_out__gte=start_date,
        check_in__lte=end_date
    )
    return not bookings.exists()

def booking_success(request):
    # We can optionally pass booking details via session or context
    booking_info = request.session.get("booking_info", None)
    return render(request, "hotel/booking_success.html", {"booking": booking_info})