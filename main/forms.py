from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput, NumberInput
from main.models import Experience, Education

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]

        # Mengubah label agar lebih mudah dibaca oleh user saat form ditampilkan
        labels = {
            "title": "Nama Posisi / Jabatan",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pekerjaan",
            "thumbnail": "URL Gambar atau Logo (Opsional)",
            "ended_at": "Tanggal Selesai (Kosongkan jika masih berlangsung)",
        }

        # Mengatur tampilan input HTML-nya (tambah placeholder, dll)
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: Data Science Member",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan peran, tugas, atau pencapaianmu di sini...",
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select", 
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://contoh.com/logo-organisasi.png",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date", # Ini bakal memunculkan kalender HTML5 otomatis!
                }
            ),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ["level", "institution_name", "start_year", "end_year", "description"]

        labels = {
            "level": "Tingkat Pendidikan",
            "institution_name": "Nama Institusi",
            "start_year": "Tahun Masuk",
            "end_year": "Tahun Lulus (Atau ketik 'Sekarang')",
            "description": "Catatan Tambahan (Opsional)",
        }

        widgets = {
            "level": TextInput(
                attrs={
                    "placeholder": "Contoh: S1, SMA, SMP",
                    "maxlength": 50,
                }
            ),
            "institution_name": TextInput(
                attrs={
                    "placeholder": "Contoh: Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "start_year": NumberInput(
                attrs={
                    "placeholder": "Contoh: 2024",
                }
            ),
            "end_year": TextInput(
                attrs={
                    "placeholder": "Contoh: 2028 atau Sekarang",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pencapaian atau jurusannmu di sini...",
                    "rows": 3,
                }
            ),
        }