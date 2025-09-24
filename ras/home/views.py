from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
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
            'gallery/3d15.jpg', 'gallery/3d2.jpg', 'gallery/3d3.jpg',
            'gallery/3d4.jpg', 'gallery/3d5.jpg', 'gallery/3d6.jpg',
            'gallery/3d7.jpg', 'gallery/3d8.jpg', 'gallery/3d9.jpg',
            'gallery/3d10.jpg', 'gallery/3d11.jpg', 'gallery/3d12.jpg',
            'gallery/3d13.jpg', 'gallery/3d14.jpg', 'gallery/3d15.jpg',
            'gallery/3d18.jpg', 'gallery/3d19.jpg', 'gallery/3d20.jpg',
            'gallery/3d16.jpg', 'gallery/3d17.jpg', 'gallery/3d21.jpg',
            'gallery/3d22.jpg', 'gallery/3d23.jpg', 'gallery/3d24.jpg',
            'gallery/3d25.jpg', 'gallery/3d26.jpg', 'gallery/3d27.jpg',
            'gallery/3d28.jpg', 'gallery/3d29.jpg', 'gallery/3d30.jpg',
            'gallery/3d31.jpg', 'gallery/3d32.jpg', 'gallery/3d33.jpg',
        ]
        heading = "Our 3D Artworks"
    elif service_type == 'mural':
        images = [
            'gallery/mural2.jpg', 'gallery/mural3.jpg',
            'gallery/mural4.jpg', 'gallery/mural5.jpg', 'gallery/mural6.jpg',
            'gallery/mural20.jpg', 'gallery/mural8.jpg', 'gallery/mural9.jpg',
            'gallery/mural10.jpg', 'gallery/mural11.jpg', 'gallery/mural12.jpg',
            'gallery/mural13.jpg', 'gallery/mural14.jpg', 'gallery/mural15.jpg',
            'gallery/mural18.jpg', 'gallery/mural19.jpg', 'gallery/mural20.jpg',
            'gallery/mural16.jpg', 'gallery/mural17.jpg', 'gallery/mural18.jpg',
            'gallery/mural19.jpg', 'gallery/mural20.jpg', 'gallery/mural21.jpg',
            'gallery/mural22.jpg', 'gallery/mural23.jpg', 'gallery/mural24.jpg',
            'gallery/mural25.jpg', 'gallery/mural26.jpg', 'gallery/mural27.jpg',
            'gallery/mural28.jpg', 'gallery/mural29.jpg', 'gallery/mural30.jpg',
            'gallery/mural31.jpg', 'gallery/mural32.jpg', 'gallery/mural33.jpg',    
        ]
        heading = "Our Mural Artworks"
    else:  # normal painting
        images = [
            'gallery/paint1.jpg', 'gallery/paint2.jpg', 'gallery/paint3.jpg',
            'gallery/paint4.jpg', 'gallery/paint5.jpg', 'gallery/paint6.jpg',
            'gallery/paint7.jpg', 'gallery/paint8.jpg', 'gallery/paint9.jpg',
            'gallery/paint10.jpg', 'gallery/paint11.jpg', 'gallery/paint12.jpg',
            'gallery/paint15.jpg', 'gallery/paint14.jpg', 'gallery/paint13.jpg',
            'gallery/paint16.jpg','gallery/paint17.jpg', 'gallery/paint18.jpg',
            'gallery/paint19.jpg', 
        ]
        heading = "Advertisement Paintings"

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

    # Apply filters with Q objects
    if name:
        query = query.filter(full_name__icontains=name)
    if pin_code:
        query = query.filter(pincode__icontains=pin_code)
    if address:
        query = query.filter(
            Q(village__icontains=address) |
            Q(city__icontains=address) |
            Q(state__icontains=address)
        )
    if work_type:
        query = query.filter(type_of_work__icontains=work_type)
    if experience_years:
        try:
            experience_years = int(experience_years)
            query = query.filter(experience__gte=experience_years)
        except ValueError:
            pass  # ignore invalid input

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
        review_text = request.POST.get("customer_review") 
        rating = request.POST.get("rating")
        image = request.FILES.get("image")

        if not (name and email and rating):
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)
        print("frw")
        review = Review.objects.create(
            # customer_id = str(uuid.uuid4()),
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

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Customer, Employee  # assuming you have Employee model

@login_required
def edit_profile_view(request):
    user = request.user
    if user.role == "employee":
        employee = get_object_or_404(Employee, user=user)

        if request.method == "POST":
            employee.fathers_name = request.POST.get("fathers_name")
            employee.dob = request.POST.get("dob")
            employee.gender = request.POST.get("gender")
            employee.house_no = request.POST.get("house_no")
            employee.village = request.POST.get("village")
            employee.city = request.POST.get("city")
            employee.state = request.POST.get("state")
            employee.pincode = request.POST.get("pincode")
            employee.aadhar_card_no = request.POST.get("aadhar_card_no")
            employee.experience = request.POST.get("experience")
            employee.preferred_work_location = request.POST.get("preferred_work_location")
            employee.bank_account_holder_name = request.POST.get("bank_account_holder_name")
            employee.account_no = request.POST.get("account_no")
            employee.ifsc_code = request.POST.get("ifsc_code")

            # File fields
            if "passport_photo" in request.FILES:
                employee.passport_photo = request.FILES["passport_photo"]
            if "aadhar_card_image_front" in request.FILES:
                employee.aadhar_card_image_front = request.FILES["aadhar_card_image_front"]
            if "aadhar_card_image_back" in request.FILES:
                employee.aadhar_card_image_back = request.FILES["aadhar_card_image_back"]

            # Multi checkbox values (list)
            employee.type_of_work = request.POST.getlist("type_of_work")

            employee.save()
            return JsonResponse({"success": True, "message": "Profile updated successfully!"})
            


        context = {
            "name": employee.full_name,
            "email_address": employee.email_address,
            "contact": employee.mobile,
            "passport_photo": employee.passport_photo.url if employee.passport_photo else None,
            "fathers_name": employee.fathers_name,
            "dob": employee.dob,
            "gender": employee.gender,
            "house_no": employee.house_no,
            "village": employee.village,
            "city": employee.city,
            "state": employee.state,
            "pincode": employee.pincode,
            "aadhar_card_no": employee.aadhar_card_no,
            "aadhar_card_image_front": employee.aadhar_card_image_front.url if employee.aadhar_card_image_front else None,
            "aadhar_card_image_back": employee.aadhar_card_image_back.url if employee.aadhar_card_image_back else None,
            "experience": employee.experience,
            "type_of_work": employee.type_of_work or [],
            "preferred_work_location": employee.preferred_work_location,
            "bank_account_holder_name": employee.bank_account_holder_name,
            "account_no": employee.account_no,
            "ifsc_code": employee.ifsc_code,
        }
        return render(request, "edit_profile.html", context)

    elif user.role == "customer":
        customer = get_object_or_404(Customer, user=user)

        context = {
            "name": customer.customer_full_name,
            "email": customer.email,
            "contact": customer.mobile,
            "profile_pic": customer.customer_photo.url if customer.customer_photo else None,
        }
        return render(request, "edit_customers_profile.html", context)

    # fallback
    return render(request, "edit_profile.html", {"user": user})




def shop(request):
    # Example products
    products = [
        {"id": 1, "name": "Acrylic Paint Set", "price": 599, "image": "gallery/paint_set.jpg"},
        {"id": 2, "name": "Canvas Board", "price": 299, "image": "gallery/canvas.jpg"},
        {"id": 3, "name": "Brush Kit", "price": 399, "image": "gallery/brush_kit.jpg"},
        {"id": 4, "name": "Oil Pastels", "price": 199, "image": "gallery/pastels.jpg"},
    ]
    return render(request, "shop.html", {"products": products})

from django.shortcuts import render
from .models import Booking

def my_orders(request):
    if not request.user.is_authenticated or request.user.role != "customer":
        return render(request, "not_allowed.html")

    # Filter bookings based on the logged-in user's ID
    bookings = Booking.objects.filter(
        customer_user_id=request.user.id
    ).order_by('-created_at')

    return render(request, "my_orders.html", {"bookings": bookings})


# views.py

from django.shortcuts import render
from .models import Review 
from django.db.models import F

def home_view(request):
    # Fetch the top 3 latest reviews, ordered by review date
    reviews = Review.objects.all().order_by('-review_date')[:3]

    # Handle the case where there are not enough reviews
    reviews_list = list(reviews)
    
    # Create placeholder reviews if needed
    fake_reviews = []
    if len(reviews_list) < 3:
        if len(reviews_list) == 2:
            fake_reviews.append({
                'customer_name': 'A. Patel',
                'customer_review': 'Amazing service! The team was professional and the result was beyond my expectations.',
                'rating': 5,
                'review_image': None,
            })
        elif len(reviews_list) == 1:
            fake_reviews.extend([
                {
                    'customer_name': 'R. Sharma',
                    'customer_review': 'They made my living room look fantastic. Highly recommended!',
                    'rating': 5,
                    'review_image': None,
                },
                {
                    'customer_name': 'B. Singh',
                    'customer_review': 'The best painters I have ever hired. Punctual and very skilled.',
                    'rating': 5,
                    'review_image': None,
                }
            ])
        elif len(reviews_list) == 0:
            fake_reviews.extend([
                {
                    'customer_name': 'P. Reddy',
                    'customer_review': 'A true artist! The mural they painted for my cafe is a masterpiece.',
                    'rating': 5,
                    'review_image': None,
                },
                {
                    'customer_name': 'S. Kumar',
                    'customer_review': 'Excellent work and very easy to communicate with. Will definitely use their service again.',
                    'rating': 5,
                    'review_image': None,
                },
                {
                    'customer_name': 'M. Gupta',
                    'customer_review': 'The 3D art on my wall looks so real. It completely changed the feel of the room.',
                    'rating': 5,
                    'review_image': None,
                }
            ])
    
    # Combine real reviews and fake reviews to get a total of 3
    all_reviews = reviews_list + fake_reviews[:3 - len(reviews_list)]

    context = {
        'reviews': all_reviews,
        # ... other context variables for your page
    }
    return render(request, 'home.html', context)