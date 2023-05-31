from django.shortcuts import render, redirect
from django.views import View
import mysql.connector as sql
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from requests import request
from django.contrib.auth.hashers import make_password
from website.models import Customer, Mycar, ContactUs, Booking
from django.contrib.auth.decorators import login_required

# Create your views here.
#Home page
def home(request):
    return render(request, "home.html")

#Function to help login the user and open dashboard
def LoginUser(request):
    if request.method=="GET":
        return render(request, "login.html")

    if request.method=="POST":
        m=sql.connect(host="localhost", user="root", passwd="prachi26", database='carpooling')
        usern=request.POST['usern']
        password=request.POST['password']

        try:
            user = authenticate(username=usern, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password!")
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Invalid username!")
            return redirect('login')
    return render(request, "login.html")


#Function to help register the user
def Register(request):
    if request.method == 'GET':
        return render(request,"registration.html")

    if request.method == 'POST':
        m=sql.connect(host="localhost", user="root", passwd="prachi26", database='carpooling')
        usern=request.POST['usern']
        fname=request.POST['fname']
        email=request.POST['email']
        password=request.POST['password']
        mobile=request.POST['mobile']
        gender=request.POST['gender']
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        if len(mobile)!=10 or mobile.isdigit()==False:
            messages.warning(request, "The phone number provided is not 10 digits!")
        elif mobile.startswith(('1', '2', '3', '4', '5', '0')):
            messages.warning(request, "The phone number provided is not valid!")
        else:
            try:
                obj=User.objects.create_user(usern, email, password)
                obj.save()
                cust=Customer.objects.create(usern=obj,fname=fname,email=email,mobile=mobile,gender=gender,address=address,city=city,state=state) 
                cust.save()
                m.commit()
                #messages.success(request, "Account created successfully!")
                return redirect('login') 
            except IntegrityError:
                messages.warning(request, "Account already exists!")
                return redirect('register')
        return render(request,"registration.html")


#Function to help user contact the admin
def Contactus(request):
    if request.method=="GET":
        return render(request, "contact.html")
    
    if request.method=="POST":
        m=sql.connect(host="localhost", user="root", passwd="prachi26", database='carpooling')
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        msg=request.POST['msg']
        if len(phone)!=10 or phone.isdigit()==False:
            messages.warning(request, "The phone number provided is not 10 digits!")
        elif phone.startswith(('1', '2', '3', '4', '5', '0')):
            messages.warning(request, "The phone number provided is not valid!")
        else:
            contact_us = ContactUs.objects.create(name=name, email=email, phone=phone, msg=msg)

        
        # save the contact details in database
            #print(request.user)
            #customer = Customer.objects.get(usern=user_name)
            #    contact_us = ContactUs.objects.create(name=name, email=email, phone=phone, msg=msg, cust=customer)
            #else:
            #    contact_us = ContactUs.objects.create(name=name, email=email, phone=phone, msg=msg, cust=None)

            #print(contact_us)
            contact_us.save()
            m.commit()
            messages.success(request, "Thank you for contacting us, we will reach you soon.")

        return render(request, "contact.html")


#Function to search the car on search.html page and redirect to the searched_cars.html
def Search(request):
    if request.method=="GET":
        return render(request, "search.html")
    
    if request.method=="POST":
        m=sql.connect(host="localhost", user="root", passwd="prachi26", database='carpooling')
        from_place=request.POST['from_place']
        to_place=request.POST['to_place']
        from_date=request.POST['from_date']
        to_date=request.POST['to_date']
        cars = Mycar.objects.filter(from_place=from_place,to_place=to_place,from_date=from_date, to_date=to_date)
        print(cars)
        context = {'cars': cars}
        return render(request, "searched_cars.html", context)
        



#Function to show details of the car to the user, but if the user is not logged in then take to login page    
@login_required(login_url='login')
def Cardetails(request,car_id):
    if request.method=="GET":
        car=Mycar.objects.get(pk=car_id)
        context={'car':car}
        return render(request,"cardetails.html",context)
    
    #Function to book the car
    if request.method=="POST":
        m=sql.connect(host="localhost", user="root", passwd="prachi26", database='carpooling')
        #name=request.POST['name']
        contact=request.POST['contact']
        email=request.POST['email']
        pickup=request.POST['pickup']
        dropoff=request.POST['dropoff']
        pick_add=request.POST['pick_add']
        drop_add=request.POST['drop_add']
        if len(contact)!=10 or contact.isdigit()==False:
            messages.warning(request, "The phone number provided is not 10 digits!")
        elif contact.startswith(('1', '2', '3', '4', '5', '0')):
            messages.warning(request, "The phone number provided is not valid!")
        else:
            user = request.user
            print(user)
            cust=Customer.objects.get(usern=user)
            print(cust)
            car=Mycar.objects.get(pk=car_id)
            overlap_bookings = Booking.objects.filter(car=car, pickup=pickup, dropoff=dropoff)
            if overlap_bookings.exists():
                messages.error(request, "The car is not available for the selected dates.")
                return redirect('cardetails', car_id=car_id)
            
            cars = Booking.objects.create(name=cust, car=car, email=email, contact=contact,pickup=pickup,dropoff=dropoff,pick_add=pick_add,drop_add=drop_add)
            cars.save()
            m.commit()
            #messages.success(request, "Your booking has been submitted successfully!")
            return redirect('bookedcar', car_id=car_id)
    return redirect('cardetails', car_id=car_id)




#Function to show the booked cars, booked by the user
def Booked(request,car_id):
    if request.method=="GET":
        if request.user.is_authenticated:
            messages.success(request, "Your booking has been done successfully!")
            user = request.user
            cust=Customer.objects.get(usern=user)
            
            book=Booking.objects.get(car=car_id, name=cust)
            print(book)
            context={'book':book}
            return render(request, "booked.html", context)




#Function to show dashboard to the logged in users
def dash(request):
    if request.user.is_authenticated:
        print(request.user)
        return render(request, "dashboard.html")



#Function to show logged in user's bookings from the dashboard
def MyBookings(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user=request.user
            cust=Customer.objects.get(usern=user)
            custs=Booking.objects.filter(name=cust)
            print(custs)
            context={'custs':custs}
            return render(request, "mybooking.html",context)
    #if request.method == 'POST':
    #    if request.user.is_authenticated:
    #       user=request.user
    #        cust=Customer.objects.get(usern=user)
    #        custs=Booking.objects.get(name=cust)
    #        print(custs)
    #        context={'custs':custs}
    #        return render(request, "mybooking.html",context)



#Function to show logged in user's account details
def MyAccount(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            cust=Customer.objects.get(usern=user)
            #print(cust)
            context={'cust': cust}
            return render(request, "myaccount.html", context)



#Function to show logged in user's cars booked by other customer's
def CustomerBookings(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user=request.user
            cust=Customer.objects.get(usern=user)
            mybook=Booking.objects.filter(name=cust)
            mycar=Mycar.objects.filter(cust=cust)
            otherbookings=Booking.objects.filter(car__in=mycar).exclude(name=cust)
            context={'otherbookings':otherbookings}
            return render(request, "cust_booking.html", context)




#Function to show logged in user, their added cars
def MyCarList(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            username=Customer.objects.get(usern=user)
            custs=Mycar.objects.filter(cust=username)
            print(custs)
            context={'custs': custs}
            return render(request, "mycar_list.html", context)



#Function to show all the cars to the logged in or unloggedin users on the allcars.html
def Cars(request):
    if request.method == 'GET':
        mycars=Mycar.objects.all()
        context={'mycars': mycars}
        return render(request, "allcars.html", context)
    
    #if request.method == 'POST':
    #    if request.user.is_authenticated:
    #        return render("")



#Function to help logged in user to change password on change.html
def Change(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "change.html")
    
    if request.method=='POST':
        if request.user.is_authenticated:
            user=request.user
            print(user)
            old_password=request.POST['old_password']
            print(old_password)
            new_password = request.POST['new_password']
            print(new_password)
            confirm_password = request.POST['confirm_password']
            print(confirm_password)
            usern = authenticate(request, username=user, password=old_password)
            print(usern)
            if usern is None:
                messages.error(request, 'The old password is incorrect!')
                return redirect('changepassword')
            
            if new_password != confirm_password:
                messages.error(request, 'The new password and confirm password does not match!')
                return redirect('changepassword')
            
            print(user.password)
            user.password = make_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('changepassword')
    return render(request, 'change.html')
            
            
#Function to add user's car in the database
def Addcar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "addmycar.html")
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            m=sql.connect(host="localhost", user="root", passwd="prachi26", database='carpooling')
            car_num=request.POST['car_num']
            car_name=request.POST['car_name']
            from_place=request.POST['from_place']
            to_place=request.POST['to_place']
            car_type=request.POST['car_type']
            company=request.POST['company']
            price=request.POST['price']
            from_date=request.POST['from_date']
            to_date=request.POST['to_date']
            car_img=request.FILES['car_img']
            custom=Customer.objects.get(usern=request.user)
            print(custom)
            car=Mycar.objects.filter(car_num=car_num)
            if car.exists():
                messages.warning(request, 'Car Already exists')
                return redirect('addmycar')
            obj=Mycar.objects.create(car_num=car_num,from_date=from_date,to_date=to_date,car_name=car_name,from_place=from_place,to_place=to_place,car_type=car_type,company=company, price=price, car_img=car_img, cust=custom)
            obj.save()
            m.commit()
            return redirect('dashboard') 
                     
    return render(request,"addmycar.html")

def logout_user(request):
    if request.user.is_authenticated:
        #request.session.clear()
        #print('User is authenticated')
        logout(request)
    return redirect('home')
    