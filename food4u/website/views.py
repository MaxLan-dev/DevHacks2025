from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from .db import SessionLocal, User, Supplier, Products, Review
from sqlalchemy import select

def home_view(request):
    return render(request, 'website/home.html')

def about_view(request):
    return render(request, 'website/about.html')

def profile_view(request, supplier_id):
    session = SessionLocal()
    try:
        query = select(Supplier).where(Supplier.id == supplier_id)
        results = session.scalar(query)
        supplier_dict = {'name' : results.name, 
                        'address' : results.address, 
                        'email' : results.email, 
                        'phone' : results.phone, 
                        'industry' : results.industry, 
                        'date_registered' : results.date_registered, 
                        'description' : results.description}
        return render(request, 'website/profile.html', supplier_dict)
    except Exception as e:
        session.rollback()
        return render(request, 'website/error.html', {'error': str(e)})
    finally:
        session.close()

def search_view(request):
    session = SessionLocal()
    try:
        query = select(Supplier)
        results = session.scalars(query)
        suppliers = []
        for result in results:
            supplier_dict = {'name' : result.name, 
                            'address' : result.address, 
                            'email' : result.email, 
                            'phone' : result.phone, 
                            'industry' : result.industry, 
                            'date_registered' : result.date_registered, 
                            'description' : result.description}
            suppliers.append(supplier_dict)
        return render(request, 'website/search.html', {'suppliers' : suppliers, 'is_authenticated' : request.user.is_authenticated})
    except Exception as e:
        session.rollback()
        return render(request, 'website/error.html', {'error': str(e)})
    finally:
        session.close()
    return render(request, 'website/search.html')

def search_results_request(request):
    # Industry, Location, Rating
    industry = request.GET.get('industry', 'any')
    #location = request.GET.get('location', '1000')
    rating_min = request.GET.get('rating_min', '1')
    rating_max = request.GET.get('rating_max', '5')
    hide_no_rating = request.GET.get('hide_no_rating', 'false')
    session = SessionLocal()
    try:
        query = select(Supplier)
        # if industry != 'any':
        #     query = query.where(Supplier.industry == industry)
        results_unrefined = session.scalars(query)
        print(results_unrefined.all())
        print(results_unrefined)
        results = []
        suppliers = []
        for supplier in results_unrefined:
            rating_sum = 0
            if supplier.reviews.length == 0 and hide_no_rating == 'true':
                print("skipped")
                continue
            for review in supplier.reviews:
                rating_sum += review.rating
            if rating_sum / supplier.reviews.length < rating_min or rating_sum / supplier.reviews.length > rating_max:
                continue
            supplier_dict = {'name' : supplier.name, 
                            'address' : supplier.address, 
                            'email' : supplier.email, 
                            'phone' : supplier.phone, 
                            'industry' : supplier.industry, 
                            'date_registered' : supplier.date_registered, 
                            'description' : supplier.description,
                            'average_rating' : rating_sum / supplier.reviews.length}           
            suppliers.append(supplier_dict)
        return JsonResponse(suppliers, safe=False)
    except Exception as e:
        session.rollback()
        return render(request, 'website/error.html', {'error': str(e)})
    finally:
        session.close()
@never_cache
@require_POST
def user_logout_view(request):
    logout(request)
    response = redirect('home')
    return response
