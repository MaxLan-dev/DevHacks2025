from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from .db import SessionLocal, User, Supplier, Products, Review
from sqlalchemy import select
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from registration.forms import UserUpdateForm, ReviewAddForm  # You'll need to create this form
from .db import SessionLocal, User
from sqlalchemy import select, update

from datetime import datetime

def home_view(request):
    return render(request, 'website/home.html')
def about_view(request):
    return render(request, 'website/aboutUs.html')
def profile_view(request, supplier_id):
    session = SessionLocal()
    try:
        query = select(Supplier).where(Supplier.id == supplier_id)
        results = session.scalar(query)
        if request.method == 'POST':
            form = ReviewAddForm(request.POST)
            if form.is_valid():
                # Update the user data in the database
                review = Review(
                    content = form.cleaned_data['content'],
                    rating = form.cleaned_data['rating'],
                    date = datetime.now(),
                    writer = request.user
                )
                session.add(review)
                session.commit()
                return redirect('profile', supplier_id=supplier_id)
        reviews = []
        for review in results.reviews:
            review_dict = {'content' : review.content,
                            'date' : review.date,
                            'rating' : review.rating,
                            'author' : review.writer.name}
            reviews.append(review_dict)
        supplier_dict = {
    'name': results.name,
    'address': results.address,
    'email': results.email,
    'phone': results.phone,
    'industry': results.industry,
    'date_registered': results.date_registered,
    'description': results.description,
    'reviews': reviews,
    'supplier_id': supplier_id  # Add this line
}

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
    industry = request.GET.get('industry', '')
    #location = request.GET.get('location', '1000')
    rating_min = int(request.GET.get('rating_min', '1'))
    rating_max = int(request.GET.get('rating_max', '5'))
    hide_no_rating = request.GET.get('no_rating', 'false')
    session = SessionLocal()
    try:
        query = select(Supplier)
        if industry != '':
             query = query.where(Supplier.industry == industry)
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
            supplier_dict = {'id' : supplier.id,
                            'name' : supplier.name, 
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

@login_required
def account_view(request):
    session = SessionLocal()
    try:
        query = select(User).where(User.email == request.user.email)
        user = session.scalar(query)

        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                # Update the user data in the database
                update_stmt = (
                    update(User)
                    .where(User.email == request.user.email)
                    .values(
                        name=form.cleaned_data['name'],
                        address=form.cleaned_data['address'],
                        phone=form.cleaned_data['phone'],
                        industry=form.cleaned_data['industry'],
                        description=form.cleaned_data.get('description', '')
                    )
                )
                session.execute(update_stmt)
                session.commit()
                messages.success(request, 'Your account has been updated!')
                return redirect('account')
        else:
            form = UserUpdateForm(initial={
                'name': user.name,
                'address': user.address,
                'phone': user.phone,
                'industry': user.industry,
                'description': user.description
            })

        user_dict = {
            'email': user.email,
            'date_registered': user.date_registered,
            'form': form
        }
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