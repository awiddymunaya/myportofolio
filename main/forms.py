from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, Select, DateInput, NumberInput
from django.utils.html import strip_tags

from main.models import Experience, Education


# Skema URL yang dilarang untuk field gambar (bisa dipakai untuk menyisipkan skrip)
DANGEROUS_URL_SCHEMES = ("javascript:", "data:", "vbscript:")


def clean_text(value, field_label, required=True):
    """
    Membersihkan input teks dari tag HTML menggunakan strip_tags.

    Jika setelah dibersihkan teksnya kosong (misalnya input hanya berisi
    <img src="x" onerror="alert('XSS!')">), input ditolak dengan pesan
    validasi agar data berbahaya tidak tersimpan diam-diam sebagai string kosong.
    """
    if value is None:
        return value
    cleaned = strip_tags(value).strip()
    if required and not cleaned:
        raise ValidationError(f"{field_label} tidak boleh kosong atau hanya berisi tag HTML.")
    return cleaned


def clean_image_path(value):
    """Membersihkan link/jalur gambar dan menolak skema URL berbahaya."""
    if not value:
        return value
    cleaned = strip_tags(value).strip()
    if cleaned.lower().replace(" ", "").startswith(DANGEROUS_URL_SCHEMES):
        raise ValidationError("Link gambar harus berupa https://... atau jalur seperti /static/img/foto.jpg.")
    return cleaned


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "logo_url", "thumbnail", "started_at", "ended_at"]

        labels = {
            "title": "Nama Posisi / Jabatan",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pekerjaan",
            "logo_url": "Link / Jalur Folder Lambang Organisasi",
            "thumbnail": "Link / Jalur Folder Foto Bukti Kegiatan",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai (Kosongkan jika masih berlangsung)",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Contoh: Data Science Member", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Ceritakan peran, tugas, atau pencapaianmu di sini...", "rows": 4}),
            "category": Select(attrs={"class": "form-select"}),
            "logo_url": TextInput(attrs={"placeholder": "Contoh: https://... atau /static/img/logo.jpg"}),
            "thumbnail": TextInput(attrs={"placeholder": "Contoh: https://... atau /static/img/kegiatan.jpg"}),
            "started_at": DateInput(attrs={"type": "date"}),
            "ended_at": DateInput(attrs={"type": "date"}),
        }

    # --- Sanitasi sisi server (Tugas 5: perlindungan XSS) ---
    def clean_title(self):
        return clean_text(self.cleaned_data.get("title"), "Nama posisi")

    def clean_description(self):
        return clean_text(self.cleaned_data.get("description"), "Deskripsi")

    def clean_logo_url(self):
        return clean_image_path(self.cleaned_data.get("logo_url"))

    def clean_thumbnail(self):
        return clean_image_path(self.cleaned_data.get("thumbnail"))

    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get("started_at")
        ended_at = cleaned_data.get("ended_at")
        if started_at and ended_at and ended_at.date() < started_at:
            self.add_error("ended_at", "Tanggal selesai tidak boleh sebelum tanggal mulai.")
        return cleaned_data


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["level", "institution_name", "start_year", "end_year", "description", "logo_url"]

        labels = {
            "level": "Tingkat Pendidikan",
            "institution_name": "Nama Institusi",
            "start_year": "Tahun Masuk",
            "end_year": "Tahun Lulus (Atau ketik 'Sekarang')",
            "description": "Catatan Tambahan (Opsional)",
            "logo_url": "Link / Jalur Folder Logo Institusi",
        }

        widgets = {
            "level": TextInput(attrs={"placeholder": "Contoh: S1, SMA, SMP", "maxlength": 50}),
            "institution_name": TextInput(attrs={"placeholder": "Contoh: Universitas Indonesia", "maxlength": 255}),
            "start_year": NumberInput(attrs={"placeholder": "Contoh: 2024"}),
            "end_year": TextInput(attrs={"placeholder": "Contoh: 2028 atau Sekarang"}),
            "description": Textarea(attrs={"placeholder": "Ceritakan pencapaian atau jurusanmu di sini...", "rows": 3}),
            "logo_url": TextInput(attrs={"placeholder": "Contoh: https://... atau /static/img/logo.png"}),
        }

    # --- Sanitasi sisi server (Tugas 5: perlindungan XSS) ---
    def clean_level(self):
        return clean_text(self.cleaned_data.get("level"), "Tingkat pendidikan")

    def clean_institution_name(self):
        return clean_text(self.cleaned_data.get("institution_name"), "Nama institusi")

    def clean_end_year(self):
        return clean_text(self.cleaned_data.get("end_year"), "Tahun lulus")

    def clean_description(self):
        return clean_text(self.cleaned_data.get("description"), "Catatan", required=False)

    def clean_logo_url(self):
        return clean_image_path(self.cleaned_data.get("logo_url"))