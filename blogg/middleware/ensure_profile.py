from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Profile
from django.contrib import messages

class EnsureProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only for authenticated users
        if request.user.is_authenticated:
            profile=Profile.objects.filter(user=request.user).first()
            if (not profile and request.path != reverse('onboarding')):
                messages.info(request, 'Please complete onboarding process! ')
                return redirect('onboarding')
        return self.get_response(request)
