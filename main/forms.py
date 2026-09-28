from django.forms import ModelForm, TextInput, Textarea, Select, DateInput, NumberInput
from main.models import Experience, Education

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        # Menambahkan logo_url ke dalam form fields
        fields = ["title", "description", "category", "logo_url", "thumbnail", "ended_at"]

        labels = {
            "title": "Nama Posisi / Jabatan",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pekerjaan",
            "logo_url": "Link / Jalur Folder Lambang Organisasi",
            "thumbnail": "Link / Jalur Folder Foto Bukti Kegiatan",
            "ended_at": "Tanggal Selesai (Kosongkan jika masih berlangsung)",
        }

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
            # Diubah menjadi TextInput agar bisa membaca jalur file statis
            "logo_url": TextInput(
                attrs={
                    "placeholder": "Contoh: https://... atau /static/img/logo.jpg",
                }
            ),
            # Diubah menjadi TextInput agar bisa membaca jalur file statis
            "thumbnail": TextInput(
                attrs={
                    "placeholder": "Contoh: https://... atau /static/img/kegiatan.jpg",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date", 
                }
            ),
        }

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
            # Diubah menjadi TextInput agar bisa membaca jalur file statis
            "logo_url": TextInput(
                attrs={
                    "placeholder": "Contoh: https://... atau /static/img/logo.png",
                }
            ),
        }