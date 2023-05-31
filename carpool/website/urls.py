from django.urls import path
#from website.views import Cars
from website import views
urlpatterns=[
    path('',views.home, name="home"),
    path('login/', views.LoginUser, name="login"),
    path('register/', views.Register, name="register"),
    path('contact/', views.Contactus, name="contact"),
    path('dashboard/', views.dash, name="dashboard"),
    path('allcars/', views.Cars, name="allcars"),
    path('addmycar/', views.Addcar, name="addmycar"),
    path('mycar_list/', views.MyCarList, name="mycar_list"),
    path('changepassword/', views.Change, name="changepassword"),
    path('searchmycar/', views.Search, name="searchmycar"),
    path('cardetails/<int:car_id>/', views.Cardetails, name="cardetails"),
    path('bookedcar/<int:car_id>/',views.Booked,name="bookedcar"),
    path('mybookings/', views.MyBookings, name="mybookings"),
    path('myaccount', views.MyAccount,name="myaccount"),
    path('customerbookings/', views.CustomerBookings, name="customerbookings"),
    path('logout/',views.logout_user, name="logout"),
]