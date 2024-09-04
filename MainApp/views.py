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
from .models import Address

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
    myid = request.GET.get('cartid')
    if myid:
        product = shop.objects.filter(id=myid).first()
        if product:
            image = product.image
            name = product.name
            price = product.price
            quantity = 1 
            total = price * quantity
            cart_item = addCart(image=image, name=name, price=price, quantity=quantity, total=total)
            cart_item.save()
    cart_items = addCart.objects.all()
    subtotal = sum(i.total for i in cart_items)
    total = subtotal
    # print(all)
    return render(request,'cart.html',{"cart_items":cart_items,'subtotal':subtotal,'total':total})

def delcart(request):
    cartid = request.GET.get('cartid')
    if cartid:
        cart_item = addCart.objects.filter(id=cartid).first()
        if cart_item:
            cart_item.delete()
    return redirect('cart_view')
    
def update_cart_quantity(request):
    cartid = request.POST.get('cartid')
    action = request.POST.get('action')
    cart_item = addCart.objects.filter(id=cartid).first()
    if cart_item:
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        cart_item.total = cart_item.price * cart_item.quantity
        cart_item.save()
    all=addCart.objects.all()
    print(all)
    return redirect('cart_view')

def checkOut(request):
    data = addCart.objects.all()
    subtotal = sum(i.total for i in data)
    total = subtotal
    
    if request.method == 'POST':
        country = request.POST.get('country')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        street = request.POST.get('street')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        data = Address(country=country,first_name=first_name,last_name=last_name,address=address,street=street,state=state,zip=zip,email=email,phone=phone)
        data.save()

    return render(request,'checkout.html',{'data':data,'subtotal':subtotal,'total':total})

def payment(request):
    return render(request,'Payment.html')

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
        
