from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicalReport
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def upload_report(request):
    if request.method == "POST":
        file = request.FILES.get("report_file")
        MedicalReport.objects.create(user=request.user, report_file=file)
        return redirect("dashboard")
    return render(request, "upload.html")

@login_required
def dashboard(request):
    reports = MedicalReport.objects.filter(user=request.user).order_by("-created_at")

    selected_report = None
    report_id = request.GET.get("report")
    if report_id:
        selected_report = MedicalReport.objects.filter(id=report_id, user=request.user).first()

    return render(request, "dashboard.html", {
        "reports": reports,
        "selected_report": selected_report
    })




def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
        else:
            print(form.errors)  # helpful for debugging
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})
