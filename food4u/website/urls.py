from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from registration.views import CustomLoginView
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/', include('registration.urls')),
    path('login/', CustomLoginView.as_view(), name='member_login'),
    path('logout/', views.user_logout_view, name='member_logout'),
]