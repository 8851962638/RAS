# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from .models import Employee

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that don't require profile completion
        allowed_urls = [
            '/edit_profile/',
            '/wallet/',  # Changed to direct path
            '/accounts/logout/',
            '/accounts/login/',
            '/media/',
            '/static/',
            '/admin/',
        ]

        # Check if user is authenticated and is an employee
        if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'employee':
            # Check if current path is not in allowed URLs
            current_path = request.path
            is_allowed = any(current_path.startswith(url) for url in allowed_urls)

            if not is_allowed:
                try:
                    employee = Employee.objects.get(user=request.user)
                    
                    # Check if profile is incomplete
                    if (not employee.fathers_name or 
                        not employee.dob or 
                        not employee.aadhar_card_no or
                        not employee.passport_photo):
                        
                        # Redirect to edit profile
                        return redirect('/edit_profile/')
                        
                except Employee.DoesNotExist:
                    pass

        response = self.get_response(request)
        return response