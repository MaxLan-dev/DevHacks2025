from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/<int:supplier_id>', views.profile_view, name='profile'),
    path('search', views.search_view, name='search'),
    path('about', views.about_view, name='about'),
    path('search_results', views.search_results_request, name='search_results'),
]