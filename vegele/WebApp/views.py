from django.shortcuts import render,redirect
from WebApp.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

@login_required
def receipe(request):
    if request.method=='POST':
        data=request.POST
        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_amount=data.get('receipe_amount')
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,
            receipe_amount=receipe_amount

        )
        print(receipe_amount)
        return redirect('/index/')
        
    return render(request,'myapp/receipe.html',{'context':receipe,})

@login_required
def index(request):
    receipe=Receipe.objects.all()
    if request.GET.get('search'):
        queryset=Receipe.objects.filter(receipe_name__icontains=request.GET.get('search'))
        print(request.GET.get('search'))
    return render(request,'myapp/index.html',{'receipe':receipe})


@login_required(login_url='/login')
def delete_receipe(request,slug):
    queryset=Receipe.objects.get(receipe_slug=slug)
    queryset.delete()
    return redirect('/index')

#@login_required(login_url='/login')
def update_receipe(request,slug):
    queryset=Receipe.objects.get(receipe_slug=slug)
    if request.method=='POST':
        data=request.POST
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        receipe_amount=data.get('receipe_amount')
        receipe_image=request.FILES.get('receipe_image')
        queryset.receipe_name=receipe_name
        queryset.receipe_description=receipe_description
        queryset.receipe_amount=receipe_amount
        if receipe_image:
            queryset.receipe_image=receipe_image
        
        queryset.save()
        return redirect('/index')

    context={'queryset':queryset}
    return render(request,'myapp/update.html',context)

def login_page(request):
    if request.method=='post':
        username=request.POSt.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'invalid username')
            return redirect('/login')
        
        user=authenticate(username='username',password='password')
        if user is None:
            messages.error(request,'invalid credential')
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/receipes')
        

    return render(request,'myapp/login.html')

def register(request):
    if request.method=='post':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'username already exists')
            return redirect('/login')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        user.set_password(password)
        user.save()
        messages.info(request,'account created successfully...')

        return redirect('/register')
    return render(request,'myapp/register.html')


def logout_page(request):
    logout(request)
    return render(request,'myapp/logout.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})

