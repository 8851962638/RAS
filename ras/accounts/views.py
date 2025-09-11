
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
