from django.shortcuts import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import Menu
from .models import products
from .models import pdetails
from .models import shop
from .models import blogs
from .models import About
from .models import blog_list
from .models import register
from .models import addCart
from .models import data
from .models import order

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

        detail = data(country=country, first_name=first_name, last_name=last_name,
                address=address, street=street, state=state, zip=zip, email=email, phone=phone)
        detail.save()

    print('hello')
    product = addCart.objects.all()
    for i in product:
        name = i.name
        quantity = i.quantity
        total = i.total
        print(name)
        print(quantity)
        print(total)
        order_item = order(name=name,quantity=quantity,total=total)
        order_item.save()
    order_items = order.objects.all()
    subtotal = sum(i.total for i in product)
    total = subtotal

    return redirect('checkOut',{'order_items':order_items,'subtotal':subtotal,'total':total})

def payment_view(request):
    # print('Hello')
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'creditdebit':
            cardnumber = request.POST.get('cardnumber')
            cardholder = request.POST.get('cardholder')
            expirydate = request.POST.get('expirydate')
            # print(cardnumber)
            # print(cardholder)
            # print(expirydate)
            if cardnumber and cardholder and expirydate:
                return redirect('/thanks')
            else:
                return render(request, 'checkout.html', {'error': 'Please fill out all required fields for credit/debit card.'})
        
        elif payment_method == 'netbanking':
            account_number = request.POST.get('acnumber')
            account_holder = request.POST.get('account_holder')
            
            if account_number and account_holder:
                return redirect('thanks')
            else:
                return render(request, 'checkout.html', {'error': 'Please fill out all required fields for net banking.'})
        
        elif payment_method == 'UPI':
            upi_id = request.POST.get('upi')
            
            if upi_id:
                return redirect('thanks')
            else:
                return render(request, 'checkout.html', {'error': 'Please provide your UPI ID.'})
        
        else:
            return render(request, 'checkout.html', {'error': 'Unknown payment method selected.'})

    return render(request, 'checkout.html')


def thankyou(request):
    return render(request,'thankyou.html')

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
            if password == log.password.strip():
                return redirect('/')
            else:
                return HttpResponse('Invalid Email or Password')
        else:
            return HttpResponse('Invalid Email or Password')
    else:
        return render(request, 'login.html')
        
