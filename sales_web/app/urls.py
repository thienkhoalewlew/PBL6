from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('cart/', views.cart_list, name='cart_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-product/', views.add_product, name='add_product'),
    path('viewfile/', views.view_file, name='view_file'),
    path('checkout/', views.checkout, name='checkout'),
    path('check_log/', views.check_log, name ='check_log'),
    # ... other URL patterns ...
]
