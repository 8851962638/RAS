from django.shortcuts import render

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
