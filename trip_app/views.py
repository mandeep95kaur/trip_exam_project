from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/travels')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        my_trips = logged_user.triper.all()
        context = {
            'false_trip': Trip.objects.filter(join=False),
            'true_trip': logged_user.has_created_trip.filter(join=True),
            'all_trip': Trip.objects.all(),
            'this_user': logged_user
        }
        return render(request, 'show_all.html', context)

def addtrip(request):
    return render(request, 'add.html')



def show_trip(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "show.html", context)

def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels')
    else:
        user = User.objects.get(id=request.session["user_id"])
        trip = Trip.objects.create(
            destination = request.POST['destination'],
            description = request.POST['description'],
            travel_date_from = request.POST['travel_date_from'],
            travel_date_to = request.POST['travel_date_to'],
            creater = user,
        )
        return redirect('/travels')

def cancel(request, trip_id):
    trip = Trip.objects.get(id=trip_id) 
    trip.cancel= True
    trip.save()
    return redirect("/travels")
    
def join(request, trip_id):
    trip = Trip.objects.get(id=trip_id) 
    trip.join = True
    trip.save()
    return redirect("/travels")

def delete(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()

    return redirect('/travels')

def logout(request):
    request.session.flush()

    return redirect('/')






