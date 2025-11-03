from django.shortcuts import render,redirect
from django.views import View
from cart.models import Cart
from shop.models import Product
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
        context={'cart':c}
        return render(request,'cartview.html',context)

class Reduceitemview(View):
    def get(self,request,i):
        u=request.user
        p=Cart.objects.get(user=u,product=i)
        if p.quantity==1:
            return redirect('cart:removeitem',i=i)
        else:
            p.quantity-=1
            p.save()
            return redirect('cart:cartview')
class Removeitemview(View):
    def get(self,request,i):
        u=request.user
        p=Cart.objects.get(user=u,product=i)
        p.delete()
        return redirect('cart:cartview')
