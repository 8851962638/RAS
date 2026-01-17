from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import translation
import logging

logger = logging.getLogger(__name__)


def custom_set_language(request):
    language = request.POST.get('language', settings.LANGUAGE_CODE)

    # Activate language
    translation.activate(language)

    # Store language in session manually (Django 5 compatible)
    request.session['django_language'] = language
    request.session.modified = True

    print(f"\n{'='*60}")
    print(f"🔄 CUSTOM SET_LANGUAGE VIEW")
    print(f"{'='*60}")
    print(f"Language Requested: {language}")
    print(f"Session Language Set: {request.session.get('django_language')}")
    print(f"{'='*60}\n")

    # Get previous page
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', '/')

    # Remove existing language prefix
    for lang_code, _ in settings.LANGUAGES:
        prefix = f"/{lang_code}/"
        if next_url.startswith(prefix):
            next_url = next_url[len(prefix):]
            break


    # Build clean redirect
    if not next_url or next_url == '/':
        redirect_url = f"/{language}/"
    else:
        if not next_url.startswith('/'):
            next_url = '/' + next_url
        redirect_url = f"/{language}{next_url}"

    print(f"Final redirect URL: {redirect_url}\n")

    return HttpResponseRedirect(redirect_url)
