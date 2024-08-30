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
    cart_items = addCart.objects.filter(user=request.user)
    
    # Calculate total price of items in the cart
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(shop, id=product_id)
    quantity = request.POST.get('quantity', 1)  # Default to 1 if no quantity provided

    cart_item, created = addCart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()

    return redirect('cart_view')

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(addCart, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart_view')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(addCart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')


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
        
