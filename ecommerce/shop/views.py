from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category,Product
from shop.forms import RegisterForm,LoginForm,AddproductForm,AddcategoryForm,AddstockForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

class Categoryview(View):
    def get(self,request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request,'categories.html',context)

class Productsview(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'categories':c}
        return render(request,'products.html',context)

class ProductDetailview(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'productdetails.html',context)


class Registerview(View):
    def get(self,request):
        form_instance=RegisterForm()
        context={'form':form_instance}
        return render(request,'register.html',context)
    def post(self,request):
        form_instance=RegisterForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:login')
        else:
            context={'form':form_instance}
            return render(request,'register.html',context)

class Loginview(View):
    def get(self,request):
        form_instance=LoginForm()
        context={'form':form_instance}
        return render(request,'login.html',context)
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.cleaned_data['username']
            p=form_instance.cleaned_data['password']
            user=authenticate(username=u,password=p)
            if user and user.is_superuser==True:
                login(request,user)
                return redirect('shop:category')
            elif user and user.is_superuser==False:
                login(request,user)
                return redirect('shop:category')
            else:
                messages.error(request,"Invalid user credentials")
                return render(request,'login.html',{'form':form_instance})
        else:
            context={'form':form_instance}
            return render(request,'login.html',context)

class Logoutview(View):
    def get(self,request):
        logout(request)
        return redirect('shop:login')

class Addproductview(View):
    def get(self,request):
        form_instance=AddproductForm()
        context={'form':form_instance}
        return render(request,"Addproducts.html",context)
    def post(self,request):
        form_instance=AddproductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            context={'form':form_instance}
            return render(request,'Addproducts.html',context)

class Addcategoryview(View):
    def get(self,request):
        form_instance=AddcategoryForm()
        context={'form':form_instance}
        return render(request,"Addcategory.html",context)
    def post(self,request):
        form_instance=AddcategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            context={'form':form_instance}
            return render(request,'Addcategory.html',context)

class Addstockview(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=AddstockForm(instance=p)
        context={'form':form_instance}
        return render(request,'Addstock.html',context)
    def post(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=AddstockForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
