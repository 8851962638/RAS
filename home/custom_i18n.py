"""Custom internationalization views"""
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.i18n import set_language as django_set_language
import logging

logger = logging.getLogger(__name__)


def custom_set_language(request):
    """
    Custom set_language view that properly handles language switching
    and redirects with the correct language prefix.
    """
    # Get the language and next URL from POST data
    language = request.POST.get('language', settings.LANGUAGE_CODE)
    next_url = request.POST.get('next', '')
    
    # Set language in session
    request.session['django_language'] = language
    request.session.modified = True
    
    print(f"\n{'='*60}")
    print(f"🔄 CUSTOM SET_LANGUAGE VIEW")
    print(f"{'='*60}")
    print(f"Language Requested: {language}")
    print(f"Next URL from form: {next_url}")
    print(f"Session Language Set: {request.session.get('django_language')}")
    print(f"{'='*60}\n")
    
    # Build the redirect URL with language prefix
    if not next_url or next_url == '/' or next_url == '':
        redirect_url = f'/{language}/'
    else:
        # Ensure the path starts with / and add language prefix
        if not next_url.startswith('/'):
            next_url = '/' + next_url
        redirect_url = f'/{language}{next_url}'
    
    print(f"Final redirect URL: {redirect_url}\n")
    
    return HttpResponseRedirect(redirect_url)
