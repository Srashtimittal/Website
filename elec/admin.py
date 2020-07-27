from django.contrib import admin
# Register your models here.
from .models import Good, Contact, Order, OrderUpdate
admin.site.register(Good)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
