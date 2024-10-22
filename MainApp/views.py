from django.shortcuts import *
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.cache import cache_control
from .models import *

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    user_id = request.session.get('id')
    menus = Menu.objects.all()
    products_list = products.objects.all()
    product_detail = pdetails.objects.all()
    blog_detail = blogs.objects.all()
    return render(request, 'index.html',{'menus':menus,'products_list':products_list,'product_detail':product_detail,'blog_detail':blog_detail,'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def shopPage(request):
    user_id = request.session.get('id')
    shop_detail = shop.objects.all()
    return render(request,'shop.html',{'shop_detail':shop_detail,'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def aboutus(request):
    user_id = request.session.get('id')
    about_us = About.objects.all()
    return render(request,'about.html',{'about_us':about_us,'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Blog(request):
    user_id = request.session.get('id')
    blog_detail = blog_list.objects.all()
    return render(request,'blog.html',{'blog_detail':blog_detail,'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Ourservice(request):
    user_id = request.session.get('id')
    services = products.objects.all()
    return render(request,'services.html',{'services':services,'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contact(request):
    user_id = request.session.get('id')
    if not user_id:
        messages.error(request, 'User not found in the Register table!!! Please Register or login')
        return redirect('login')
    else:
        return render(request,'contact.html',{'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_view(request):
    user_id = request.session.get('id')
    if not user_id:
        messages.error(request, 'User not found in the Register table! Please register or login.')
        return redirect('login')

    myid = request.GET.get('cartid')  

    if myid:
        product = shop.objects.filter(id=myid).first()
        if product:
            cart_item = addCart.objects.filter(name=product.name).first()

            if cart_item:
                cart_item.quantity += 1
                cart_item.total = cart_item.price * cart_item.quantity
                cart_item.save()  
                messages.success(request, f'Increased quantity of {product.name} in the cart.')
            else:
                cart_item = addCart(
                    image=product.image,
                    name=product.name,
                    price=product.price,
                    quantity=1,
                    total=product.price  
                )
                cart_item.save()  
                messages.success(request, f'Added {product.name} to the cart.')

        else:
            messages.error(request, 'Product not found.')

    cart_items = addCart.objects.all()

    subtotal = sum(item.total for item in cart_items)
    total = subtotal 

    return render(request, 'cart.html', {
        "cart_items": cart_items,
        'subtotal': subtotal,
        'total': total,
        'user_id': user_id
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delcart(request):
    cartid = request.GET.get('cartid')
    if cartid:
        cart_item = addCart.objects.filter(id=cartid).first()
        if cart_item:
            cart_item.delete()
    return redirect('cart_view')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_cart_quantity(request):
    cartid = request.POST.get('cartid')
    action = request.POST.get('action')
    cart_item = addCart.objects.filter(id=cartid).first()
    if cart_item:
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            cart_item.quantity -= 1
        
        cart_item.total = cart_item.price * cart_item.quantity
        cart_item.save()
    all=addCart.objects.all()
    print(all)
    return redirect('cart_view')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkOut(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')
    else:
        if request.method == 'POST':
            print('Received Post request')
            print(request.POST)
            country = request.POST.get('country')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            email = request.POST.get('email')
            print(email)
            phone = request.POST.get('phone')

            if not email:
                messages.error(request, 'Email is required.')
                return render(request, 'checkout.html', {'user_id': user_id})
            else:
            
                if not register_data.objects.filter(email=email).exists():
                    messages.error(request, 'User not found in the Register table!!! Please Register or login')
                    return redirect('checkout')
                else:
                    if bill_detail.objects.filter(email=email).exists():
                        messages.error(request, 'This email is already used! Please try with another email.')
                        return redirect('checkout')
                    else:
                        detail = bill_detail(
                            country=country, first_name=first_name, last_name=last_name,
                            address=address, city=city, state=state, zip=zip, email=email, phone=phone) 
                        detail.save()
            
            
        if request.method == 'POST':
            print(request.POST)
            ship_country = request.POST.get('ship_country')
            ship_address = request.POST.get('ship_address')
            ship_city = request.POST.get('ship_city')
            ship_state = request.POST.get('ship_state')
            ship_zip = request.POST.get('ship_zip')
            ship_phone = request.POST.get('ship_phone')

            if ship_country and ship_address and ship_city and ship_state and ship_zip:
                ship_detail = ship_detail(
                ship_country=ship_country, ship_address=ship_address, ship_city=ship_city, 
                ship_state=ship_state, ship_zip=ship_zip, ship_phone=ship_phone
                )
                ship_detail.save()

            request.session['email'] = email
            return redirect('order_view')
        return render(request, 'checkout.html',{'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_view(request):
    user_id = request.session.get('id')
    print('orders')
    alll=addCart.objects.all()
    subtotal = sum(i.total for i in alll)
    total = subtotal
    return render(request,'order.html',{"alll":alll,"subtotal":subtotal,"total":total,'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_view(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')
    else:
        if request.method == 'POST':
            payment_method = request.POST.get('payment_method')

            if payment_method == 'creditdebit':
                print('card')
                cardnumber = request.POST.get('cardnumber')
                cardholder = request.POST.get('cardholder')
                expirydate = request.POST.get('expirydate')

                if cardnumber and cardholder and expirydate:
                    print('Payment Done')
                    addCart.objects.all().delete()
                    return redirect('/thanks/')
                else:
                    return render(request, 'order.html', {'error': 'Please fill out all required    fields for credit/debit card.'})

            elif payment_method == 'netbanking':
                print('netbanking')
                account_number = request.POST.get('account_number')
                account_holder = request.POST.get('account_holder')

                if account_number and account_holder:
                    print('Payment Done')
                    addCart.objects.all().delete()
                    return redirect('/thanks')
                else:
                    return render(request, 'order.html', {'error': 'Please fill out all required    fields for net banking.'})

            elif payment_method == 'UPI':
                print('upi')
                upi_id = request.POST.get('upi')

                if upi_id:
                    print('Payment Done')
                    addCart.objects.all().delete()
                    return redirect('/thanks')
                else:
                    return render(request, 'order.html', {'error': 'Please provide your UPI ID.'})

            else:
                return render(request, 'order.html', {'error': 'Unknown payment method selected.'})

        return render(request, 'order.html',{'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def thankyou(request):
    user_id = request.session.get('id')
    return render(request,'thankyou.html',{'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_user(request):
    user_id = request.session.get('id')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        user = register_data(username=username,email=email,password=password,cpassword=cpassword)
        user.save()
        
        return redirect('login')
    return render(request,'register.html',{'user_id':user_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user(request):
    print('function called')
    if request.method == 'POST':
        print('received request')
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        print('Email:', email)
        print('Password:', password)

        try:
            log = register_data.objects.get(email=email)
            print('ID:', log.id)

            if password == log.password.strip():
                request.session['id'] = log.id
                print('Login successful, session set')
                return redirect('/')
            else:
                print('Invalid password')
                messages.error(request, 'Invalid Email or Password')
                return redirect('login')
        except register_data.DoesNotExist:
            print('User does not exist')
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')

    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    del request.session['id'] 
    addCart.objects.all().delete()   
    print('deleted')
    return redirect('/')        