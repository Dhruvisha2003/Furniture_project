from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=25)
    url = models.FileField()

class products(models.Model):
    picture = models.ImageField()
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)

class pdetails(models.Model):
    photo = models.ImageField()
    name = models.CharField(max_length=20)
    detail = models.CharField(max_length=220)
    link = models.CharField(max_length=20)

class blogs(models.Model):
    images = models.ImageField()
    line1 = models.CharField(max_length=100)

class shop(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)

class About(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    details = models.CharField(max_length=255)
    link = models.CharField(max_length=20)

class blog_list(models.Model):
    photo = models.ImageField()
    detail = models.CharField(max_length=100)

class register(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    cpassword = models.CharField(max_length=10)

class addCart(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()

class data(models.Model):
    country = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    street = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=6)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)

class order(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    total = models.IntegerField()