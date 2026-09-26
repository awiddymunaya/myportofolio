from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required

# Helper untuk mengecek apakah user masuk ke grup 'Editor'
def is_editor(user):
    return user.groups.filter(name='Editor').exists()

def show_main(request):
    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "npm": "2506622872",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Aku adalah seorang pemalas dan hobiku ialah tidur. "
            "Aku berasal dari Padang, umurku 18, dan aku suka kota Jakarta."
        ),
        "last_login": request.COOKIES.get('last_login'),
    }
    return render(request, "index.html", context)


# ==============================
# VIEW EXPERIENCE
# ==============================
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def show_experience(request):
    title_query = request.GET.get("q", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "experiences": experiences,
        # Variabel ini dikirim ke HTML agar tombol edit muncul untuk Editor
        "is_editor": is_editor(request.user) if request.user.is_authenticated else False, 
    }
    return render(request, "experience.html", context)

@login_required(login_url='/login')
def create_experience(request):
    # OTORISASI: Hanya Superuser (Pemilik) yang bisa Create
    if not request.user.is_superuser:
        return HttpResponseForbidden("Akses Ditolak: Hanya Pemilik yang dapat menambah data.")

    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil ditambahkan!")
        return redirect('main:show_experience')
            
    context = {'form': form}
    return render(request, "create_experience.html", context)

@login_required(login_url='/login')
def delete_experience(request, experience_id):
    # OTORISASI: Hanya Superuser (Pemilik) yang bisa Delete
    if not request.user.is_superuser:
        return HttpResponseForbidden("Akses Ditolak: Hanya Pemilik yang dapat menghapus data.")

    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")

# FITUR BARU: Bintang (Semua User Login bisa akses)
@login_required(login_url='/login')
def toggle_star(request, experience_id):
    if request.method == "POST":
        experience = get_object_or_404(Experience, pk=experience_id)
        # Jika user sudah memberi bintang, maka cabut bintangnya. Jika belum, tambahkan.
        if request.user in experience.stars.all():
            experience.stars.remove(request.user)
        else:
            experience.stars.add(request.user)
    return redirect('main:show_experience')


# ==============================
# VIEW EDUCATION
# ==============================
def get_educations_json(request):
    educations = Education.objects.all()
    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

def show_education(request):
    educations = Education.objects.all()
    context = {
        'educations': educations,
        'name': "Awiddy Munaya Rajanadoli",
        "is_editor": is_editor(request.user) if request.user.is_authenticated else False, 
    }
    return render(request, 'education.html', context)

@login_required(login_url='/login')
def create_education(request):
    # OTORISASI: Hanya Superuser (Pemilik) yang bisa Create
    if not request.user.is_superuser:
        return HttpResponseForbidden("Akses Ditolak: Hanya Pemilik yang dapat menambah data.")

    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil ditambahkan!")
        return redirect('main:show_education')
            
    context = {'form': form}
    return render(request, "create_education.html", context)

@login_required(login_url='/login')
def update_education(request, education_id):
    # OTORISASI: Superuser ATAU Editor yang bisa Update
    if not (request.user.is_superuser or is_editor(request.user)):
        return HttpResponseForbidden("Akses Ditolak: Minimal peran Editor diperlukan untuk mengubah data.")

    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "form": form,
        "education": education,
    }
    return render(request, "update_education.html", context)

@login_required(login_url='/login')
def delete_education(request, education_id):
    # OTORISASI: Hanya Superuser (Pemilik) yang bisa Delete
    if not request.user.is_superuser:
        return HttpResponseForbidden("Akses Ditolak: Hanya Pemilik yang dapat menghapus data.")

    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Data pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")


# ==============================
# VIEW AUTENTIKASI
# ==============================
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('main:login')
    
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            response = redirect('main:show_main')
            waktu_sekarang = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response.set_cookie('last_login', waktu_sekarang)
            
            return response
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm(request)
        
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    response = redirect('main:login')
    # Menghapus cookie keamanan last_login saat pengguna logout
    response.delete_cookie('last_login')
    logout(request)
    return response