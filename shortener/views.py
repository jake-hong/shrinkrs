from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render 
from shortener.models import Users
from shortener.forms import RegisterForm
from django.contrib.auth import authenticate,login

# Create your views here.
def index(request):
    print("hello")
    user = Users.objects.filter(id=request.user.id).first()
    email = user.email if user else "anonyumous user!"
    print(email)
    print("Logged in?",  request.user.is_authenticated)
    # print(request.user.pay_plan.name)
    
    if request.user.is_authenticated is False:
        email = "anonymous user!"
        print(email)
    return render(request, "base.html",{"welcome_msg":f"hello{user}"}
    )

@csrf_exempt
def get_user(request,user_id):
    print(user_id)
    
    if request.method =="GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request,"base.html",{"user":user,"params":[abc,xyz]})
    
    elif request.method == "POST":
        username = request.GET.get("username")
        if username :
            user = Users.objects.filter(pk=user_id).update(username=username)
            return JsonResponse(status=201, data = dict(msg="You just reached with post method"), safe =False)

def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
        msg = "unvalid data"

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            raw_pw = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_pw)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            msg="Login Success"
        return render(request, "register.html", {"form":form,"msg":msg})
    else:
        form = RegisterForm()
        return render(request,"register.html",{"form":form})  