from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from students.models import StudentProfile
from careers.models import Career

def register_view(request):
    if request.user.is_authenticated:
        return redirect("students:dashboard")
        
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        
        college = request.POST.get("college", "Engineering Institute").strip()
        degree = request.POST.get("degree", "B.Tech").strip()
        branch = request.POST.get("branch", "Computer Science & Engineering").strip()
        graduation_year = int(request.POST.get("graduation_year", 2026))
        cgpa = float(request.POST.get("cgpa", 8.0))
        phone = request.POST.get("phone", "").strip()
        
        if not username or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "accounts/register.html")
            
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html")
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "accounts/register.html")
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "accounts/register.html")
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Default target career
        default_career = Career.objects.first()
        
        StudentProfile.objects.create(
            user=user,
            phone=phone,
            college=college,
            degree=degree,
            branch=branch,
            graduation_year=graduation_year,
            cgpa=cgpa,
            target_career=default_career
        )
        
        login(request, user)
        messages.success(request, f"Welcome to AI Career Guidance, {user.first_name or user.username}! Let's set up your profile.")
        return redirect("students:skills")
        
    return render(request, "accounts/register.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("students:dashboard")
        
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Ensure profile exists
            StudentProfile.objects.get_or_create(user=user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("students:dashboard")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("login")
