from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    show_education, 
    create_experience, 
    get_experiences_json, 
    delete_experience,
    # Import fungsi-fungsi education yang baru:
    create_education,
    update_education,
    delete_education,
    get_educations_json
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    
    # --- URL Experience ---
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    
    # --- URL Education ---
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/<uuid:education_id>/update/", update_education, name="update_education"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("api/education/", get_educations_json, name="get_educations_json"),
]