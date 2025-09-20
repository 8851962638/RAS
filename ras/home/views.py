from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def home_view(request):
    return render(request, 'home.html')

def edit_profile(request):
    return render(request, "edit_profile.html")


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
