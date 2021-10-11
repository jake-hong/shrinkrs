from django.shortcuts import render, redirect 
from shortener.models import Users

# Create your views here.
def index(request):
    user = Users.objects.filter(username="admin").first()
    email = user.email if user else "anonyumous user!"
    print(email)
    print(request.user.is_authenticated)
    if request.user.is_authenticated is False:
        email = "anonymous user!"
        print(email)
    return render(request, "base.html",{"welcome_msg":f"hello{user}"}
    )