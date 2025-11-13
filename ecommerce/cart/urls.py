
from django.urls import path
from cart import views
app_name='cart'

urlpatterns = [
    path('addtocart/<int:i>',views.Addtocart.as_view(),name='addtocart'),
    path('cartview',views.Cartview.as_view(),name='cartview'),
    path('addtocart/<int:i>', views.Addtocart.as_view(), name='addtocart'),
    path('reduceitem/<int:i>', views.Reduceitemview.as_view(), name='reduceitem'),
    path('deleteitem/<int:i>', views.Removeitemview.as_view(), name='removeitem'),
    path('checkout', views.Checkoutview.as_view(), name='checkout'),
    path('payment', views.Paymentview.as_view(), name='payment'),
    path('paymentsuccess/<i>', views.PaymentsuccessView.as_view(), name='payment_success'),
    path('yourorders', views.OrdersView.as_view(), name='orders'),
]
