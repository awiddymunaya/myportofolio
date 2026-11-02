from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """Semua orang boleh membaca; hanya Pemilik (superuser) yang boleh mengubah data."""

    message = "Hanya Pemilik portofolio yang dapat mengubah data."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Aturan Tugas 4 untuk Experience:
      - semua orang boleh membaca (GET/HEAD/OPTIONS)
      - Pemilik (superuser) boleh semuanya
      - Editor hanya boleh mengubah (PUT/PATCH), tidak boleh menambah atau menghapus
    """

    message = "Akses ditolak: peranmu tidak boleh melakukan tindakan ini."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
