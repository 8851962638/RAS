from django.http import JsonResponse
from django.shortcuts import render
from .models import ServiceImage

def service_images_view(request):
    if request.method == "POST":
        try:
            name = request.POST.get("image_name")
            price = request.POST.get("price")
            type_of_art = request.POST.get("type_of_art")
            image = request.FILES.get("image")

            # Debug: Let's see what we're working with
            print(f"User: {request.user}")
            print(f"Is authenticated: {request.user.is_authenticated}")
            print(f"Full name: {getattr(request.user, 'full_name', 'NO FULL_NAME ATTR')}")
            print(f"Email: {getattr(request.user, 'email', 'NO EMAIL ATTR')}")

            # More defensive user handling with priority for full_name
            user_name = "Anonymous"  # Default fallback
            user_id = 0  # Default fallback
            
            if hasattr(request.user, 'is_authenticated') and request.user.is_authenticated:
                user_id = getattr(request.user, 'id', 0)
                
                # Priority order: full_name -> email -> fallback to Anonymous
                user_name = (getattr(request.user, 'full_name', None) or 
                            getattr(request.user, 'email', None) or 
                            'Anonymous')
                
                # Extra safety check for empty strings
                if not user_name or user_name.strip() == '':
                    user_name = "Anonymous"

            print(f"Final user_name: {user_name}")
            print(f"Final user_id: {user_id}")

            ServiceImage.objects.create(
                image_name=name,
                price=price,
                image=image,
                type_of_art=type_of_art,
                userupload_id=user_id,
                userupload_name=user_name,
            )

            return JsonResponse({"success": True, "message": "✅ Service Image added successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"❌ {str(e)}"})

    return render(request, "service_images.html")