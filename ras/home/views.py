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
from employee.models import ServiceImage  # Make sure to import your model

def explore_service(request, service_type):
    """
    service_type: '3d-art', 'mural', 'normal-paint'
    """
    if service_type == '3d-art':
        heading = "Our 3D Artworks"
        art_type_filter = "3D"  # Match what you save in form
        
    elif service_type == 'mural':
        heading = "Our Mural Artworks"
        art_type_filter = "mural"  # Match what you save in form
        
    else:  # normal painting
        heading = "Advertisement Paintings"
        art_type_filter = "normal"  # Match what you save in form

    # Get database images for this service type
    db_images = ServiceImage.objects.filter(type_of_art__icontains=art_type_filter).order_by('-id')
    
    # Debug - let's see what we have
    print(f"Service type: {service_type}")
    print(f"Art type filter: {art_type_filter}")
    print(f"DB images found: {db_images.count()}")
    for img in db_images:
        print(f"- {img.image_name} ({img.type_of_art})")
    
    context = {
        'db_images': db_images,
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
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        # ✅ Ensure logged-in user is a customer
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return JsonResponse({"success": False, "error": "Only customers can submit reviews"}, status=403)

        name = request.POST.get("name")
        email = request.POST.get("email")
        review_text = request.POST.get("customer_review")
        rating = request.POST.get("rating")
        image = request.FILES.get("image")

        if not (name and email and rating):
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

        # ✅ Use logged-in customer id
        review = Review.objects.create(
            customer_id=customer.id,  
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
                "customer_id": customer.id,  
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
# @login_required
# @csrf_exempt
# def save_booking(request):
#     if request.method == 'POST':
#         try:
#             print("Logged-in user:", request.user, request.user.id)

#             # Get the Customer record
#             customer_qs = request.user.customers.all()
#             if not customer_qs.exists():
#                 return JsonResponse({'success': False, 'message': 'This option is only available for customers.'})

#             customer = customer_qs.first()  # the single Customer object

#             booking_id = str(uuid.uuid4())[:8]

#             appointment_date = None
#             appointment_date_str = request.POST.get('appointment_date')
#             if appointment_date_str:
#                 appointment_date = datetime.strptime(appointment_date_str, "%d-%m-%Y").date()

#             booking = Booking.objects.create(
#                 booking_id=booking_id,
#                 customer_name=customer.customer_full_name,
#                 customer_user_id=customer.id,
#                 service_name=request.POST.get('service_name'),
#                 contact_number=request.POST.get('contact_number'),
#                 email=request.POST.get('email'),
#                 address=request.POST.get('address'),
#                 pin_code=request.POST.get('pin_code'),
#                 state=request.POST.get('state'),
#                 city=request.POST.get('city'),
#                 total_walls=int(request.POST.get('total_walls', 0)),
#                 width=float(request.POST.get('width', 0)),
#                 height=float(request.POST.get('height', 0)),
#                 total_sqft=float(request.POST.get('total_sqft', 0)),
#                 appointment_date=appointment_date,
#                 payment_option="pending",
#                 payment_amount=0.00,
#                 is_paid=False
#             )

#             return JsonResponse({'success': True, 'message': 'Booking saved successfully!'})

#         except Exception as e:
#             return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


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
            employee.role = "employee"

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

        if request.method == "POST":
            customer.customer_full_name = request.POST.get("name")
            customer.email = request.POST.get("email")
            customer.mobile = request.POST.get("contact")

            # Handle profile picture
            if "customer_photo" in request.FILES:
                customer.customer_photo = request.FILES["customer_photo"]

            customer.save()
            return JsonResponse({"success": True, "message": "Profile updated successfully!"})

        context = {
            "name": customer.customer_full_name,
            "email": customer.email,
            "contact": customer.mobile,
            "profile_pic": customer.customer_photo.url if customer.customer_photo else None,
        }
        return render(request, "edit_customers_profile.html", context)

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
from .models import Review
from accounts.models import Customer

def home_view(request):
    reviews = Review.objects.all().order_by('-review_date')[:3]
    reviews_list = list(reviews)

    fake_reviews = [
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
    },
]
  # keep your same fake reviews

    all_reviews = reviews_list + fake_reviews[:3 - len(reviews_list)]

    enriched_reviews = []
    for r in all_reviews:
        if isinstance(r, dict):
            rating = r["rating"]
            r["full_stars"] = range(rating)
            r["empty_stars"] = range(5 - rating)
            r["customer_photo"] = None  # fake ones don’t have photos
            enriched_reviews.append(r)
        else:  
            rating = r.rating
            setattr(r, "full_stars", range(rating))
            setattr(r, "empty_stars", range(5 - rating))
            try:
                customer = Customer.objects.get(id=r.customer_id)
                setattr(r, "customer_photo", customer.customer_photo.url if customer.customer_photo else None)
            except Customer.DoesNotExist:
                setattr(r, "customer_photo", None)
            enriched_reviews.append(r)

    context = {
        "reviews": enriched_reviews,
    }
    return render(request, "home.html", context)




# views.py - Add these functions to your existing views.py

import razorpay
import time
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@require_http_methods(["POST"])
def create_razorpay_order(request):
    try:
        # Get amount from request (convert to paise - multiply by 100)
        amount_str = request.POST.get('amount', '0')
        amount = int(float(amount_str) * 100)  # Convert to paise
        
        # Create unique receipt ID
        receipt_id = f'booking_{int(time.time())}'
        
        # Create Razorpay order
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': receipt_id,
            'payment_capture': 1  # Auto capture payment
        }
        
        order = razorpay_client.order.create(data=order_data)
        
        return JsonResponse({
            'success': True,
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
            'key_id': settings.RAZORPAY_KEY_ID
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def verify_razorpay_payment(request):
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        # Extract payment details
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        # This will raise an exception if signature is invalid
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Payment is verified successfully
        # Here you can save payment details to your database
        # Example:
        # Payment.objects.create(
        #     order_id=razorpay_order_id,
        #     payment_id=razorpay_payment_id,
        #     signature=razorpay_signature,
        #     status='completed'
        # )
        
        return JsonResponse({
            'success': True,
            'message': 'Payment verified successfully',
            'payment_id': razorpay_payment_id
        })
        
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({
            'success': False,
            'error': 'Payment signature verification failed'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
    

# Add this to your views.py or update your existing save_bookings view

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def save_booking(request):
    try:
        # Get form data
        service_name = request.POST.get('service_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        state = request.POST.get('state')
        city = request.POST.get('city')
        total_walls = request.POST.get('total_walls')
        width = request.POST.get('width')
        height = request.POST.get('height')
        total_sqft = request.POST.get('total_sqft')
        appointment_date = request.POST.get('appointment_date')
        
        # Validate required fields
        required_fields = [service_name, contact_number, email, address, pin_code, 
                          state, city, total_walls, width, height, appointment_date]
        
        if not all(required_fields):
            return JsonResponse({
                'success': False,
                'message': 'Please fill all required fields'
            })
        
        # Save to database (replace with your model)
        # Example:
        # booking = Booking.objects.create(
        #     service_name=service_name,
        #     contact_number=contact_number,
        #     email=email,
        #     address=address,
        #     pin_code=pin_code,
        #     state=state,
        #     city=city,
        #     total_walls=total_walls,
        #     width=width,
        #     height=height,
        #     total_sqft=total_sqft,
        #     appointment_date=appointment_date
        # )
        
        # Store booking data in session for payment step
        request.session['booking_data'] = {
            'service_name': service_name,
            'contact_number': contact_number,
            'email': email,
            'address': address,
            'pin_code': pin_code,
            'state': state,
            'city': city,
            'total_walls': total_walls,
            'width': width,
            'height': height,
            'total_sqft': total_sqft,
            'appointment_date': appointment_date
        }
        
        return JsonResponse({
            'success': True,
            'message': 'Booking data saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error saving booking: {str(e)}'
        })