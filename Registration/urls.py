from Registration import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('',views.reg,name='reg'),
    path('login_user',views.login_user,name='login_user'), 
    path('home',views.home,name='home'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('gallary',views.gallary,name='gallary'),
    path('contact',views.contact,name='contact'),
    path('forgot',views.forgot,name='forgot'),   
    path('home1',views.home1,name='home1'),
    path('email',views.email,name='email'),
    path('forgotpassword/<str:uidb64>/<str:token>/', views.forgotpassword, name='forgotpassword'),
    path('pin',views.pin,name='pin'),
    path('departments',views.departments,name='departments'),
    path('fooditem',views.fooditem,name='fooditem'),
    path('food',views.food,name='food'),
    path('view_items',views.view_items,name='view_items'),
    
    
    

]