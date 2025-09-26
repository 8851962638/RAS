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
