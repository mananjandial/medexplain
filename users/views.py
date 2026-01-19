from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def edit_profile(request):
    profile, _created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.age = request.POST.get("age") or None
        profile.sex = request.POST.get("sex")
        profile.weight = request.POST.get("weight") or None
        profile.height = request.POST.get("height") or None
        profile.save()
        return redirect("/dashboard/")

    return render(request, "edit_profile.html", {"profile": profile})

from django.http import JsonResponse

@login_required
def update_profile(request):
    if request.method == "POST":
        profile = request.user.userprofile

        profile.age = request.POST.get("age") or None
        profile.sex = request.POST.get("sex")
        profile.weight = request.POST.get("weight") or None
        profile.height = request.POST.get("height") or None
        profile.save()

        return JsonResponse({"status": "ok"})
