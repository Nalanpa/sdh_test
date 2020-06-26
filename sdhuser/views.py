"""
SDHUSER app views
"""

from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .forms import SignupForm
from .models import SDHuser

email_confirm_token = PasswordResetTokenGenerator()


def user_profile(request):
    """
    User profile page
    """
    user = request.user
    user_invite = SDHuser.objects.filter(invited=user)
    if request.method == 'POST':
        if not user.invitation_code:
            code_length = getattr(settings, 'INVITATION_CODE_LENGTH', 6)
            code = get_random_string(length=code_length)
            user.invitation_code = code
            user.save()
    return render(request, 'sdhuser/user_profile.html',
                  context={'user_invite': user_invite})


def top10(request):
    """
    Top-10 page
    """
    rating = SDHuser.objects.filter(points__gt=0).order_by('-points')[:10]
    return render(request, 'sdhuser/top10.html', context={'rating': rating})


def signup_confirm(request):
    """
    Signup confirmation page
    """
    return render(request, 'sdhuser/signup_confirm.html')


class Signup(View):
    """
    Signup view
    """
    form_class = SignupForm
    template_name = 'sdhuser/signup.html'

    def get(self, request):
        """
        GET request
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        POST request
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email_confirmed = False
            user.save()
            if user.invited:
                user.invited.accrue_points(user.invited.fond())
            current_site = get_current_site(request)
            subject = _('Activate your email')
            message = render_to_string('sdhuser/email_confirm_letter.html', {
                'user': user,
                'domain': current_site.domain,
                'user_id': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_confirm_token.make_token(user),
            })
            user.email_user(subject, message)
            return HttpResponseRedirect(reverse('signup-confirm'))

        return render(request, self.template_name, {'form': form})


def email_activate(request, user_id, token):
    """
    Activate (confirm) email
    """
    try:
        uid = force_text(urlsafe_base64_decode(user_id))
        user = SDHuser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and email_confirm_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        return render(request, 'sdhuser/email_confirmed.html')

    return render(request, 'sdhuser/email_confirm_invalid.html')
