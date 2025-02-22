from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from .db import SessionLocal, User, Supplier, Products, Review
from sqlalchemy import select

from datetime import datetime

def home_view(request):
    return render(request, 'website/home.html')
def wishlist_view(request):
    return render(request, 'website/wishlist.html')
def about_view(request):
    return render(request, 'website/aboutUs.html')
def profile_view(request, supplier_id):
    session = SessionLocal()
    try:
        query = select(Supplier).where(Supplier.id == supplier_id)
        results = session.scalar(query)
        print(results.reviews)
        supplier_dict = {
                        'id' : results.id,
                        'name' : results.name,
                        'address' : results.address,
                        'email' : results.email,
                        'phone' : results.phone,
                        'industry' : results.industry,
                        'date_registered' : results.date_registered,
                        'description' : results.description,
                        'reviews' : results.reviews}
        print(supplier_dict)
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
    rating_min = int(request.GET.get('rating_min', '1'))
    rating_max = int(request.GET.get('rating_max', '5'))
    hide_no_rating = request.GET.get('hide_no_rating', 'false')
    session = SessionLocal()
    try:
        query = select(Supplier)
        # if industry != 'any':
        #     query = query.where(Supplier.industry == industry)
        results_unrefined = session.scalars(query)
        results = []
        suppliers = []
        for supplier in results_unrefined.all():
            #print(supplier.name)
            rating_sum = 0
            rating_count = len(supplier.reviews)
            if rating_count == 0 and hide_no_rating == 'true':
                print("skipped")
                continue
            for review in supplier.reviews:
                rating_sum += review.rating
            if rating_count == 0:
                rating_count = 1
            elif rating_sum / rating_count < rating_min or rating_sum / rating_count > rating_max:
                print("skipped")
                continue
            supplier_dict = {'name' : supplier.name, 
                            'address' : supplier.address, 
                            'email' : supplier.email, 
                            'phone' : supplier.phone, 
                            'industry' : supplier.industry, 
                            'date_registered' : supplier.date_registered, 
                            'description' : supplier.description,
                            'average_rating' : rating_sum / rating_count}           
            suppliers.append(supplier_dict)
        return JsonResponse(suppliers, safe=False)
    except Exception as e:
        session.rollback()
        print(e)
        return render(request, 'website/error.html', {'error': str(e)})
    finally:
        session.close()

def account_view(request, user_id):
    session = SessionLocal()
    try:
        query = select(User).where(User.id == user_id)
        results = session.scalar(query)
        user_dict = {'name' : results.name, 
                        'address' : results.address, 
                        'email' : results.email, 
                        'phone' : results.phone, 
                        'industry' : results.industry, 
                        'date_registered' : results.date_registered, 
                        'description' : results.description}
        return render(request, 'website/account.html', user_dict)
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




session = SessionLocal()
try:
    rev1 = Review(writer_id=1, product_id=1, supplier_id=2, rating=5, label="test review1", content="test content1", date=datetime.now())
    rev2 = Review(writer_id=1, product_id=1, supplier_id=2, rating=4, label="test review2", content="test content2", date=datetime.now())
    #test_supplier = Supplier(name="test supplsier2", address="test address2", email="tests email2", phone="test phone2", industry="test industry2", description="test description2",
                             #reviews=[rev1, rev2])
    session.add(rev1)
    session.add(rev2)
    #session.add(test_supplier)
    session.commit()
    print("adsadasdassa")
    #data = [obj.to_dict() for obj in results]  # Assume your models have a to_dict method
except Exception as e:
    print(e)
    print("errorerrorerrorerror")
    session.rollback()
finally:
    session.close()