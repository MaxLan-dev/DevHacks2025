from django.urls import path
from .views import RegisterView, VerifyRegistrationView, UserLoginView, HomeView, WelcomeView, UserLogoutView, \
    PasswordResetRequestView, PasswordResetSentView, ResetPasswordView, ChangePasswordView, CheckEmailView, CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/retailer/', RegisterView.as_view(), kwargs={'retailer': 'true'}, name='register_retailer'),
    path('verify/<str:verification_id>/', VerifyRegistrationView.as_view(), name='verify_registration'),
    # path('login/', UserLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='member_login'),
    # path('home/', HomeView.as_view(), name='home'),
    # path('', WelcomeView.as_view(), name='welcome'),
    # path('logout/', UserLogoutView.as_view(), name='member_logout'),
    path('logout/', UserLogoutView.as_view(), name='member_logout'),
    path('password_reset_request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset_sent/', PasswordResetSentView.as_view(), name='password_reset_sent'),
    path('reset_password/<str:verification_id>/', ResetPasswordView.as_view(), name='reset_password'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
]
