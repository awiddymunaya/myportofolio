from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "npm": "2506622872",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Aku adalah seorang pemalas dan hobiku ialah tidur. "
            "Aku berasal dari Padang, umurku 18, dan aku suka kota Jakarta."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Awiddy Munaya Rajanadoli",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)