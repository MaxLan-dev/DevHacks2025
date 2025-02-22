from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from registration.views import CustomLoginView
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/<int:supplier_id>', views.profile_view, name='profile'),
    path('search', views.search_view, name='search'),
    path('about', views.about_view, name='about'),
    path('account', views.account_view, name='account'),
    path('search_results', views.search_results_request, name='search_results'),
    path('accounts/', include('registration.urls')),
    path('login/', CustomLoginView.as_view(), name='member_login'),
    path('logout/', views.user_logout_view, name='member_logout'),
]