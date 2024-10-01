from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomerInfo, Product
from django import forms
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import requires_csrf_token
from .models import Cart, CartItem, Product
import os
from django.http import HttpResponse, Http404
from django.conf import settings

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

@login_required
def cart_list(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user) 
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product) 
    if not created: 
        cart_item.quantity += 1  
        cart_item.save() 
    cart_item.save() 
    return redirect('cart_list') 

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart = cart, product_id = product_id)
    cart_item.delete()
    return redirect('cart_list')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

from mimetypes import guess_type
from django.utils.html import escape

def view_file(request):
    file_path = request.GET.get('documents', '')
    
    if file_path.startswith('/media'):
        file_path = file_path[6:]
    
    file_path = os.path.normpath(file_path.lstrip('/'))
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if not os.path.exists(full_path):
        raise Http404("File not found")
    
    if not os.path.commonpath([settings.MEDIA_ROOT, full_path]) == settings.MEDIA_ROOT:
        raise Http404("Access denied")
    
    try:
        content_type, _ = guess_type(full_path)
        
        if content_type and content_type.startswith('text') or full_path.endswith(('.log', '.txt', '.csv', '.md', '.py', '.js', '.css', '.html')):
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                # Nếu UTF-8 không hoạt động, thử với ISO-8859-1
                with open(full_path, 'r', encoding='iso-8859-1') as file:
                    content = file.read()
            content = escape(content)
            html_content = f"<pre style='white-space: pre-wrap; word-wrap: break-word;'>{content}</pre>"
            return HttpResponse(html_content, content_type='text/html')
        else:
            with open(full_path, 'rb') as file:
                file_content = file.read()
            
            if not content_type:
                content_type = 'application/octet-stream'
            
            response = HttpResponse(file_content, content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(full_path)}"'
            return response
        
    except IOError as e:
        print(f"IOError: {e}")
        raise Http404("File not found")                          