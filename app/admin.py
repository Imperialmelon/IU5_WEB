from django.contrib import admin
from .models import Cargo, Shipping, Shipping_Cargo
admin.site.register(Cargo)
admin.site.register(Shipping)
admin.site.register(Shipping_Cargo)
# Register your models here.
