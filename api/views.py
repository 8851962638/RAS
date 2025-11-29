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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from wallet.models import Wallet, WalletTransaction

import razorpay
import json
import time
from decimal import Decimal

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@csrf_exempt
def api_create_order(request):
    """REST API → Create Razorpay wallet recharge order"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST method required"})

    try:
        body = json.loads(request.body)
        amount = int(float(body.get("amount", 0)) * 100)

        if amount < 100:
            return JsonResponse({"success": False, "error": "Minimum amount is ₹1"})

        receipt_id = f"wallet_{int(time.time())}"

        order_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": receipt_id,
            "payment_capture": 1
        }

        order = razorpay_client.order.create(order_data)

        return JsonResponse({
            "success": True,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": settings.RAZORPAY_KEY_ID,
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    


@csrf_exempt
def api_verify_payment(request):
    """REST API → Verify payment and credit wallet"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST method required"})

    try:
        body = json.loads(request.body)

        user_id = body.get("user_id")
        if not user_id:
            return JsonResponse({"success": False, "error": "user_id required"})

        user = User.objects.get(id=user_id)

        razorpay_order_id = body.get("razorpay_order_id")
        razorpay_payment_id = body.get("razorpay_payment_id")
        razorpay_signature = body.get("razorpay_signature")
        amount = Decimal(str(body.get("amount")))

        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }

        # verify payment signature
        razorpay_client.utility.verify_payment_signature(params_dict)

        # credit wallet
        wallet, _ = Wallet.objects.get_or_create(user=user)
        wallet.credit(amount)

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type="CREDIT",
            razorpay_payment_id=razorpay_payment_id
        )

        return JsonResponse({"success": True, "message": "Wallet credited successfully"})

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"success": False, "error": "Signature verification failed"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404

from wallet.models import Wallet, WalletTransaction
from accounts.models import Employee, Customer

import time
import json
from decimal import Decimal


# =============== CUSTOMER PROFILE ===============
@csrf_exempt
def api_get_customer_profile(request):
    if request.method != "GET":
        return JsonResponse({"success": False, "error": "GET method required"})

    user = request.user
    if not user.is_authenticated or user.role != "customer":
        return JsonResponse({"success": False, "error": "Unauthorized"})

    customer = Customer.objects.get(user=user)

    return JsonResponse({
        "success": True,
        "data": {
            "name": customer.customer_full_name,
            "email": customer.email,
            "mobile": customer.mobile,
            "profile_photo": customer.customer_photo.url if customer.customer_photo else None
        }
    })


@csrf_exempt
def api_update_customer_profile(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"})

    user = request.user
    if not user.is_authenticated or user.role != "customer":
        return JsonResponse({"success": False, "error": "Unauthorized"})

    customer = Customer.objects.get(user=user)

    customer.customer_full_name = request.POST.get("name")
    customer.email = request.POST.get("email")
    customer.mobile = request.POST.get("mobile")

    if "profile_photo" in request.FILES:
        customer.customer_photo = request.FILES["profile_photo"]

    customer.save()

    return JsonResponse({"success": True, "message": "Profile updated successfully"})


# =============== EMPLOYEE PROFILE ===============
@csrf_exempt
def api_get_employee_profile(request):
    if request.method != "GET":
        return JsonResponse({"success": False, "error": "GET method required"})

    user = request.user
    if not user.is_authenticated or user.role != "employee":
        return JsonResponse({"success": False, "error": "Unauthorized"})

    employee = Employee.objects.get(user=user)

    return JsonResponse({
        "success": True,
        "data": {
            "father_name": employee.fathers_name,
            "dob": str(employee.dob),
            "gender": employee.gender,
            "house_no": employee.house_no,
            "village": employee.village,
            "city": employee.city,
            "state": employee.state,
            "pincode": employee.pincode,
            "aadhar_card_no": employee.aadhar_card_no,
            "experience": employee.experience,
            "preferred_work_location": employee.preferred_work_location,
            "type_of_work": employee.type_of_work,
            "ready_to_take_orders": employee.status,
            "passport_photo": employee.passport_photo.url if employee.passport_photo else None,
            "aadhar_front": employee.aadhar_card_image_front.url if employee.aadhar_card_image_front else None,
            "aadhar_back": employee.aadhar_card_image_back.url if employee.aadhar_card_image_back else None,
        }
    })


@csrf_exempt
def api_update_employee_profile(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"})

    user = request.user
    if not user.is_authenticated or user.role != "employee":
        return JsonResponse({"success": False, "error": "Unauthorized"})

    employee = Employee.objects.get(user=user)
    prev_status = employee.status

    # Basic fields
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

    # Multi-Select
    employee.type_of_work = request.POST.getlist("type_of_work")
    employee.preferred_work_location = ", ".join(request.POST.getlist("preferred_work_location"))

    # Files
    if "passport_photo" in request.FILES:
        employee.passport_photo = request.FILES["passport_photo"]

    if "aadhar_front" in request.FILES:
        employee.aadhar_card_image_front = request.FILES["aadhar_front"]

    if "aadhar_back" in request.FILES:
        employee.aadhar_card_image_back = request.FILES["aadhar_back"]

    # Banking + org fields
    employee.bank_account_holder_name = request.POST.get("bank_account_holder_name")
    employee.account_no = request.POST.get("account_no")
    employee.ifsc_code = request.POST.get("ifsc_code")
    employee.pan_card = request.POST.get("pan_card")
    employee.gst_no = request.POST.get("gst_no")
    employee.organization_name = request.POST.get("organization_name")

    # Ready to take orders
    is_ready = request.POST.get("ready_to_take_orders") == "true"

    # Deduct ₹20 only ONCE
    if not prev_status and is_ready:
        wallet = Wallet.objects.filter(user=user).first()

        if wallet and wallet.balance >= Decimal("20.00"):
            wallet.balance -= Decimal("20.00")
            wallet.save()

            WalletTransaction.objects.create(
                wallet=wallet,
                transaction_type="DEBIT",
                amount=Decimal("20.00"),
                razorpay_payment_id=f"ACTIVATION_{user.id}_{int(time.time())}"
            )

            employee.status = True
        else:
            employee.status = False
            employee.save()
            return JsonResponse({"success": False, "message": "Insufficient wallet balance"})

    else:
        employee.status = is_ready

    employee.save()

    return JsonResponse({"success": True, "message": "Employee profile updated successfully"})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from accounts.models import CustomUser
from home.models import CustomProduct


@csrf_exempt
def api_save_custom_product(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"})

    try:
        data = json.loads(request.body)

        user_id = data.get("user_id")  # Flutter must send this
        user = CustomUser.objects.get(id=user_id)

        CustomProduct.objects.create(
            user=user,
            name=data.get("product_name"),
            size=data.get("size"),
            material=data.get("material"),
            other_material=data.get("other_material"),
            message=data.get("message"),
        )

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



# API IMPORTS
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.db.models import Q
from home.models import Booking
from employee.models import ServiceImage
from .serializers import ServiceImageSerializer # Assuming serializer is in current directory

# SESSION CHECK API
@csrf_exempt
def session_status_api(request):
    """Returns whether the current user session is active."""
    if request.user.is_authenticated:
        return JsonResponse({
            "success": True,
            "is_logged_in": True,
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "full_name": request.user.full_name,
                "role": request.user.role,
            }
        })
    return JsonResponse({"success": True, "is_logged_in": False})

# LOGOUT API
@csrf_exempt
def logout_api(request):
    logout(request)
    return JsonResponse({"success": True, "message": "Logged out successfully"})

# SAVE BOOKING API
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

# EXPLORE SERVICE API
@api_view(['GET'])
@permission_classes([AllowAny])
def explore_service_api(request, service_type):
    service_dict = {
        '3d-wall-art': '3D Wall Art', '3d-floor-art': '3D Floor Art', 'mural-art': 'Mural Art',
        'mural': 'Mural Art', 'metro-advertisement': 'Metro Advertisement',
        'outdoor-advertisement': 'Outdoor Advertisement', 'school-painting': 'School Painting',
        'selfie-painting': 'Selfie Painting', 'madhubani-painting': 'Madhubani Painting',
        'texture-painting': 'Texture Painting', 'stone-murti': 'Stone Murti', 'statue': 'Statue',
        'scrap-animal-art': 'Scrap Animal Art', 'nature-fountain': 'Nature & Water Fountain',
        'fountain-art': 'Nature & Water Fountain', 'cartoon-painting': 'Cartoon Painting',
        'home-painting': 'Home Painting',
    }
    service_name = service_dict.get(service_type, 'Service')
    query_term = service_name

    # special cases
    if service_name == 'Mural Art':
        query_term = 'Mural'
    elif service_name == 'Nature & Water Fountain':
        query_term = 'Fountain'

    # Filtering logic
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

