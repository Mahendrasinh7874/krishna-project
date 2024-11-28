from django.contrib import admin
from.models import *
# Register your models here.

class showregister(admin.ModelAdmin):
    list_display =["username","emailaddress"]

admin.site.register(register,showregister)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(CartItem)
admin.site.register(OrderedItems)
