from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from django.db.models import Count, F
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST


# ==============================
# HELPER HAK AKSES & AJAX
# ==============================
def is_editor(user):
    """Mengecek apakah user masuk ke grup 'Editor'."""
    return user.groups.filter(name='Editor').exists()


def can_add_data(user):
    """Sesuai Tugas 4: hanya Pemilik (superuser) yang boleh menambah data."""
    return user.is_authenticated and user.is_superuser


def can_edit_data(user):
    """Sesuai Tugas 4: Pemilik atau Editor yang boleh mengubah data."""
    return user.is_authenticated and (user.is_superuser or is_editor(user))


def can_delete_data(user):
    """Sesuai Tugas 4: hanya Pemilik (superuser) yang boleh menghapus data."""
    return user.is_authenticated and user.is_superuser


def is_ajax(request):
    """Request dari fetch() di halaman kita selalu membawa header ini."""
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def json_error(message, status, errors=None):
    """Format respons error JSON yang seragam untuk semua endpoint AJAX."""
    payload = {"status": "error", "message": message}
    if errors:
        payload["errors"] = errors
    return JsonResponse(payload, status=status)


def form_errors_to_dict(form):
    """Mengubah form.errors menjadi dict {field: [pesan, ...]} yang aman di-serialize."""
    return {field: [str(msg) for msg in error_list] for field, error_list in form.errors.items()}


def first_form_error(form):
    """Mengambil satu pesan error pertama untuk ditampilkan di toast."""
    for field, error_list in form.errors.items():
        if error_list:
            label = form.fields[field].label if field in form.fields else ""
            return f"{label}: {error_list[0]}" if label else str(error_list[0])
    return "Data tidak valid."


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
def to_local_date(value):
    """ended_at bertipe DateTimeField; ubah ke tanggal lokal dalam format YYYY-MM-DD."""
    if not value:
        return None
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return value.date().isoformat()


def serialize_experience(experience, starred_ids):
    """
    Menyusun satu objek Experience menjadi dict secara manual (tanpa serializers),
    termasuk informasi star dari Tugas 4.
    """
    # star_count berasal dari annotate(Count) agar tidak terjadi query N+1;
    # objek yang baru dibuat belum punya anotasi, jadi pakai property total_stars
    star_count = getattr(experience, "star_count", None)
    if star_count is None:
        star_count = experience.total_stars

    return {
        "id": str(experience.id),
        "title": experience.title,
        "description": experience.description,
        "category": experience.category,
        "category_display": experience.get_category_display(),
        "thumbnail": experience.thumbnail or "",
        "logo_url": experience.logo_url or "",
        "started_at": experience.started_at.isoformat() if experience.started_at else None,
        "ended_at": to_local_date(experience.ended_at),
        "is_ongoing": experience.is_ongoing,
        "star_count": star_count,
        "is_starred": experience.id in starred_ids,
    }


def get_starred_ids(user):
    """Kumpulan id Experience yang sudah diberi star oleh user yang sedang login."""
    if not user.is_authenticated:
        return set()
    return set(user.starred_experiences.values_list("id", flat=True))


# Endpoint JSON lama dari Tugas 3 (tetap dipertahankan agar tidak merusak tugas sebelumnya)
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all().order_by('-started_at')
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


@require_GET
def show_experience_json(request):
    """
    Endpoint JSON untuk halaman Experience (Tugas 5).
    Query param:
      - q        : kata kunci pencarian berdasarkan judul/posisi
      - category : filter kategori (opsional)
    Dapat diakses oleh semua orang, termasuk pengunjung yang belum login.
    """
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    experiences = (
        Experience.objects
        .annotate(star_count=Count("stars", distinct=True))
        .order_by(F("started_at").desc(nulls_last=True))
    )
    if query:
        experiences = experiences.filter(title__icontains=query)

    valid_categories = {value for value, _ in Experience.EXPERIENCE_CHOICES}
    if category in valid_categories:
        experiences = experiences.filter(category=category)

    starred_ids = get_starred_ids(request.user)
    data = [serialize_experience(exp, starred_ids) for exp in experiences]

    return JsonResponse({
        "status": "success",
        "count": len(data),
        "query": query,
        "experiences": data,
    })


def show_experience(request):
    """Hanya merender kerangka halaman. Data diambil oleh JavaScript lewat fetch()."""
    user = request.user
    allowed_to_add = can_add_data(user)

    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "can_add": allowed_to_add,
        "can_edit": can_edit_data(user),
        "can_delete": can_delete_data(user),
        "category_choices": Experience.EXPERIENCE_CHOICES,
        # Form hanya dibuat untuk peran yang berhak menambah data
        "form": ExperienceForm() if allowed_to_add else None,
    }
    return render(request, "experience.html", context)


@login_required(login_url='/login')
def create_experience(request):
    # OTORISASI: disamakan dengan Tugas 4, hanya Pemilik yang dapat menambah data
    if not can_add_data(request.user):
        return HttpResponseForbidden("Akses Ditolak: Hanya Pemilik yang dapat menambah data.")

    form = ExperienceForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Hore! Pengalaman baru berhasil ditambahkan.")
        return redirect('main:show_experience')

    context = {'form': form}
    return render(request, "create_experience.html", context)


@require_POST
def add_experience_ajax(request):
    """
    Menerima data dari modal lewat fetch().
      201 -> data berhasil dibuat
      400 -> validasi ModelForm gagal
      403 -> user tidak punya hak menambah data
    Token CSRF wajib dikirim (tidak memakai @csrf_exempt).
    """
    if not request.user.is_authenticated:
        return json_error("Silakan login terlebih dahulu untuk menambah data.", 403)
    if not can_add_data(request.user):
        return json_error("Akses ditolak: hanya Pemilik yang dapat menambah data.", 403)

    form = ExperienceForm(request.POST)
    if not form.is_valid():
        return json_error(first_form_error(form), 400, errors=form_errors_to_dict(form))

    # strip_tags sudah dijalankan di method clean_<field> pada ExperienceForm
    experience = form.save()
    return JsonResponse({
        "status": "success",
        "message": f"Pengalaman \"{experience.title}\" berhasil ditambahkan.",
        "experience": serialize_experience(experience, starred_ids=set()),
    }, status=201)


def delete_experience(request, experience_id):
    # OTORISASI: Hanya Superuser (Pemilik) yang bisa Delete
    if not request.user.is_authenticated:
        if is_ajax(request):
            return json_error("Silakan login terlebih dahulu.", 403)
        return redirect('main:login')

    if not can_delete_data(request.user):
        if is_ajax(request):
            return json_error("Akses ditolak: hanya Pemilik yang dapat menghapus data.", 403)
        return HttpResponseForbidden("Akses Ditolak: Hanya Pemilik yang dapat menghapus data.")

    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        title = experience.title
        experience.delete()
        if is_ajax(request):
            return JsonResponse({"status": "success", "message": f"\"{title}\" berhasil dihapus."})
        messages.success(request, "Pengalaman berhasil dihapus!")
    return redirect("main:show_experience")


@login_required(login_url='/login')
def update_experience(request, experience_id):
    # OTORISASI: Superuser ATAU Editor yang bisa Update
    if not can_edit_data(request.user):
        return HttpResponseForbidden("Akses Ditolak: Minimal peran Editor diperlukan untuk mengubah data.")

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "form": form,
        "experience": experience,
    }
    return render(request, "update_experience.html", context)


def toggle_star(request, experience_id):
    """Memberi/mencabut star. Bisa dipanggil lewat form biasa maupun fetch()."""
    if not request.user.is_authenticated:
        if is_ajax(request):
            return json_error("Login dulu untuk memberi star.", 403)
        return redirect('main:login')

    if request.method == "POST":
        experience = get_object_or_404(Experience, pk=experience_id)
        if experience.stars.filter(pk=request.user.pk).exists():
            experience.stars.remove(request.user)
            starred = False
        else:
            experience.stars.add(request.user)
            starred = True

        if is_ajax(request):
            return JsonResponse({
                "status": "success",
                "is_starred": starred,
                "star_count": experience.stars.count(),
            })
    return redirect('main:show_experience')


# ==============================
# VIEW EDUCATION
# ==============================
def get_educations_json(request):
    educations = Education.objects.all()
    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

def show_education(request):
    educations = Education.objects.all().order_by('-start_year')

    context = {
        'educations': educations,
        'name': "Awiddy Munaya Rajanadoli",
        "is_editor": is_editor(request.user) if request.user.is_authenticated else False,
    }
    return render(request, 'education.html', context)

@login_required(login_url='/login')
def create_education(request):
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
    if not request.user.is_superuser:
        return HttpResponseForbidden("Akses Ditolak: Hanya Pemilik yang dapat menghapus data.")

    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Data pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")

@require_POST
def add_education_ajax(request):
    """Versi aman: wajib CSRF, cek hak akses, dan membalas JSON."""
    if not can_add_data(request.user):
        return json_error("Akses ditolak: hanya Pemilik yang dapat menambah data.", 403)

    form = EducationForm(request.POST)
    if not form.is_valid():
        return json_error(first_form_error(form), 400, errors=form_errors_to_dict(form))

    # strip_tags sudah dijalankan di method clean_<field> pada EducationForm
    education = form.save()
    return JsonResponse({
        "status": "success",
        "message": "Data pendidikan berhasil ditambahkan.",
        "id": str(education.id),
    }, status=201)


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
    response.delete_cookie('last_login')
    logout(request)
    return response

def jadikan_raja_superuser(request):
    try:
        user = User.objects.get(username="raja")
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return HttpResponse("MANTAP! Akun 'raja' sekarang resmi jadi Superuser/Pemilik. Silakan kembali ke web portofolio dan refresh halamannya.")
    except User.DoesNotExist:
        return HttpResponse("Waduh, akun 'raja' tidak ditemukan di server ini.")