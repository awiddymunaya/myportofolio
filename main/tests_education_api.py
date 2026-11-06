"""Test API Education (Tugas 6) untuk keempat peran dari Tugas 4."""
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education


class EducationAPITest(APITestCase):
    def setUp(self):
        # Migrasi 0005 mengisi data awal dari fixture; kosongkan agar test terkendali
        Education.objects.all().delete()

        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.user = User.objects.create_user(
            username="biasa", password="test-password", email="biasa@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        # Database test selalu kosong, jadi grup Editor dibuat di sini
        self.editor.groups.add(Group.objects.create(name="Editor"))

        self.education = Education.objects.create(
            level="S1 Ilmu Komputer", institution_name="Universitas Indonesia",
            start_year=2025, end_year="Sekarang",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])
        self.payload = {
            "level": "SMA", "institution_name": "SMAN 1 Sumatera Barat",
            "start_year": 2022, "end_year": "2025",
            "description": "Jurusan MIPA", "logo_url": "",
        }

    def assert_education_unchanged(self):
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "Universitas Indonesia")
        self.assertEqual(self.education.level, "S1 Ilmu Komputer")

    # ---------- Membaca data ----------
    def test_guest_can_read_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        item = response.data[0]
        self.assertEqual(item["id"], str(self.education.id))
        self.assertEqual(item["star_count"], 0)
        self.assertFalse(item["is_starred"])
        # Relasi stars (id User) dan data akun tidak boleh ikut tampil
        self.assertNotIn("stars", item)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["institution_name"], "Universitas Indonesia")

    def test_browsable_api_page_opens(self):
        response = self.client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Education List")

    def test_search_with_query_param(self):
        Education.objects.create(level="SMA", institution_name="SMAN 1", start_year=2022, end_year="2025")
        response = self.client.get(self.list_url, {"q": "universitas"})
        self.assertEqual([e["institution_name"] for e in response.data], ["Universitas Indonesia"])
        # Pencarian juga mencocokkan jenjang
        response = self.client.get(self.list_url, {"q": "sma"})
        self.assertEqual([e["level"] for e in response.data], ["SMA"])
        response = self.client.get(self.list_url, {"q": "tidak-ada"})
        self.assertEqual(response.data, [])

    def test_missing_education_returns_404(self):
        url = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.patch(url, {"level": "S2"}, format="json").status_code, 404)

    # ---------- Penolakan per peran ----------
    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.user):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.list_url, self.payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            response = self.client.patch(self.detail_url, {"institution_name": "Diubah"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            response = self.client.put(self.detail_url, self.payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            response = self.client.delete(self.detail_url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Isi database tetap sama: tidak ada data baru, tidak berubah, tidak terhapus
        self.assertEqual(Education.objects.count(), 1)
        self.assert_education_unchanged()

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"institution_name": "UI Depok"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "UI Depok")
        self.assertEqual(self.education.level, "S1 Ilmu Komputer")   # field lain tidak berubah

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.level, "SMA")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Education.objects.count(), 1)
        self.assertTrue(Education.objects.filter(pk=self.education.id).exists())

    def test_staff_without_editor_group_cannot_write(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"institution_name": "Diubah"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_education_unchanged()

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Education.objects.get(pk=response.data["id"])
        self.assertEqual(created.institution_name, "SMAN 1 Sumatera Barat")

        response = self.client.patch(self.detail_url, {"end_year": "2029"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.end_year, "2029")

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=self.education.id).exists())

    def test_wrong_method_returns_405(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # ---------- Validasi input ----------
    def test_invalid_input_returns_400(self):
        self.client.force_authenticate(user=self.owner)
        cases = [
            ({"institution_name": "   "}, "institution_name"),
            ({"institution_name": '<img src="x" onerror="alert(1)">'}, "institution_name"),
            ({"level": "<script></script>"}, "level"),
            ({"end_year": ""}, "end_year"),
            ({"start_year": "bukan-angka"}, "start_year"),
            ({"start_year": 1800}, "start_year"),
            ({"start_year": 2025, "end_year": "2020"}, "end_year"),
            ({"logo_url": "javascript:alert(1)"}, "logo_url"),
        ]
        for changes, field in cases:
            with self.subTest(field=field, changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        self.assertEqual(Education.objects.count(), 1)

    def test_put_requires_all_fields(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(self.detail_url, {"level": "S2"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("institution_name", response.data)
        self.assert_education_unchanged()

    def test_patch_validates_against_existing_data(self):
        # end_year baru dibandingkan dengan start_year lama (2025)
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"end_year": "2010"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.education.refresh_from_db()
        self.assertEqual(self.education.end_year, "Sekarang")

    def test_html_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload,
            "institution_name": "<b>SMAN 1</b> Padang",
            "description": "<script>alert(1)</script>Juara kelas",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Education.objects.get(pk=response.data["id"])
        self.assertEqual(created.institution_name, "SMAN 1 Padang")
        self.assertEqual(created.description, "alert(1)Juara kelas")

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True, "stars": [self.user.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(Education.objects.get(pk=response.data["id"]).stars.count(), 0)

    # ---------- Star ----------
    def test_guest_cannot_star(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.education.stars.count(), 0)

    def test_regular_user_can_star_and_unstar(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(self.education.stars.filter(pk=self.user.pk).exists())
        # Data akun pemberi star tidak ikut tampil
        self.assertNotIn("biasa@example.com", str(response.data))

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(self.education.stars.filter(pk=self.user.pk).exists())

    def test_star_always_uses_request_user(self):
        # Mengirim id user lain di body tidak berpengaruh
        self.client.force_authenticate(user=self.user)
        self.client.post(self.star_url, {"user": self.owner.id}, format="json")
        self.assertEqual(list(self.education.stars.all()), [self.user])

    def test_is_starred_follows_logged_in_user(self):
        self.education.stars.add(self.user)
        self.client.force_authenticate(user=self.user)
        self.assertTrue(self.client.get(self.detail_url).data["is_starred"])
        self.client.force_authenticate(user=self.editor)
        response = self.client.get(self.detail_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

    def test_star_missing_education_returns_404(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("api:education-star", args=[uuid.uuid4()])
        self.assertEqual(self.client.post(url).status_code, status.HTTP_404_NOT_FOUND)

    # ---------- CSRF dengan login sungguhan ----------
    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

    def test_star_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="biasa", password="test-password")
        self.assertEqual(client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.education.stars.count(), 0)

    def test_session_write_with_csrf_from_page_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="editor", password="test-password")
        # Halaman Education memasang cookie csrftoken (@ensure_csrf_cookie)
        page = client.get(reverse("main:show_education"))
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.patch(
            self.detail_url, {"institution_name": "UI"}, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "UI")


class EducationPageTest(APITestCase):
    """Halaman Education hanya menampilkan tombol sesuai peran; datanya dari API."""

    def setUp(self):
        self.url = reverse("main:show_education")
        self.owner = User.objects.create_superuser(username="owner", password="pw")
        self.editor = User.objects.create_user(username="editor", password="pw")
        self.editor.groups.add(Group.objects.create(name="Editor"))

    def test_page_points_to_api(self):
        response = self.client.get(self.url)
        self.assertContains(response, reverse("api:education-list"))
        self.assertContains(response, 'data-can-edit="false"')
        self.assertNotContains(response, 'id="open-add-modal"')
        self.assertNotContains(response, 'id="eduModal"')
        self.assertIn("csrftoken", response.cookies)

    def test_editor_sees_edit_modal_but_no_add_button(self):
        self.client.login(username="editor", password="pw")
        response = self.client.get(self.url)
        self.assertContains(response, 'id="eduModal"')
        self.assertContains(response, 'data-can-edit="true"')
        self.assertContains(response, 'data-can-delete="false"')
        self.assertNotContains(response, 'id="open-add-modal"')

    def test_owner_sees_add_button(self):
        self.client.login(username="owner", password="pw")
        response = self.client.get(self.url)
        self.assertContains(response, 'id="open-add-modal"')
        self.assertContains(response, 'data-can-delete="true"')
