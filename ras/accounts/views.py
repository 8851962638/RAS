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
from .models import User  




from .models import Customer  # import your Customer model

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


@csrf_exempt  # CSRF token is included via AJAX FormData
def save_signup(request):
    if request.method == 'POST':
        try:
            # Get all the data from POST
            full_name = request.POST.get('full_name')
            fathers_name = request.POST.get('fathers_name')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            mobile = request.POST.get('mobile')
            email_address = request.POST.get('email_address')
            password = request.POST.get('password')
            house_no = request.POST.get('house_no')
            village = request.POST.get('village')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            aadhar_card_no = request.POST.get('aadhar_card_no')
            experience = request.POST.get('experience')
            type_of_work_list = request.POST.getlist('type_of_work')  # for checkboxes
            preferred_work_location = request.POST.get('preferred_work_location')
            bank_account_holder_name = request.POST.get('bank_account_holder_name')
            account_no = request.POST.get('account_no')
            ifsc_code = request.POST.get('ifsc_code')

            # Get uploaded files
            aadhar_card_image_front = request.FILES.get('aadhar_card_image_front')
            aadhar_card_image_back = request.FILES.get('aadhar_card_image_back')
            passport_photo = request.FILES.get('passport_photo')

            # Join type_of_work list into a string
            type_of_work = ', '.join(type_of_work_list)

            # Create Employee record
            employee = Employee.objects.create(
                full_name=full_name,
                fathers_name=fathers_name,
                dob=dob,
                gender=gender,
                mobile=mobile,
                email_address=email_address,
                password=password,  # You may want to hash it for security
                house_no=house_no,
                village=village,
                city=city,
                state=state,
                pincode=pincode,
                aadhar_card_no=aadhar_card_no,
                aadhar_card_image_front=aadhar_card_image_front,
                aadhar_card_image_back=aadhar_card_image_back,
                experience=experience,
                type_of_work=type_of_work,
                preferred_work_location=preferred_work_location,
                passport_photo=passport_photo,
                bank_account_holder_name=bank_account_holder_name,
                account_no=account_no,
                ifsc_code=ifsc_code
            )

            return JsonResponse({'success': True, 'message': 'Employee saved successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def customer_signup(request):
    return render(request, "accounts/signup_customer.html")
@csrf_exempt
def save_customer_signup(request):
    if request.method == 'POST':
        try:
            # Get signup data
            full_name = request.POST.get('customer_full_name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            create_password = request.POST.get('customer_password')

            # Validate email
            email_regex = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
            if not re.match(email_regex, email):
                return JsonResponse({'success': False, 'error': 'Invalid email format'})

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Store data in session temporarily
            request.session['signup_data'] = {
                'customer_full_name': full_name,
                'mobile': mobile,
                'email': email,
                'customer_password': create_password,
            }
            request.session['otp'] = otp

            # Send OTP email
            send_mail(
                subject="Your Painting App Verification OTP",
                message=f"Hello {full_name},\n\nYour OTP is: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'OTP sent to email!'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
def verify_customer_otp(request):
    if request.method == "POST":
        otp_entered = request.POST.get('otp')

        # Retrieve stored data & OTP
        otp_saved = request.session.get('otp')
        signup_data = request.session.get('signup_data')

        if otp_saved and signup_data and otp_entered == otp_saved:
        
        
        # Create User in DB after OTP verification
            qs=User.objects.create(
                full_name=signup_data['customer_full_name'],
                email_id=signup_data['email'],
                password=signup_data['customer_password'],
                is_verified=True,
                role='customer'
            )
            # Create customer in DB after OTP verification
            customer = Customer.objects.create(
                customer_full_name=signup_data['customer_full_name'],
                user_id_id=qs.id,
                mobile=signup_data['mobile'],
                email=signup_data['email'],
                customer_password=signup_data['customer_password'],
                is_verified=True
            )

            # Clear session
            del request.session['otp']
            del request.session['signup_data']

            return JsonResponse({'success': True, 'message': 'Email verified & customer registered!', 'customer_id': customer.id})
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

            user = User.objects.get(email_id=email, password=password)  # ⚠️ Use hashed passwords in production

            # Save session
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            request.session['is_verified'] = user.is_verified

            return JsonResponse({"success": True})

        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid email or password"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    # For GET request, just render login page
    return render(request, 'home/home.html')