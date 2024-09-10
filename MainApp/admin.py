from django.contrib import admin
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
# from .models import order

admin.site.register(Menu)
admin.site.register(products)
admin.site.register(pdetails)
admin.site.register(shop)
admin.site.register(blogs)
admin.site.register(About)
admin.site.register(blog_list)
admin.site.register(register)
admin.site.register(addCart)
admin.site.register(data)
# admin.site.register(order)


