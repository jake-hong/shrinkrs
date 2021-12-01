from django.contrib.auth.forms import AuthenticationForm
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render 
from shortener.models import Users
from shortener.forms import RegisterForm
from django.contrib.auth import authenticate,login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    # print(request.user.pay_plan.name)
    user = Users.objects.filter(id=request.user.id).first()
    email = user.email if user else "anonyumous user!"
    print("Logged in?",  request.user.is_authenticated)
    # print(request.user.pay_plan.name)
    
    if request.user.is_authenticated is False:
        email = "anonymous user!"
        print(email)
    return render(request, "base.html",{"welcome_msg":f"hello"})


@csrf_exempt # 사이트 위변조 방지 
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
            form.save()
            username = form.cleaned_data.get("username")
            raw_pw = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_pw)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            msg="로그인 성공"
        return render(request, "register.html", {"form":form,"msg":msg})
    else:
        form = RegisterForm()
        return render(request,"register.html",{"form":form})  

def login_view(request):
    if request.method =="POST":
        form = AuthenticationForm(request, request.POST)
        msg = "로그인 정보가 잘못 되었습니다. 가입하지 않으셨다면 회원 가입을 진행해주세요."
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_pw = form.cleaned_data.get("password")
            user = authenticate(username=username,password=raw_pw)
            if user is not None:
                msg = "로그인 성공"
                login(request,user)
        return render(request, "login.html", {"form":form, "msg":msg})
    else:
        form = AuthenticationForm()         
        return render(request, "login.html",{"form":form}) 

def logout_view(request):
    logout(request)
    return redirect("index")

# @login_required
def list_view(request):
    page= int(request.GET.get("p",1))
    users = Users.objects.all().order_by("id")
    paginator = Paginator(users,10)
    users = paginator.get_page(page)
    return render(request,"board.html",{"users":users})