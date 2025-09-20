from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def home_view(request):
    return render(request, 'home.html')

# def edit_profile(request):
#     return render(request, "edit_profile.html")


def book_service(request, service_name):
    # service_name will be "3d-art", "mural", or "normal-paint"
    return render(request, 'book_service.html', {'service_name': service_name})


from django.shortcuts import render

def explore_service(request, service_type):
    """
    service_type: '3d-art', 'mural', 'normal-paint'
    """
    if service_type == '3d-art':
        images = [
            'gallery/art1.jpg', 'gallery/3d2.jpg', 'gallery/3d3.jpg',
            'gallery/3d4.jpg', 'gallery/3d5.jpg', 'gallery/3d6.jpg',
            'gallery/3d7.jpg', 'gallery/3d8.jpg', 'gallery/3d9.jpg',
        ]
        heading = "Our 3D Artworks"
    elif service_type == 'mural':
        images = [
            'gallery/mural1.jpg', 'gallery/mural2.jpg', 'gallery/mural3.jpg',
            'gallery/mural4.jpg', 'gallery/mural5.jpg', 'gallery/mural6.jpg',
        ]
        heading = "Our Mural Artworks"
    else:  # normal painting
        images = [
            'gallery/paint1.jpg', 'gallery/paint2.jpg', 'gallery/paint3.jpg',
            'gallery/paint4.jpg', 'gallery/paint5.jpg', 'gallery/paint6.jpg',
        ]
        heading = "Our Normal Paintings"

    context = {
        'images': images,
        'heading': heading,
    }
    return render(request, 'explore_service.html', context)



def book_service(request, service_type):
    """
    service_type: '3d-art', 'mural', 'normal-paint'
    """
    service_dict = {
        '3d-art': '3D Art',
        'mural': 'Mural Art',
        'normal-paint': 'Normal Painting'
    }
    service_name = service_dict.get(service_type, 'Service')

    if request.method == 'POST':
        # handle form submission
        pass

    return render(request, 'book_service.html', {'service_name': service_name})



def home(request):
    return render(request, 'home.html')

from django.shortcuts import render

def reviews(request):
    return render(request, 'reviews.html')



from django.contrib.auth import logout
from django.shortcuts import render, redirect

def logout_view(request):
    logout(request)
    return render(request, "accounts/login.html")


from django.shortcuts import render
from django.db.models import Q 
from accounts.models import Employee


def artists(request):
    query = Employee.objects.all()

    # Get filters
    name = request.GET.get("name")
    pin_code = request.GET.get("pin_code")
    address = request.GET.get("address")
    work_type = request.GET.get("work_type")
    experience_years = request.GET.get("experience_years")

    # Apply filters with correct field names
    if name:
        query = query.filter(full_name__icontains=name)
    if pin_code:
        query = query.filter(pincode__icontains=pin_code)
    if address:
        query = query.filter(
            village__icontains=address
        ) | query.filter(city__icontains=address) | query.filter(state__icontains=address)
    if work_type:
        query = query.filter(type_of_work__icontains=work_type)
    if experience_years:
        query = query.filter(experience__gte=experience_years)

    return render(request, "artist.html", {"artists": query})



from .models import Review
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Review

@csrf_exempt
@require_POST
def save_review(request):
    try:
        name = request.POST.get("name")
        email = request.POST.get("email")
        review_text = request.POST.get("customaer_review")
        rating = request.POST.get("rating")
        image = request.FILES.get("image")

        if not (name and email and rating):
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

        review = Review.objects.create(
            customer_id = str(uuid.uuid4()),
            customer_name=name,
            customer_email=email,
            customer_review=review_text,
            rating=rating,
            review_image=image
        )

        return JsonResponse({
            "success": True,
            "message": "Review submitted successfully!",
            "data": {
                "name": review.customer_name,
                "email": review.customer_email,
                "customer_review": review.customer_review,
                "rating": review.rating,
                "image": review.review_image.url if review.review_image else None,
                "created_at": review.review_date.strftime("%Y-%m-%d %H:%M"),
            }
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)




from .models import Booking

def bookings(request):
    all_bookings = Booking.objects.all().order_by('-created_at')  
    return render(request, 'bookings.html', {'bookings': all_bookings})


from django.http import JsonResponse
from .models import Booking
from accounts.models import Customer
from datetime import datetime
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
@login_required
@csrf_exempt
def save_booking(request):
    if request.method == 'POST':
        try:
            print("Logged-in user:", request.user, request.user.id)

            # Get the Customer record
            customer_qs = request.user.customers.all()
            if not customer_qs.exists():
                return JsonResponse({'success': False, 'message': 'This option is only available for customers.'})

            customer = customer_qs.first()  # the single Customer object

            booking_id = str(uuid.uuid4())[:8]

            appointment_date = None
            appointment_date_str = request.POST.get('appointment_date')
            if appointment_date_str:
                appointment_date = datetime.strptime(appointment_date_str, "%d-%m-%Y").date()

            booking = Booking.objects.create(
                booking_id=booking_id,
                customer_name=customer.customer_full_name,
                customer_user_id=customer.id,
                service_name=request.POST.get('service_name'),
                contact_number=request.POST.get('contact_number'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                pin_code=request.POST.get('pin_code'),
                state=request.POST.get('state'),
                city=request.POST.get('city'),
                total_walls=int(request.POST.get('total_walls', 0)),
                width=float(request.POST.get('width', 0)),
                height=float(request.POST.get('height', 0)),
                total_sqft=float(request.POST.get('total_sqft', 0)),
                appointment_date=appointment_date,
                payment_option="pending",
                payment_amount=0.00,
                is_paid=False
            )

            return JsonResponse({'success': True, 'message': 'Booking saved successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile_view(request):
    user = request.user

    if user.role == "employee":
        return render(request, "edit_profile.html", {"user": user})

    elif user.role == "customer":
        return render(request, "edit_customers_profile.html", {"user": user})

    # fallback (optional)
    return render(request, "edit_profile.html", {"user": user})
