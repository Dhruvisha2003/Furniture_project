"""
URL configuration for Git_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('Shop/',views.shopPage,name='shop'),
    path('About/',views.aboutus,name='aboutus'), 
    path('Services/',views.Ourservice,name='services'),
    path('Blog/',views.Blog,name='Ourblog'),
    path('Contact/',views.contact,name='contactUs'),
    path('CartPage/', views.cart_view, name='cart_view'),
    path('Delete_cart/', views.delcart, name='delete'),
    path('Update_cart/', views.update_cart_quantity, name='update_cart'),
    path('Register/',views.register_user,name='register'),
    path('Login/',views.login_user,name='login'),
    path('Logout/', views.logout, name='logout'),
    path('Checkout/',views.checkOut,name='checkout'),
    path('Order/',views.order_view,name='order_view'),
    path('Payment/',views.payment_view,name='payment'),
    path('Thanks/',views.thankyou,name='thanks'),

]
