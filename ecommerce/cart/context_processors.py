from cart.models import Cart

def totalproducts(request):
    products=0
    try:
        u=request.user
        C=Cart.objects.filter(user=u)
        for i in C:
            products+=i.quantity
    except:
        products=0
    return {'products':products}
