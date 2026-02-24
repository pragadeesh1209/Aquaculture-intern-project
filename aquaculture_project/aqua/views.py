from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vendor, OrganicFood, Suggestion
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Home Page
def home(request):
    return render(request, "aqua.html")


# User Login View
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect("user_suggestion_page")
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist")

    return render(request, "login.html")


# User Signup View
def user_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
             return render(request, "signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken"})

        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error": "Email already registered"})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        return redirect("user_login")

    return render(request, "signup.html")


def vendor_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        shop_name = request.POST.get("shop_name")
        shop_place = request.POST.get("shop_place")
        contact = request.POST.get("contact")

        if Vendor.objects.filter(username=username).exists():
            return render(request, "vendor_signup.html", {"error": "Username already exists"})

        vendor = Vendor(
            name=name,
            username=username,
            shop_name=shop_name,
            shop_place=shop_place,
            contact=contact
        )
        vendor.set_password(password)
        vendor.save()

        return redirect("vendor_login")

    return render(request, "vendor_signup.html")



def vendor_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            vendor = Vendor.objects.get(username=username)
            if vendor.check_password(password):

                request.session['vendor_id'] = vendor.id
                return redirect('vendor_dashboard')
            else:
                error = "Invalid username or password"
        except Vendor.DoesNotExist:
            error = "Invalid username or password"

    return render(request, "vendor_login.html", {"error": error})


# Vendor Dashboard View
def vendor_dashboard(request):
    vendor_id = request.session.get("vendor_id")
    if not vendor_id:
        return redirect("vendor_login")

    vendor = Vendor.objects.get(id=vendor_id)

    if request.method == "POST":
        name = request.POST.get("name")
        fish_type = request.POST.get("fish_type")

        food = OrganicFood.objects.create(
            vendor=vendor,
            name=name,
            fish_type=fish_type
        )

        Suggestion.objects.create(food=food, fish_type=fish_type)

    foods = OrganicFood.objects.filter(vendor=vendor)
    suggestions = Suggestion.objects.filter(food__vendor=vendor)

    return render(request, "vendor_dashboard.html", {
        "vendor": vendor,
        "foods": foods,
        "suggestions": suggestions
    })



def user_suggestion_page(request):
    suggestions = None
    vendors = None
    fish_type = None

    if request.method == 'POST':
        fish_type = request.POST.get('fish_type')

        if 'search_feed' in request.POST:
            suggestions = OrganicFood.objects.filter(fish_type__icontains=fish_type)


        elif 'find_vendors' in request.POST:
            # Fetch vendors who offer matching food
            matching_foods = OrganicFood.objects.filter(fish_type__icontains=fish_type)
            vendor_ids = matching_foods.values_list('vendor_id', flat=True).distinct()
            vendors = Vendor.objects.filter(id__in=vendor_ids)
            suggestions = matching_foods

    return render(request, 'suggestion.html', {
        'suggestions': suggestions,
        'vendors': vendors,
        'fish_type': fish_type
    })

