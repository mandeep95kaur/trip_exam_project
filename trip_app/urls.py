from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('travels',views.show_all),
    path('travels/addtrip',views.addtrip),
    path('travels/create',views.create_trip),
    path('travels/<int:trip_id>',views.show_trip),
    path('travels/<int:trip_id>/cancel',views.cancel),
    path('travels/<int:trip_id>/delete',views.delete),
    path('travels/<int:trip_id>/join',views.join),
    path('logout',views.logout),
]