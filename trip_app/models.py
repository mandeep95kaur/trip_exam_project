from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # Length of the first name
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"

        # Length of the last name
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"

        # Email matches format
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        # Email is unique
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"

        # Password was entered (less than 8)
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characers long"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Your passwords do not match"

        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors['destination'] = 'destination should be at least 3 character'
        if len(postData['description']) < 3:
            errors['description'] = 'decription should be at least three character'
        return errors
        if datetime.strptime(form['travel_date_from'], '%Y-%m-%d') < datetime.now():
            errors['travel_date_from'] = 'travel Date should be in the future'
        return errors
        if datetime.strptime(form['travel_date_to'], '%Y-%m-%d') < datetime.now():
            errors['travel_date_to'] = 'travel Date to should be Date  after the travel date from '
        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creater = models.ForeignKey(User, related_name="has_created_trip", on_delete=models.CASCADE)
    trip_by = models.ManyToManyField(User, related_name="triper")
    join = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = TripManager()

