from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Education, Experience
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import EducationSerializer, ExperienceSerializer


# ==============================
# API EXPERIENCE (Tutorial 07)
# ==============================
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = (
            Experience.objects
            .prefetch_related("stars")
            .order_by(F("started_at").desc(nulls_last=True), "title", "id")
        )

        title = request.query_params.get("title", "").strip()
        if title:
            experiences = experiences.filter(title__icontains=title)

        # Filter kategori dari Tugas 5 tetap didukung
        category = request.query_params.get("category", "").strip()
        valid_categories = {value for value, _ in Experience.EXPERIENCE_CHOICES}
        if category in valid_categories:
            experiences = experiences.filter(category=category)

        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)

    # POST: tambah data baru
    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("stars"), pk=experience_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT (semua field wajib) atau PATCH (hanya field yang dikirim)
    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    # Akun pemberi star selalu request.user, klien tidak bisa memilih user lain
    if experience.stars.filter(pk=request.user.pk).exists():
        experience.stars.remove(request.user)
    else:
        experience.stars.add(request.user)

    serializer = ExperienceSerializer(experience, context={"request": request})
    return Response(serializer.data)


# ==============================
# API EDUCATION (Tugas 6)
# ==============================
# Hak akses ditangani permission class, validasi ditangani EducationSerializer,
# jadi view hanya mengatur alur request -> serializer -> response.

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    """
    GET  : daftar Education, terbuka untuk semua orang.
           Query param ?q= mencari berdasarkan nama institusi atau jenjang.
    POST : tambah Education baru (hanya Pemilik). 201 jika berhasil, 400 jika tidak valid.
    """
    if request.method in ("GET", "HEAD"):
        educations = (
            Education.objects
            .prefetch_related("stars")
            .order_by("-start_year", "institution_name", "id")
        )

        query = request.query_params.get("q", "").strip()
        if query:
            educations = educations.filter(
                Q(institution_name__icontains=query) | Q(level__icontains=query)
            )

        serializer = EducationSerializer(
            educations, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = EducationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    """
    GET          : detail satu Education (semua orang).
    PUT / PATCH  : ubah data (Pemilik dan Editor).
    DELETE       : hapus data (hanya Pemilik), membalas 204 tanpa body.
    """
    education = get_object_or_404(
        Education.objects.prefetch_related("stars"), pk=education_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = EducationSerializer(education, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT wajib mengirim semua field, PATCH cukup field yang berubah
    serializer = EducationSerializer(
        education, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    """Memberi atau membatalkan star untuk akun yang sedang login."""
    education = get_object_or_404(Education, pk=education_id)
    # Akun pemberi star selalu request.user, klien tidak bisa memilih user lain
    if education.stars.filter(pk=request.user.pk).exists():
        education.stars.remove(request.user)
    else:
        education.stars.add(request.user)

    serializer = EducationSerializer(education, context={"request": request})
    return Response(serializer.data)
