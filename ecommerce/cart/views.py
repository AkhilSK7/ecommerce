from django.contrib.messages.context_processors import messages
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from cart.models import Order,Order_items,Cart
from shop.models import Product
import razorpay
import uuid
# Create your views here.

class Addtocart(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)#checks whether the product already placed by current user
            c.quantity+=1#or checks whether the product is there in the cart table
            c.save()#if yes increments  the quantity by 1
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)#else creates a new cart record inside cart table
            c.save()
        return redirect('cart:cartview')

class Cartview(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.subtotal()

        context={'cart':c,'total':total}
        return render(request,'cartview.html',context)

class Reduceitemview(View):
    def get(self,request,i):
        u=request.user
        try:
            p = Cart.objects.get(user=u, product=i)
            if p.quantity>1:
                p.quantity -= 1
                p.save()
            else:
              p.delete()
        except:
            pass
        return redirect('cart:cartview')
class Removeitemview(View):
    def get(self,request,i):
        u=request.user
        try:
            p=Cart.objects.get(user=u,product=i)
            p.delete()
        except:
            pass
        return redirect('cart:cartview')

from cart.forms import Orderform
from cart.models import Order_items,Order
from django.contrib import messages
def stock_available(c):
    stock=True
    for i in c:
        if i.product.stock < i.quantity:
            stock=False
            break
    else:
        stock=True
    return stock

class Checkoutview(View):
    def post(self,request):
        form_instance=Orderform(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user#current user
            o.user=u
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.subtotal()
            o.amount=total
            o.save()
            if (o.payment_method=="online"):
                #razorpay connection
                client=razorpay.Client(auth=('rzp_test_Rckyc30XnSl9Ws','B6yZJq6WY7sA8ZcShYMXS6Ai'))
                #place order
                response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                print(response_payment)
                id=response_payment['id']
                o.order_id=id
                o.save()
                context={'payment':response_payment}
                return render(request,'payment.html',context)
            else:
                o.is_ordered=True
                uid=uuid.uuid4().hex[:14]
                id="order_COD"+uid
                o.order_id=id
                o.save()
                for i in c:
                    items=Order_items.objects.create(order=o,product=i.product,quantity=i.quantity)
                    items.save()
                    items.product.stock -= items.quantity
                    items.product.save()
                c.delete()
                return render(request,'payment.html')
        return redirect('cart:payment')

    def get(self,request):
        u=request.user
        c = Cart.objects.filter(user=u)
        stock=stock_available(c)
        if stock:
            form_instance=Orderform()
            context={'form':form_instance}
            return render(request,'checkoutform.html',context)
        else:
            messages.error(request,"can't place order")
            return render(request, 'checkoutform.html')

class Paymentview(View):
    def get(self,request):
        return render(request,'payment.html')

from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt,name="dispatch")
class PaymentsuccessView(View):
    def post(self,request,i):#here i represents the username
        u=User.objects.get(username=i)#to add user into current session again
        login(request,u)#add the user again into session
        response=request.POST
        print(response)
        id=response['razorpay_order_id']
        print(id)
        order=Order.objects.get(order_id=id)
        order.is_ordered=True
        order.save()
        c=Cart.objects.filter(user=u)
        for i in c:
            o=Order_items.objects.create(order=order,product=i.product,quantity=i.quantity)
            o.save()
            o.product.stock-=o.quantity
            o.product.save()
        c.delete()
        return render(request,'paymentsuccess.html')

class OrdersView(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'order':o}
        return render(request,'orders.html',context)