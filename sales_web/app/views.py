from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomerInfo, Product
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import requires_csrf_token

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                
                customer_info = CustomerInfo(
                    user=user,
                    name=name,
                    phone=request.POST.get('phone', ''),
                    address=request.POST.get('address', ''),
                    date_of_birth=request.POST.get('date_of_birth', None),
                    profile_picture=request.FILES.get('profile_picture', None)
                )
                customer_info.save()
                
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def edit_profile(request):
    customer_info = request.user.customerinfo
    if request.method == 'POST':
        # Update user information
        request.user.email = request.POST.get('email')
        request.user.save()

        # Update customer information
        customer_info.name = request.POST.get('name')
        customer_info.phone = request.POST.get('phone')
        customer_info.address = request.POST.get('address')
        customer_info.date_of_birth = request.POST.get('date_of_birth') or None

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            customer_info.profile_picture = request.FILES['profile_picture']

        customer_info.save()

        # Handle password change
        if request.POST.get('old_password'):
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your profile and password were successfully updated.')
            else:
                messages.error(request, 'Please correct the error in the password form.')
        else:
            messages.success(request, 'Your profile was successfully updated.')

        return redirect('edit_profile')
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'edit_profile.html', {
        'customer_info': customer_info,
        'password_form': password_form
    })

@requires_csrf_token
def csrf_failure(request, reason=""):
    context = {'reason': reason}
    return render(request, 'csrf_failure.html', context, status=403)

