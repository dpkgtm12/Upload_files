from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.http import HttpResponse 
from .forms import UploadFileForm
from.models import UploadedFile

def home(request):
    if request.method == 'POST' :
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_file = request.FILES["file"]
        if form.is_valid():
            instance = UploadedFile(file=request.FILES['file'],email=request.session["username"])
            instance.save()
            return redirect(home)
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})


@csrf_exempt
def register(request):
    if 'name' in request.session:
            return redirect(home)
    if request.method == "POST": 
        name = request.POST.get("name","default")
        email = request.POST.get("email","default")
        password = request.POST.get("password","default")
        if User.objects.filter(email = email).exists():
            return "User already exists"
        else:
            user=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            user.save()
            return redirect(login)
        
    if 'name' in request.session:
        del request.session['name']
        auth.logout(request)
    return render(request,"register.html")

@csrf_exempt
@never_cache
def login(request):
    if request.method == "POST":
        username=request.POST.get("username","default")
        password=request.POST.get("password","default")
        print(username, password)
        user=auth.authenticate(username=username,password=password)
        if user is None:
            return  HttpResponse("Invalid username or password")
        else:
            auth.login(request,user)
            d={"x":user.first_name}
            global email
            request.session['username'] = username
            request.session['name'] = user.first_name
            email=username
            return redirect(home)
    if 'name' in request.session:
        del request.session['name']
        auth.logout(request)
    return redirect(register)

def logout(request):
    del request.session['name']
    auth.logout(request)
    return redirect(home)

def myuploads(request):
    if "name" not in request.session:
        return redirect(home)
    data=UploadedFile.objects.filter(email=request.session["username"])
    for i in data:
        print(i)
    return render(request,"show_list.html",{"uploads":data})
