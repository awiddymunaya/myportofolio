from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput
from main.models import Experience

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