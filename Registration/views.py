from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from Registration.models import *
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
import random
from django.db.models import Q

def reg(request):
    if request.method=='POST':
        firstname=request.POST.get('first_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm=request.POST.get('c_password')
        address=request.POST.get('address')
        contact=request.POST.get('contact')
        if password != confirm:
            return render(request, 'Register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(email=email).exists():
            return render(request, 'Register.html', {'error': 'Email is already registered'})
        password = make_password(password)
        datanames=User.objects.create(first_name=firstname,email=email,password=password,username=username)
        datanames.save()
        data=register(address=address,contact=contact,user=datanames)
        data.save()
        return redirect('login_user')
    return render(request,'Register.html')


def login_user(request):
     if request.method=='POST':
       
        username=request.POST.get('user')
       
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            
            return redirect('home')
        else:
            return render(request,'login.html',{'error': 'invalid username or password'})
     return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def home1(request):
    return render(request,'home1.html')
def logout_user(request):
   uname=request.session.get('uid')
   request.session.clear()
   django_logout(request)
   return redirect('reg')

def gallary(request):
    
    return render(request,'gallary.html')

def contact(request):
   
    return render(request,'contact.html')

def forgot(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        # if current_password != new_password:
        #     return render(request, 'forgot.html', {'error': 'Passwords do not match'})
        
        user = authenticate(password=current_password,username=username)
        
        if user is not None:
            user.set_password(new_password)
            user.save()
            print("Password updated successfully. Redirecting to home page.")
            return render(request,'home.html',{'user':user}) 
        else:
            messages.error(request, 'Invalid username or current password.')
            print("Authentication failed. Not redirecting to home page.")
           
    return render(request,'forgot.html')
   

   


def email(request):
    if request.method == 'POST':
        email = request.POST['email']
        request.session['email']=email
        user = User.objects.get(email=email)
        
        pin = ""
        for i in range(6):
            number = random.randint(1, 9)
            pin += str(number)
            request.session['pno']=pin
        # # Construct the password reset link
        # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # # reset_link = request.build_absolute_uri(reverse('forgotpassword', kwargs={'uidb64': uidb64, 'token':pin}))
        # reset_link = request.build_absolute_uri(reverse('forgotpassword', kwargs={'uidb64': uidb64, 'token':pin}))
       
        # # Send the password reset link via email
        subject = 'Password Reset'
        message = f"Hello {user.username},\n\nYou recently requested to reset your password. Please type 6 digit pin  to continue with the password reset:\n{pin}\n\nIf you did not request this reset, please ignore this email.\n\nThank you!"
        send_mail(subject, message, 'joyboynikaman921@gmail.com', [email])
        
        return redirect('pin')
    
    return render(request,'email.html')

def pin(request):
    email=request.session.get('email')
    user = User.objects.get(email=email)
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    
    if request.method == 'POST':
            pin_number = request.POST.get('pin')
            pin_session=request.session.get('pno')
            
            
            if pin_number == pin_session :
                reset_link = request.build_absolute_uri(reverse('forgotpassword', kwargs={'uidb64': uidb64, 'token':token}))
                return redirect(reset_link)
            else:
                messages.error(request, 'Invalid PIN or session data missing')
                return redirect('pin')
           
    return render(request,'pin.html')

def forgotpassword(request,uidb64,token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)
    request.session['uidb64']=str(uidb64)
    request.session['token']=token
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('newpassword')
            confirm_password = request.POST.get('confirmpassword')
            
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                print( 'Your password has been successfully reset')
                return redirect('login_user')  # Redirect to the login page after successful password reset
            else:
                messages.error(request, 'invalid username or password')
                return redirect('forgotpassword', uidb64=uidb64, token=token)
        else:
            return render(request, 'forgotpassword.html')
           
    return render(request,'forgotpassword.html')
          
def departments(request):
    if request.method=='POST':
        dept=request.POST['department']
        data=department(department=dept)
        data.save()
    return render(request,'department.html')


def fooditem(request):
    dept=department.objects.all()
    if request.method=='POST':
        food=request.POST['fooditem']
        image=request.FILES.get('image')
        dept_id = request.POST['dept']
        deptname=department.objects.get(id=dept_id)
        data=foods(fooditem=food,image=image,dept=deptname)
        data.save()
    return render(request,'fooditem.html',{'d': dept})

def view_items(request):
    search_query=request.GET.get('search')
    if  search_query:
       items = foods.objects.filter(Q(dept__department__iexact=search_query)| Q(fooditem__iexact=search_query) )
       
    else:
        items=foods.objects.all()
    return render(request,'view_items.html',{'v':items})



def food(request):
    dept=department.objects.all()
    food=foods.objects.all()
    return render(request,'foods.html',{'d':dept,'f':food})