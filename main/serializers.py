from rest_framework import serializers

from main.forms import clean_image_path, clean_text
from main.models import Education, Experience


class ExperienceSerializer(serializers.ModelSerializer):
    # Label kategori yang enak dibaca, misalnya "Part-Time" untuk "part-time"
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)

    # Field hasil perhitungan: otomatis read-only, nilainya dari method get_<nama_field>
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    # Form modal mengirim tanggal saja (YYYY-MM-DD), padahal ended_at di model bertipe DateTimeField
    ended_at = serializers.DateTimeField(
        required=False, allow_null=True, input_formats=["iso-8601", "%Y-%m-%d"],
    )

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "logo_url", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    # --- Validasi per field ---
    # Memakai ulang fungsi dari forms.py. Serializer tidak menjalankan clean_<field>
    # milik ExperienceForm, jadi aturan yang sama harus dipasang di sini juga.
    # ValidationError Django yang dilempar fungsi tersebut otomatis diubah DRF menjadi error 400.
    def validate_title(self, value):
        return clean_text(value, "Nama posisi")

    def validate_description(self, value):
        return clean_text(value, "Deskripsi")

    def validate_logo_url(self, value):
        return clean_image_path(value)

    def validate_thumbnail(self, value):
        return clean_image_path(value)

    # --- Validasi antar-field (sama seperti ExperienceForm.clean) ---
    def validate(self, attrs):
        # Saat PATCH, field yang tidak dikirim diambil dari data lama
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started_at and ended_at and ended_at.date() < started_at:
            raise serializers.ValidationError(
                {"ended_at": "Tanggal selesai tidak boleh sebelum tanggal mulai."}
            )
        return attrs

    # --- Field hasil perhitungan ---
    def get_star_count(self, obj):
        return obj.stars.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.stars.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.stars.all())


class EducationSerializer(serializers.ModelSerializer):
    """Representasi dan validasi data Education untuk API /api/v1/education/ (Tugas 6)."""

    # Field hasil perhitungan dari relasi star (Tugas 4): selalu read-only
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Education
        # Ditulis eksplisit (bukan "__all__") agar relasi stars, yang berisi id User,
        # tidak ikut terbuka dan tidak bisa diisi langsung oleh klien
        fields = [
            "id", "level", "institution_name", "start_year", "end_year",
            "description", "logo_url", "star_count", "is_starred",
        ]
        read_only_fields = ["id"]

    # --- Validasi per field ---
    # Aturannya sama dengan clean_<field> pada EducationForm (Tugas 5), termasuk strip_tags.
    def validate_level(self, value):
        return clean_text(value, "Tingkat pendidikan")

    def validate_institution_name(self, value):
        return clean_text(value, "Nama institusi")

    def validate_end_year(self, value):
        return clean_text(value, "Tahun lulus")

    def validate_description(self, value):
        return clean_text(value, "Catatan", required=False)

    def validate_logo_url(self, value):
        return clean_image_path(value)

    def validate_start_year(self, value):
        if not 1900 <= value <= 2100:
            raise serializers.ValidationError("Tahun masuk harus di antara 1900 dan 2100.")
        return value

    # --- Validasi antar-field ---
    def validate(self, attrs):
        # Saat PATCH, field yang tidak dikirim diambil dari data lama
        start_year = attrs.get("start_year", getattr(self.instance, "start_year", None))
        end_year = attrs.get("end_year", getattr(self.instance, "end_year", None))
        # end_year boleh berupa teks seperti "Sekarang"; hanya angka yang dibandingkan
        if start_year and end_year and str(end_year).isdigit() and int(end_year) < start_year:
            raise serializers.ValidationError(
                {"end_year": "Tahun lulus tidak boleh sebelum tahun masuk."}
            )
        return attrs

    # --- Field hasil perhitungan ---
    def get_star_count(self, obj):
        return obj.stars.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.stars.all()
