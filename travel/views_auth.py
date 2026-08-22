from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.core.cache import cache
import random

from .forms import SignUpForm


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("travel:dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Traveloop. Your account is ready.")
            return redirect("travel:dashboard")
    else:
        form = SignUpForm()
    return render(request, "travel/auth/signup.html", {"form": form})

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            otp = str(random.randint(1000, 9999))
            cache.set(f"pwd_reset_otp_{email}", otp, timeout=600)
            request.session["reset_email"] = email
            send_mail(
                "Your Password Reset OTP",
                f"Your 4-digit OTP is {otp}. It expires in 10 minutes.",
                "noreply@globetrotter.com",
                [email],
                fail_silently=False,
            )
            return redirect("password_reset_otp")
        else:
            messages.error(request, "No user is associated with this email address.")
    return render(request, "travel/auth/password_reset.html")

def password_reset_otp(request):
    email = request.session.get("reset_email")
    if not email:
        return redirect("password_reset")
        
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        real_otp = cache.get(f"pwd_reset_otp_{email}")
        if real_otp and entered_otp == real_otp:
            request.session["can_reset_password"] = True
            return redirect("password_reset_new")
        else:
            messages.error(request, "Invalid or expired OTP.")
    return render(request, "travel/auth/password_reset_otp.html", {"email": email})

def password_reset_new(request):
    email = request.session.get("reset_email")
    if not email or not request.session.get("can_reset_password"):
        return redirect("password_reset")
        
    User = get_user_model()
    user = User.objects.get(email=email)
    
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            request.session.pop("reset_email", None)
            request.session.pop("can_reset_password", None)
            cache.delete(f"pwd_reset_otp_{email}")
            messages.success(request, "Password reset successfully. You can now login.")
            return redirect("login")
    else:
        form = SetPasswordForm(user)
    return render(request, "travel/auth/password_reset_new.html", {"form": form})
