from django.shortcuts import render   # ✅ ADD THIS LINE

def home(request):
    return render(request, "aqua.html")