from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render 
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