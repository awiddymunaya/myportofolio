from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
import datetime # Akan kita gunakan nanti untuk fitur Cookie Last Login
from django.contrib.auth.decorators import login_required

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

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def show_experience(request):
    json_response = get_experiences_json(request)
    experiences_deserialized = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experiences = [exp.object for exp in experiences_deserialized]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def show_education(request):
    educations = Education.objects.all()
    context = {
        'educations': educations,
        'name': "Awiddy Munaya Rajanadoli",
    }
    return render(request, 'education.html', context)

@login_required(login_url='/login')
def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "form": form,
    }
    return render(request, "create_experience.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")

def get_educations_json(request):
    educations = Education.objects.all()
    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

# 2. Menampilkan data (dengan deserialisasi JSON)
def show_education(request):
    json_response = get_educations_json(request)
    educations_deserialized = serializers.deserialize("json", json_response.content.decode("utf-8"))
    educations = [edu.object for edu in educations_deserialized]

    context = {
        'educations': educations,
        'name': "Awiddy Munaya Rajanadoli",
    }
    return render(request, 'education.html', context)

# 3. Create (Menambah data)
@login_required(login_url='/login')
def create_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "form": form,
    }
    return render(request, "create_education.html", context)

# 4. Update (Mengubah data)
def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    # Memasukkan data lama ke dalam form (instance)
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

# 5. Delete (Menghapus data)
@login_required(login_url='/login')
def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Data pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")

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
            # Format waktu menjadi Tahun-Bulan-Tanggal Jam:Menit:Detik
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
    logout(request)
    return redirect('main:login')