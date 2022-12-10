from crm.models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cnt=Cart.objects.filter(user=request.user).count()
        return {"cnt":cnt}
    else:
        return {"cnt":0}