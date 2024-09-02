from django.shortcuts import *
from django.http import HttpResponse
from .models import Menu
from .models import products
from .models import pdetails
from .models import shop
from .models import blogs
from .models import About
from .models import blog_list
from .models import register
from .models import addCart

# Create your views here.

def index(request):
    menus = Menu.objects.all()
    products_list = products.objects.all()
    product_detail = pdetails.objects.all()
    blog_detail = blogs.objects.all()
    return render(request, 'index.html',{'menus':menus,'products_list':products_list,'product_detail':product_detail,'blog_detail':blog_detail})

def shopPage(request):
    shop_detail = shop.objects.all()
    return render(request,'shop.html',{'shop_detail':shop_detail})

def aboutus(request):
    about_us = About.objects.all()
    return render(request,'about.html',{'about_us':about_us})

def Blog(request):
    blog_detail = blog_list.objects.all()
    return render(request,'blog.html',{'blog_detail':blog_detail})

def Ourservice(request):
    services = products.objects.all()
    return render(request,'services.html',{'services':services})

def contact(request):
    return render(request,'contact.html')

def cart_view(request):
    myid=request.GET.get('cartid')
    print(myid)
    filter=shop.objects.filter(id=myid).first()
    image = filter.image
    name = filter.name
    price = filter.price
    quantity = 1
    total = price * quantity
    product = addCart(image=image,name=name,price=price,quantity=quantity,total=total)
    product.save()
    cart_items = addCart.objects.all()
    return render(request,'cart.html',{'cart_items':cart_items})

def delcart(request):
    data = request.GET.get('cartid')
    filter_data = addCart.objects.filter(id=data).first()
    filter_data.delete()
    return redirect('Cart')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user = register(username=username,email=email,password=password,cpassword=cpassword)
        user.save()
        return redirect('login')
    return render(request,'signin.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        
        log = register.objects.filter(email=email).first()
        
        if log:
            # Strip any whitespace from the stored password as well
            if password == log.password.strip():
                return redirect('/')
            else:
                return HttpResponse('Invalid Email or Password')
        else:
            return HttpResponse('Invalid Email or Password')
    else:
        return render(request, 'login.html')
        
