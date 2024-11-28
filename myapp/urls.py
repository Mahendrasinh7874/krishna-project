from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('Payment',views.Payment,name='Payment'),
    path('Product',views.Products,name='Product'),
    path('contact',views.contact,   name='contact'),
    path('services',views.services,name='services'),
    path('cart',views.cart,name='cart'),
    path('add-cart/', views.add_cart, name='add_cart'),
    path('show-cart/', views.show_cart, name='show-cart'),  # Use hyphen in name
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('ProductDetail/<int:pk>', views.ProductDetail, name="ProductDetail"),
    path('adduser', views.adduser, name='adduser'),
    path('signup',views.signup,name="signup"),
    path('removeitem/<int:pk>/', views.removeitem, name='removeitem'),
    # path('update-cart',views.update_cart),
    path('show-cart/update-cart/', views.update_cart, name='update-cart'),  # Ensure this has a trailing slash
    path('pay/<int:amount>',views.Payment,name='pay'),
    path('confirm-order',views.ConfirmOrder,name='confirm-order'),
    path('Orders', views.orders, name="Orders"),
    path('Getorder',views.getorders,name='Getorder'),

    # path('initiate-payment/<int:amount>/', views.initiate_payment, name='initiate_payment'),
    # path('payment-success/', views.payment_success, name='payment_success'),
    # path('payment-failed/', views.payment_failed, name='payment_failed'),
      path('initiate-payment/<int:amount>/', views.initiate_payment, name='initiate_payment'),
      path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    ]