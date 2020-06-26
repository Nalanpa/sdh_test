"""
Forms for SDHUSER app
"""

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import SDHuser


class SignupForm(UserCreationForm):
    """
    User Sign-Up form
    """
    username = forms.CharField(
        label=_('Username'),
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your username'),
            'class': 'form-control'
        }),
    )
    password1 = forms.CharField(
        label=_('Password'),
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your password'),
            'class': 'form-control',
            'type': 'password',
        }),
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': _('Confirm your password'),
            'class': 'form-control',
            'type': 'password',
        }),
    )
    email = forms.EmailField(
        label=_('EMail'),
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': _('Enter your EMail'),
            'class': 'form-control'
        }),
        error_messages={'invalid': _('Invalid EMail format')}
    )
    invitation_code = forms.CharField(
        label=_('Invitattion Code'),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your invitation code'),
            'class': 'form-control'
        }),
        )

    # pylint: disable=missing-class-docstring, disable=too-few-public-methods
    class Meta:
        model = SDHuser
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'invitation_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        not_invited_count = SDHuser.not_invited_users_count()
        max_not_invited = getattr(settings, 'MAX_NOT_INVITED', 2)
        if not_invited_count > max_not_invited:
            self.fields['invitation_code'].required = True

    def clean_invitation_code(self):
        """
        Invitation code format check
        """
        invitation_code = self.cleaned_data.get('invitation_code')
        code_length = getattr(settings, 'INVITATION_CODE_LENGTH', 6)
        if len(invitation_code) != code_length:
            self.add_error(
                'invitation_code',
                format_lazy(
                    'Invitation code must be {} characters long',
                    code_length))
        try:
            invitor = SDHuser.objects.get(invitation_code=invitation_code)
            self.instance.invited = invitor
        # pylint: disable=E1101
        except SDHuser.DoesNotExist:
            self.add_error('invitation_code', 'Wrong invitation code')
        return ''

    def clean_email(self):
        """
        Avoid email duplication
        """
        email = self.cleaned_data.get('email')
        if email and SDHuser.objects.filter(email=email).exists():
            self.add_error('email', _('Email is registered already'))
        return email
