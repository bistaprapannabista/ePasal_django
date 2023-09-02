from django.urls import path
from store.views import IndexView,LoginView,SignupView, ProductDetailView, CartView, CheckoutView, OrderView, SearchView
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('',IndexView.as_view(),name="index"),
    path('product/<int:pk>',ProductDetailView.as_view(),name="product-detail"),
    path('login',LoginView.as_view(),name="login"),
    path('logout',LogoutView.as_view(next_page="login"),name='logout'),
    path('signup',SignupView.as_view(),name="signup"),
    path('cart',CartView.as_view(),name="cart"),
    path('checkout',CheckoutView.as_view(),name="checkout"),
    path('orders',OrderView.as_view(),name="orders"),
    path('search',SearchView.as_view(),name="search"),
]