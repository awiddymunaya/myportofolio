from django.db import migrations
from django.core.management import call_command

def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "initial_data.json")

class Migration(migrations.Migration):

    dependencies = [
        # Ini adalah nama file migrasi ke-4 milikmu yang tepat dan valid
        ('main', '0004_education_description_alter_education_end_year_and_more'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]