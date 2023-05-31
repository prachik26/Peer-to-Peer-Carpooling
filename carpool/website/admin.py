from django.contrib import admin
from website.models import Customer, Booking, ContactUs, Mycar

# Register your models here.
admin.site.register(Customer)
admin.site.register(Mycar)
admin.site.register(ContactUs)
admin.site.register(Booking)