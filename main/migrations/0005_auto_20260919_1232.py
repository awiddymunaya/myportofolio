from django.db import migrations
from django.core.management import call_command

def load_my_initial_data(apps, schema_editor):
    # Memuat file initial_data.json ke dalam database saat migrasi berjalan
    call_command("loaddata", "initial_data.json")

class Migration(migrations.Migration):

    dependencies = [
        # BIARKAN BARIS INI APA ADANYA SESUAI BAWAAN DJANGO!
        # (Biasanya berisi: ('main', '0004_education_description...'))
    ]

    operations = [
        # Tambahkan baris ini ke dalam operations
        migrations.RunPython(load_my_initial_data),
    ]