import os
from django.contrib.auth import logout, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, PasswordResetRequestForm, \
    SetPasswordForm, ChangePasswordForm
from .models import CustomUser
import uuid
import smtplib
import ssl
from django.core.mail.backends.smtp import EmailBackend
from .forms import CustomLoginForm
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache

from django.contrib.auth.models import Group
from django.db import transaction

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Retailers').exists():
            return reverse_lazy('retailer_registered_home')
        else:
            return reverse_lazy('farmer_landing')

class CustomEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        try:
            # Set up the SSL context with disabled certificate verification
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Connect to the SMTP server
            self.connection = smtplib.SMTP(self.host, self.port)
            self.connection.ehlo()
            self.connection.starttls(context=context)
            self.connection.ehlo()

            # Log in to the SMTP server if credentials are provided
            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except:
            if not self.fail_silently:
                raise
            return False


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('farmer_landing') # Direct redirect

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_retailer'] = self.kwargs.get('retailer', 'false').lower() == 'true'
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()  # Save the user
        user.set_password(form.cleaned_data['password1'])
        user.save()

        group_name = 'Retailers' if form.is_retailer else 'Subscribers'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        login(self.request, user)  # Log in immediately
        return super().form_valid(form)

class VerifyRegistrationView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(verification_id=kwargs['verification_id'])
            user.is_active = True
            user.verification_id = None
            user.save()
            login(request, user)
            
            # Check if the user is in the Retailers group
            if user.groups.filter(name='Retailers').exists():
                return redirect('retailer_registered_home')
            else:
                return redirect('farmer_landing')
        except CustomUser.DoesNotExist:
            return render(request, 'registration/verification_failed.html')

# class CheckEmailView(LoginRequiredMixin, TemplateView):
class CheckEmailView(TemplateView):
    template_name = 'registration/check_email.html'


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'website/home.html'


class WelcomeView(TemplateView):
    template_name = 'website/welcome.html'


# class UserLogoutView(LogoutView):
#     @method_decorator(csrf_protect)
#     def post(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('home')  
class UserLogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('home')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        response = super().dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class PasswordResetRequestView(FormView):
    template_name = 'registration/password_reset_request.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('password_reset_sent')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            user.verification_id = str(uuid.uuid4())
            user.save()
            reset_url = self.request.build_absolute_uri(
                reverse_lazy('reset_password', args=[user.verification_id])
            )
            send_mail(
                'Reset your password',
                f'Click this link to reset your password: {reset_url}',
                os.environ.get('RAG_RELAY_EMAIL'),
                [user.email],
                fail_silently=False,
                auth_user=os.environ.get('RAG_RELAY_EMAIL'),
                auth_password=os.environ.get('RAG_RELAY_PW'),
            )
        except CustomUser.DoesNotExist:
            pass
        return super().form_valid(form)

class PasswordResetSentView(TemplateView):
    template_name = 'registration/password_reset_sent.html'


class ResetPasswordView(FormView):
    template_name = 'registration/reset_password.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('member_login')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = CustomUser.objects.get(verification_id=kwargs['verification_id'])
        except CustomUser.DoesNotExist:
            return render(request, 'registration/reset_password_invalid.html')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'verification_id': self.kwargs['verification_id']}
        return kwargs

    def form_valid(self, form):
        # TODO: Should I verify both passwords match?
        self.user.set_password(form.cleaned_data['new_password1'])
        self.user.verification_id = None
        self.user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url


# Enter current and new pw1/pw2
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('home')
    template_name = 'registration/change_password.html'

    def get_success_url(self):
        return self.success_url
