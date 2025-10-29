
from django.urls import path
from shop import views
app_name='shop'

urlpatterns = [
    path('',views.Categoryview.as_view(),name='category'),
    path('products/<int:i>', views.Productsview.as_view(), name='products'),
]
