from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
        # Migrasi 0005 mengisi data awal dari fixture; kosongkan agar test terkendali
        Experience.objects.all().delete()
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        # Sejak Tugas 5 kartu dirender JavaScript, jadi halaman hanya berisi kerangka
        # dan alamat API; datanya diperiksa lewat API DRF (Tutorial 07).
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, reverse("api:experience-list"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

        data = self.client.get(reverse("api:experience-list")).json()
        self.assertEqual(data[0]["title"], self.experience.title)
        self.assertEqual(data[0]["description"], self.experience.description)
        self.assertEqual(data[0]["category_display"], "Part-Time")
        self.assertTrue(data[0]["is_ongoing"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("api:experience-list"))

        self.assertEqual(response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        data = self.client.get(reverse("api:experience-list")).json()

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(data[0]["is_ongoing"])
        self.assertIsNotNone(data[0]["ended_at"])

class EducationTest(TestCase):
    def setUp(self):
        Education.objects.all().delete()

    def test_education_url_is_exist_and_uses_correct_template(self):
        response = self.client.get(reverse('main:show_education'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education.html')

    def test_education_shows_empty_message_when_no_data(self):
        # Data Education dimuat lewat fetch() ke endpoint JSON, bukan dirender template
        response = self.client.get(reverse('main:get_educations_json'))
        self.assertEqual(response.json(), [])

    def test_education_shows_data_when_exists(self):
        Education.objects.create(
            level="SMA",
            institution_name="SMA Negeri 1 Jakarta",
            start_year="2019",
            end_year="2022"
        )
        response = self.client.get(reverse('main:get_educations_json'))
        self.assertContains(response, "SMA Negeri 1 Jakarta")