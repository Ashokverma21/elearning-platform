# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from courses.models import EnrolledCourse



#login
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Yaha wo page jaha login ke baad bhejna hai
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "users/login.html")

def register_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if User.objects.filter(username=email).exists():
            return render(request,'users/register.html',{'error': 'User already exists'})
        else:
            user = User.objects.create_user(username=email,email=email, password=password)
            user.save()
            return redirect('login')
        
            
    
    
    return render(request,"users/register.html")

#logout
def logout_user(request):
    logout(request)
    return redirect('login')
    
#profile
@login_required(login_url='login')
def profile_page(request):

    # Get enrolled courses for logged-in user
    enrollments = EnrolledCourse.objects.filter(user=request.user)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'enrollments': enrollments,
    })



#edit profile

from django.shortcuts import render, redirect
from .models import Profile

def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name")

        if request.FILES.get("image"):
            profile.image = request.FILES["image"]

        profile.save()
        return redirect("profile")

    return render(request, "users/edit_profile.html")

