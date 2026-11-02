import json
from pathlib import Path

from django.db import migrations

FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "initial_data.json"


def load_my_initial_data(apps, schema_editor):
    # Memakai model "historis" (apps.get_model), bukan call_command("loaddata").
    # loaddata selalu memakai models.py versi terbaru, sehingga gagal saat database
    # baru dibuat (misalnya ketika menjalankan test) karena started_at sekarang DateField,
    # sedangkan fixture ini dibuat waktu started_at masih DateTimeField.
    # Database yang sudah pernah migrate tidak terpengaruh, karena migrasi ini tidak dijalankan ulang.
    with open(FIXTURE_PATH, encoding="utf-8") as fixture:
        objects = json.load(fixture)

    for obj in objects:
        model = apps.get_model(obj["model"])
        field_names = {field.name for field in model._meta.concrete_fields}
        defaults = {key: value for key, value in obj["fields"].items() if key in field_names}
        model.objects.update_or_create(pk=obj["pk"], defaults=defaults)


class Migration(migrations.Migration):

    dependencies = [
        # Ini adalah nama file migrasi ke-4 milikmu yang tepat dan valid
        ('main', '0004_education_description_alter_education_end_year_and_more'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data, migrations.RunPython.noop),
    ]
