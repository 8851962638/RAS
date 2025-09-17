from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
import re, random
import json
from django.core.mail import send_mail
from django.conf import settings
# from .models import User  




from .models import Customer  

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import json, random, re

CustomUser = get_user_model()  # This points to accounts.CustomUser


@csrf_exempt
def save_customer_signup(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('customer_full_name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            create_password = request.POST.get('customer_password')

            if email:
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
def verify_customer_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_saved = request.session.get('otp')
        signup_data = request.session.get('signup_data')

        if otp_saved and signup_data and otp_entered == otp_saved:
            # Save user & customer after OTP verification
            user = CustomUser.objects.create_user(
            email=signup_data['email'],
            password=signup_data['customer_password'],  # hashed automatically
            full_name=signup_data['customer_full_name'],
            role='customer',
            is_verified=True
        )

            customer = Customer.objects.create(
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


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse AJAX JSON
            email = data.get("email")
            password = data.get("password")

            from django.contrib.auth import authenticate, login
            user = authenticate(request, email=email, password=password)

            if user is None:
                return JsonResponse({"success": False, "error": "Invalid email or password"})

            if not user.is_verified:
                return JsonResponse({"success": False, "error": "Email not verified yet!"})

            # Login and save session
            login(request, user)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return render(request, 'accounts/login.html')


@csrf_exempt
def login_auth(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")

            from django.contrib.auth import authenticate, login
            user = authenticate(request, email=email, password=password)

            if user is None:
                return JsonResponse({"success": False, "error": "Invalid email or password"})

            if not user.is_verified:
                return JsonResponse({"success": False, "error": "Email not verified yet!"})

            # Login and save session
            login(request, user)

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})



class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('accounts:login')  # Redirect after successful login

    def form_valid(self, form):
        messages.success(self.request, 'Welcome back!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password.')
        return super().form_invalid(form)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup_employee.html'
    success_url = reverse_lazy('accounts:login')  # Redirect after signup

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Account created successfully! Please login.')
        return super().form_valid(form)  # use super() to respect success_url

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@csrf_exempt
def save_employee_signup(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email_address')
            full_name = request.POST.get('full_name')
            mobile = request.POST.get('mobile')
            password = request.POST.get('password')

            if email:
                email_regex = r'^[^@\s]+@[^\s@]+\.[^@\s]+$'
                if not re.match(email_regex, email):
                    return JsonResponse({'success': False, 'error': 'Invalid email format'})

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Save form data + files temporarily in session
            signup_data = request.POST.dict()
            file_data = {k: v.name for k, v in request.FILES.items()}  # store only names in session

            request.session['employee_signup_data'] = signup_data
            request.session['employee_file_data'] = file_data
            request.session['employee_otp'] = otp

            # Store files temporarily in request.FILES (you’ll re-upload later)
            request.session['has_files'] = True

            # Send OTP
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
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def verify_employee_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_saved = request.session.get('employee_otp')
        signup_data = request.session.get('employee_signup_data')

        if otp_saved and signup_data and otp_entered == otp_saved:
            try:
                # Create Employee record
                employee = Employee.objects.create(
                    full_name=signup_data.get('full_name'),
                    fathers_name=signup_data.get('fathers_name'),
                    dob=signup_data.get('dob'),
                    gender=signup_data.get('gender'),
                    mobile=signup_data.get('mobile'),
                    email_address=signup_data.get('email_address'),
                    password=signup_data.get('password'),
                    house_no=signup_data.get('house_no'),
                    village=signup_data.get('village'),
                    city=signup_data.get('city'),
                    state=signup_data.get('state'),
                    pincode=signup_data.get('pincode'),
                    aadhar_card_no=signup_data.get('aadhar_card_no'),
                    experience=signup_data.get('experience'),
                    type_of_work=", ".join(request.POST.getlist('type_of_work')),
                    preferred_work_location=signup_data.get('preferred_work_location'),
                    bank_account_holder_name=signup_data.get('bank_account_holder_name'),
                    account_no=signup_data.get('account_no'),
                    ifsc_code=signup_data.get('ifsc_code'),
                    aadhar_card_image_front=request.FILES.get('aadhar_card_image_front'),
                    aadhar_card_image_back=request.FILES.get('aadhar_card_image_back'),
                    passport_photo=request.FILES.get('passport_photo')
                )

                # Clear session
                del request.session['employee_otp']
                del request.session['employee_signup_data']

                return JsonResponse({'success': True, 'message': 'Employee registered successfully!'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid OTP'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def customer_signup(request):
    return render(request, "accounts/signup_customer.html")

