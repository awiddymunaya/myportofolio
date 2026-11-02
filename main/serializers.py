from rest_framework import serializers

from main.forms import clean_image_path, clean_text
from main.models import Experience


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
