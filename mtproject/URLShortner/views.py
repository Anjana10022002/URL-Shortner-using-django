from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import URLForm
from .models import URLShortner
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random, string
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

def signup_page(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})
                
def login_page(request):
    if request.method =='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

@login_required(login_url='login')
def home_page(request):
    urls = URLShortner.objects.filter(user=request.user)
    return render(request, "home.html", {"urls": urls})

def generate_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
@login_required(login_url='login')   
def add_url(request):
    if URLShortner.objects.filter(user=request.user).count() >= 5:
        messages.error(request, "Limit reached: You can add only 5 URLs.")
        return redirect('home')
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.user = request.user
            url.short_url = generate_url()
            url.save()
            messages.success(request, "URL added successfully.")
            return redirect('home')
    else:
        
        form = URLForm()
    return render(request, 'add_url.html', {'form':form})

@login_required(login_url='login')        
def url_list(request):
    urls = URLShortner.objects.filter(user=request.user).order_by('-time')
    query = request.GET.get('search_box')
    if query:
        urls = urls.filter(
            Q(title__icontains=query) | Q(short_url__icontains=query)
        )
    paginator = Paginator(urls, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'url_list.html', {'page_obj': page_obj})

@login_required(login_url='login')
def edit_url(request,id):
    url = URLShortner.objects.get(id=id, user=request.user) 
    if request.method == 'POST':
        form = URLForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            messages.success(request, "URL updated successfully.")
            return redirect('url_list')
    else:
        form = URLForm(instance=url)
    return render(request, 'edit_url.html', {'form': form})

@login_required(login_url='login')
def delete_url(request, id):
    url = URLShortner.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        url.delete()
        return redirect('url_list')
    return render(request, 'delete_url.html', {'url': url})

@login_required(login_url='login')
def logout_page(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged out successfully.")   
        return redirect('login')
    return render(request, 'logout.html')

@login_required(login_url='login')
def redirect_url(request, code):
    url_obj = get_object_or_404(URLShortner, short_url=code)
    return HttpResponseRedirect(url_obj.url)