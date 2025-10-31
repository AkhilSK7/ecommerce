
from django.urls import path
from shop import views
app_name='shop'

urlpatterns = [
    path('',views.Categoryview.as_view(),name='category'),
    path('products/<int:i>', views.Productsview.as_view(), name='products'),
    path('productdetails/<int:i>',views.ProductDetailview.as_view(),name='productdetails'),
    path('register',views.Registerview.as_view(),name='register'),
    path('login',views.Loginview.as_view(),name='login'),
    path('logout', views.Logoutview.as_view(), name='logout'),
]
