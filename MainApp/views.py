from django.shortcuts import *
from django.http import HttpResponse
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from .models import Menu
from .models import products
from .models import pdetails
from .models import shop
from .models import blogs
from .models import About
from .models import blog_list
from .models import register_data
from .models import addCart
from .models import bill_address
from .models import ship_address

# from .models import order

# Create your views here.

def index(request):
    user_id = request.session.get('user_id')
    print(user_id)
    menus = Menu.objects.all()
    products_list = products.objects.all()
    product_detail = pdetails.objects.all()
    blog_detail = blogs.objects.all()
    return render(request, 'index.html',{'menus':menus,'products_list':products_list,'product_detail':product_detail,'blog_detail':blog_detail,'user_id':user_id})

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
        email = request.POST.get('email')
        country = request.POST.get('country')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        street = request.POST.get('street')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone')
        ordernote = request.POST.get('ordernote')
        
        if not email:
            return HttpResponse('Email is required.')
        
        if not register_data.objects.filter(email=email).exists():
            messages.error(request, 'User not found in the Register table!!! Please Register or login')
            return redirect('checkout')

        # try:
        #     register_entry = register_data.objects.get(email=email)
        # except register_data.DoesNotExist:
        #     messages.error(request, 'User not found in the Register table!!! Please Register or login')
        #     return redirect('checkout')

        if bill_address.objects.filter(email=email).exists() or ship_address.objects.filter(email=email).exists():
            messages.error(request, 'This email is already used! Please try with another email.')
            return redirect('checkout')

        detail = bill_address(
            country=country, first_name=first_name, last_name=last_name,
            address=address, street=street, state=state, zip=zip, email=email, phone=phone)
        detail.save()

        ship_detail = ship_address(
            country=country, first_name=first_name, last_name=last_name,
            address=address, street=street, state=state, zip=zip, email=email, phone=phone)
        ship_detail.save()

        return redirect('order_view')
    return render(request, 'checkout.html')

    
def order_view(request):
    print('orders')
    alll=addCart.objects.all()
    subtotal = sum(i.total for i in alll)
    total = subtotal
    return render(request,'order.html',{"alll":alll,"subtotal":subtotal,"total":total})

def payment_view(request):
    print('call')
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'creditdebit':
            print('card')
            cardnumber = request.POST.get('cardnumber')
            cardholder = request.POST.get('cardholder')
            expirydate = request.POST.get('expirydate')
          
            if cardnumber and cardholder and expirydate:
                print('hello')
                addCart.objects.all().delete()
                return redirect('/thanks/')
            else:
                return render(request, 'order.html', {'error': 'Please fill out all required fields for credit/debit card.'})
        
        elif payment_method == 'netbanking':
            print('netbanking')
            account_number = request.POST.get('account_number')
            account_holder = request.POST.get('account_holder')
            
            if account_number and account_holder:
                print('hello')
                addCart.objects.all().delete()
                return redirect('/thanks')
            else:
                return render(request, 'order.html', {'error': 'Please fill out all required fields for net banking.'})
        
        elif payment_method == 'UPI':
            print('upi')
            upi_id = request.POST.get('upi')
            
            if upi_id:
                print('hello')
                addCart.objects.all().delete()
                return redirect('/thanks')
            else:
                return render(request, 'order.html', {'error': 'Please provide your UPI ID.'})
        
        else:
            return render(request, 'order.html', {'error': 'Unknown payment method selected.'})

    return render(request, 'order.html')


def thankyou(request):
    return render(request,'thankyou.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        # if email:
        #     return HttpResponse('This email is already registered')
        # else:
        user = register_data(username=username,email=email,password=password,cpassword=cpassword)
        user.save()
        
        return redirect('login')
    return render(request,'register.html')


def login_user(request):
    print('function called')
    if request.method == 'POST':
        print('received request')
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        print('Function called')
        print('Received request')
        print('Email:', email)
        print('Password:', password)

        try:
            log = register_data.objects.get(email=email)
            print('ID:',log.id)
            request.session['id']=log.id
            # print("Session==",Sessionn)
            if request.session['id']:
                print('yes')
                return redirect('/')
            if password == log.password.strip():
                    return redirect('/')
            else:
                messages.error(request, 'Invalid Email or Password')
                return redirect('login')
        except register_data.DoesNotExist:
            messages.error(request, 'Invalid Email or Password')
        return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    return redirect('/')        
