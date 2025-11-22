from django.shortcuts import render

# Create your views here.
import random, re
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser, Customer


@csrf_exempt
def save_customer_signup_api(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('customer_full_name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            create_password = request.POST.get('customer_password')

            if not all([full_name, mobile, email, create_password]):
                return JsonResponse({'success': False, 'error': 'All fields are required'})

            # Email validation
            email_regex = r'^[^@\s]+@[^\s@]+\.[^@\s]+$'
            if not re.match(email_regex, email):
                return JsonResponse({'success': False, 'error': 'Invalid email format'})

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Save in session temporarily
            request.session['signup_data'] = {
                'customer_full_name': full_name,
                'mobile': mobile,
                'email': email,
                'customer_password': create_password,
            }
            request.session['otp'] = otp

            # Send OTP email
            send_mail(
                subject="Your Painting App OTP",
                message=f"Hello {full_name},\n\nYour OTP is: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'OTP sent to your email!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def verify_customer_otp_api(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_saved = request.session.get('otp')
        signup_data = request.session.get('signup_data')

        if otp_saved and signup_data and otp_entered == otp_saved:
            # Save user & customer after OTP verification
            user = CustomUser.objects.create_user(
                email=signup_data['email'],
                password=signup_data['customer_password'],
                full_name=signup_data['customer_full_name'],
                role='customer',
                is_verified=True
            )

            Customer.objects.create(
                customer_full_name=signup_data['customer_full_name'],
                user=user,
                mobile=signup_data['mobile'],
                email=signup_data['email'],
                customer_password=signup_data['customer_password'],
                is_verified=True
            )

            # Clear session
            del request.session['otp']
            del request.session['signup_data']

            return JsonResponse({'success': True, 'message': 'Email verified & customer registered!'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid OTP'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


import random, re
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from accounts.models import CustomUser, Employee


@csrf_exempt
def save_employee_signup_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    try:
        email = request.POST.get('email_address')
        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile', '')

        if not all([email, full_name]):
            return JsonResponse({'success': False, 'error': 'Email and full name are required'})

        # Validate email
        email_regex = r'^[^@\s]+@[^\s@]+\.[^@\s]+$'
        if not re.match(email_regex, email):
            return JsonResponse({'success': False, 'error': 'Invalid email format'})

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Save form fields in session
        signup_data = {
            'full_name': full_name,
            'email_address': email,
            'mobile': mobile,
            'password': request.POST.get('password', 'defaultpass123')  # optional default password
        }
        request.session['employee_signup_data'] = signup_data
        request.session['employee_otp'] = otp

        # Send OTP via email
        send_mail(
            subject="Your Painting Employee Signup OTP",
            message=f"Hello {full_name},\n\nYour OTP is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'success': True, 'message': 'OTP sent to your email!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def verify_employee_otp_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    try:
        otp_entered = request.POST.get('otp')
        otp_saved = request.session.get('employee_otp')
        signup_data = request.session.get('employee_signup_data')

        # ✅ OTP validation
        if not (otp_entered and otp_saved and otp_entered.strip() == str(otp_saved).strip()):
            return JsonResponse({'success': False, 'error': 'Invalid OTP'})

        if not signup_data:
            return JsonResponse({'success': False, 'error': 'Signup data missing in session'})

        # Database operations inside transaction
        with transaction.atomic():
            if CustomUser.objects.filter(email=signup_data['email_address']).exists():
                return JsonResponse({'success': False, 'error': 'Email already registered'})

            # 1. Create user
            user = CustomUser.objects.create_user(
                email=signup_data['email_address'],
                password=signup_data['password'],
                full_name=signup_data['full_name'],
                role="employee",
                is_verified=True
            )

            # 2. Create employee profile
            Employee.objects.create(
                user=user,
                full_name=signup_data['full_name'],
                mobile=signup_data.get('mobile', ''),
                email_address=signup_data['email_address'],
            )

        # Clear session after success
        for key in ['employee_otp', 'employee_signup_data']:
            request.session.pop(key, None)

        return JsonResponse({'success': True, 'message': 'Employee registered successfully!'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login


@csrf_exempt
def login_api(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"})

    try:
        # Parse JSON data from Flutter
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return JsonResponse({"success": False, "error": "Email and password are required"})

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse({"success": False, "error": "Invalid email or password"})

        if not user.is_verified:
            return JsonResponse({"success": False, "error": "Email not verified yet!"})

        # Log the user in and save session
        login(request, user)

        # Optional: return basic user info
        user_data = {
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        }

        return JsonResponse({"success": True, "user": user_data})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from employee.models import ServiceImage
from .serializers import ServiceImageSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def explore_service_api(request, service_type):

    service_dict = {
        '3d-wall-art': '3D Wall Art',
        '3d-floor-art': '3D Floor Art',
        'mural-art': 'Mural Art',
        'mural': 'Mural Art',
        'metro-advertisement': 'Metro Advertisement',
        'outdoor-advertisement': 'Outdoor Advertisement',
        'school-painting': 'School Painting',
        'selfie-painting': 'Selfie Painting',
        'madhubani-painting': 'Madhubani Painting',
        'texture-painting': 'Texture Painting',
        'stone-murti': 'Stone Murti',
        'statue': 'Statue',
        'scrap-animal-art': 'Scrap Animal Art',
        'nature-fountain': 'Nature & Water Fountain',
        'fountain-art': 'Nature & Water Fountain',
        'cartoon-painting': 'Cartoon Painting',
        'home-painting': 'Home Painting',
    }

    service_name = service_dict.get(service_type, 'Service')
    query_term = service_name

    # special cases
    if service_name == 'Mural Art':
        query_term = 'Mural'
    elif service_name == 'Nature & Water Fountain':
        query_term = 'Fountain'

    # 🔥 Same filtering logic as original view
    if request.user.is_authenticated and request.user.is_staff:
        db_images = ServiceImage.objects.filter(type_of_art__icontains=query_term)

    elif request.user.is_authenticated:
        db_images = ServiceImage.objects.filter(
            type_of_art__icontains=query_term
        ).filter(
            Q(is_verified_pic=True) | Q(userupload_id=request.user.id)
        )

    else:
        db_images = ServiceImage.objects.filter(
            type_of_art__icontains=query_term,
            is_verified_pic=True
        )

    serializer = ServiceImageSerializer(db_images, many=True)

    return Response({
        "service_name": service_name,
        "service_slug": service_type,
        "images": serializer.data
    })


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from home.models import Booking

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_booking_api(request):
    data = request.data
    try:
        # Required fields validation
        required = ["service_name", "contact_number", "email", "address", "pin_code",
                    "state", "city", "total_walls", "width", "height",
                    "total_sqft", "appointment_date", "total_amount"]
        for field in required:
            if not data.get(field):
                return Response({"success": False, "message": f"{field} is required"}, status=400)

        # Date format fix
        appointment = data.get("appointment_date")
        try:
            appointment_date = datetime.strptime(appointment, "%d-%m-%Y").date()
        except:
            appointment_date = datetime.strptime(appointment, "%Y-%m-%d").date()

        next_id = Booking.objects.count() + 1
        booking_id = f"RCC{next_id}"

        design_name = data.get("selected_design_name")
        design_price = float(data.get("selected_design_price")) if data.get("selected_design_price") else None
        custom_design_file = request.FILES.get("custom_design")

        if design_name:
            art_type = "Selected Design"
        elif custom_design_file:
            art_type = "Custom Upload"
            design_price = design_price if design_price else 0
        else:
            art_type = "Standard Service"

        booking = Booking.objects.create(
            customer_name=request.user.full_name or request.user.email,
            customer_user_id=request.user.id,
            booking_id=booking_id,
            service_name=data.get("service_name"),
            contact_number=data.get("contact_number"),
            email=data.get("email"),
            address=data.get("address"),
            pin_code=data.get("pin_code"),
            state=data.get("state"),
            city=data.get("city"),
            total_walls=data.get("total_walls"),
            width=data.get("width"),
            height=data.get("height"),
            total_sqft=data.get("total_sqft"),
            appointment_date=appointment_date,
            design_names=design_name,
            type_of_art_booked=art_type,
            price_of_design=design_price,
            customer_design=custom_design_file,
            total_amount=data.get("total_amount")
        )

        # Email trigger (optional)
        try:
            send_mail(
                f"Booking Confirmation - {booking.booking_id}",
                f"Dear {booking.customer_name}, your booking {booking.booking_id} is confirmed.",
                settings.DEFAULT_FROM_EMAIL,
                [booking.email]
            )
        except Exception as e:
            print("Email Error", e)

        return Response({
            "success": True,
            "message": "Booking saved successfully",
            "booking": {
                "id": booking.id,
                "booking_id": booking.booking_id,
                "total_amount": booking.total_amount,
                "customer_name": booking.customer_name
            }
        }, status=200)

    except Exception as e:
        return Response({"success": False, "message": str(e)}, status=500)
