from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Customer(models.Model):
    usern=models.OneToOneField(User, on_delete=models.CASCADE, max_length=80, unique=True, blank=True)
    fname=models.CharField(max_length=80, blank=True)
    email=models.EmailField(max_length=80, unique=True)
    #password=models.CharField(max_length=200)
    gender=models.CharField(max_length=20)
    mobile=models.CharField(max_length=11, null=False)
    address=models.CharField(max_length=100, null=False)
    city=models.CharField(max_length=100, null=False)
    state=models.CharField(max_length=100, null=False)

    def __str__(self):
        return str(self.fname)
    

class Mycar(models.Model):
    cust=models.ForeignKey(Customer, max_length=100, blank=True, null=True, on_delete=models.SET_NULL)
    car_num=models.CharField(max_length=10, unique=True)
    company=models.CharField(max_length=30)
    car_name=models.CharField(max_length=30)
    car_type=models.CharField(max_length=30)
    from_place=models.CharField(max_length=30)
    to_place=models.CharField(max_length=30)
    from_date=models.DateField(null=True)
    to_date=models.DateField(null=True)
    price=models.FloatField()
    car_img = models.ImageField(upload_to="cars",default="", null = True,blank = True)

    def __str__(self):
        return self.car_num
    
    @property
    def imageURL(self):
        try:
            url = self.car_img.url
        except:
            url = ''
        return url


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.car_img.path)
        if img.height > 1500 or img.width > 1500:
            output_size = (1500, 1500)
            img.thumbnail(output_size)
            img.save(self.car_img.path)

class ContactUs(models.Model):
    name=models.CharField(max_length=80)
    email=models.EmailField(max_length=80, unique=True, blank=False)
    phone=models.CharField(max_length=11, null=False, blank=True)
    msg=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Booking(models.Model):
    name=models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
    car=models.ForeignKey(Mycar,on_delete=models.SET_NULL, null=True)
    contact=models.CharField(max_length=11,null=False)
    email=models.EmailField(max_length=80)
    pickup=models.DateField()
    dropoff=models.DateField()
    pick_add=models.CharField(max_length=100, null=False)
    drop_add=models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)