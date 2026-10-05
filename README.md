# 👑 Royal Portfolio - Awiddy Munaya

Nama : Awiddy Munaya Rajanadoli

NPM : 2506622872

Kelas : PBP D

Proyek ini adalah sebuah aplikasi web portofolio pribadi berbasis Django yang dirancang untuk menampilkan profil, riwayat pengalaman, dan riwayat pendidikan dengan balutan antarmuka eksklusif bertema **Royal Blue & Gold**. Aplikasi ini dikembangkan sebagai pemenuhan Tugas Individu mata kuliah Pemrograman Berbasis Platform (CSGE602022) di Fakultas Ilmu Komputer, Universitas Indonesia.

## 🚀 Fitur Utama
* **Desain Eksklusif:** Antarmuka responsif dengan skema warna yang konsisten dan animasi interaktif.
* **Role-Based Access Control (RBAC):** Sistem otorisasi 4 tingkat (Superuser, Editor, Pengguna Biasa, dan Pengunjung Anonim) yang membatasi hak akses CRUD di sisi server maupun tampilan UI.
* **Fitur Interaktif (Star):** Pengguna yang sudah *login* dapat memberikan *star* (bintang) pada riwayat pengalaman favorit layaknya platform profesional.
* **Halaman Experience berbasis AJAX:** Data dimuat lewat `fetch()`, pencarian dengan *debouncing*, tambah data lewat modal, notifikasi *toast*, serta perlindungan XSS di sisi server dan klien.

## 📅 Progres Mingguan

| Tugas | Topik | Hasil utama |
| --- | --- | --- |
| Tugas 1 | Static Web (HTML5 & CSS3) | Halaman profil dan *experience* statis yang responsif |
| Tugas 2 | MVT pada Django | Model `Experience` & `Education`, *view*, dan *template* |
| Tugas 3 | Form & Data Delivery | `ModelForm`, form tambah data, endpoint JSON |
| Tugas 4 | Authentication, Session & Cookies | Login/register, RBAC 4 peran, cookie `last_login`, fitur *star* |
| Tugas 5 | Web Interactivity with JavaScript | AJAX, *debouncing*, modal, *toast*, perlindungan XSS |

---

## 🛠️ Instruksi Setup Lokal

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di mesin lokalmu:

1. **Kloning repositori**
   ```bash
   git clone <URL_REPOSITORI_GITHUB_KAMU>
   cd myportofolio
   ```
2. **Buat dan aktifkan *virtual environment***
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # macOS / Linux
   source env/bin/activate
   ```
3. **Pasang dependensi**
   ```bash
   pip install -r requirements.txt
   ```
4. **Jalankan migrasi database**
   ```bash
   python manage.py migrate
   ```
5. **Buat akun Pemilik (superuser)**. Peran Editor dibuat dengan menambahkan grup bernama `Editor` lewat halaman `/admin`.
   ```bash
   python manage.py createsuperuser
   ```
6. **Jalankan server**
   ```bash
   python manage.py runserver
   ```
   Buka `http://127.0.0.1:8000/`.

---

## Tugas 1

1. Di tugas ini, aku lumayan banyak pakai elemen semantik HTML5 kayak `<section>`, `<main>`, `<header>`, dan `<footer>`. Ternyata elemen-elemen ini ngebantu banget buat menstrukturkan *codingan*. Dibanding cuma pakai `<div>` di mana-mana yang bikin pusing pas lagi *nge-debug*, pakai elemen semantik bikin kode HTML jauh lebih rapi dan jelas pembagiannya (mana blok untuk profil, mana yang khusus untuk *experience*). Selain lebih gampang dibaca oleh manusia, dari yang aku pelajari ini juga praktik yang bagus buat SEO dan *accessibility* *website*-nya.

2. Tantangan paling berasa pas ngatur CSS supaya *responsive* itu waktu masukin foto-foto kegiatan ke dalam kotak (*card*) *experience*. Karena ukuran asli fotonya beda-beda, tinggi kotaknya sempat jadi berantakan dan nggak sejajar. Akhirnya aku ngakalin pakai CSS Grid dan nambahin `object-fit: cover` serta `width: 100%` di gambarnya biar otomatis rapi dan nggak gepeng. Buat tampilan *mobile* (layar kecil), aku mutusin buat ngubah susunan *grid*-nya jadi satu kolom memanjang ke bawah. Alasannya simpel: kalau dipaksa berjejer ke samping di HP, kontennya bakal kekecilan dan malah susah dibaca *user*.

3. Karena ini masih *static web* murni, batasan yang paling bikin repot adalah proses *update* kontennya. Kalau misalnya bulan depan aku mau nambahin pengalaman organisasi baru atau sekadar ganti foto profil, aku harus buka *file* HTML-nya lagi, nulis kode secara manual (*hardcode*), terus ngulang proses *commit* dan *push* ke GitHub dan PWS. Lumayan ribet. Makanya buat iterasi proyek selanjutnya, aku pengen banget nambahin fungsionalitas dinamis pakai *database*. Jadi nanti kalau mau nambah portofolio, tinggal masukin data lewat semacam halaman admin, dan *website*-nya bisa otomatis ter-*update* tanpa harus nyentuh-nyentuh kode HTML lagi.

### AI Disclosure & Collaboration Notes

Dalam mengerjakan tugas portofolio ini, saya berkolaborasi dengan AI Gemini sebagai *thought partner*. Berikut adalah rincian transparan mengenai pemanfaatannya:

1. **Tools yang Digunakan:**
   - Gemini (sebagai asisten pengembang dan pemecah masalah teknis).
   - Git Bash & Python untuk implementasi kode.

2. **Bagian Spesifik yang Dibantu oleh AI:**
   - Membantu menyusun struktur kode CSS Grid untuk tata letak kotak pengalaman (*card layout*) dan properti `object-fit` agar gambar seragam.
   - Mengatasi kendala teknis saat server lokal gagal terhubung (*localhost refused to connect*) dan masalah format gambar `.HEIC` dari perangkat seluler yang tidak terbaca oleh browser.
   - Memberikan alternatif palet warna tema Royal Navy & Muted Gold menggunakan variabel CSS (`:root`).

3. **Strategi Prompt & Evaluasi Kritis (Perbaikan Manual):**
   - Prompt awal: Meminta bantuan untuk merancang kotak *experience* agar responsif dan sejajar tingginya.
   - Evaluasi dan Perbaikan Manual: Meskipun AI memberikan solusi tata letak dasar, saya harus melakukan penyesuaian manual secara aktif. Contohnya, ketika kotak pengalaman memanjang sebelah akibat ada kartu yang belum memiliki foto, saya mengevaluasi ulang solusinya dengan menerapkan Flexbox (`flex-direction: column`) dan `margin-top: auto` agar posisi teks durasi tetap konsisten di bagian bawah kartu. Saya juga harus secara manual mengonversi format foto `.HEIC` ke `.JPG` dan memperbaiki kesalahan penulisan nama file (*typo*) pada direktori `static/img/` agar gambar dapat dimuat dengan sempurna di server PWS.

4. **Cuplikan Log Prompting Utama:**
   - Prompt 1: "Bagaimana cara membuat section Experience dengan card grid di Django dan CSS agar responsif?"
   - Prompt 2: "Kenapa foto berformat .HEIC tidak muncul di browser dan bagaimana cara mengatasinya?"
   - Prompt 3: "Bagaimana cara meratakan tinggi card Experience di CSS Grid meskipun salah satu card belum memiliki foto?"

---

## Tugas 2

1. Ketika pengguna membuka halaman baru, `urls.py` proyek menerima *request* dan mengarahkannya ke `urls.py` aplikasi, yang kemudian memanggil fungsi *view* untuk mengambil data dari model di database sebelum akhirnya merender dan mengembalikan halaman tersebut ke browser menggunakan *template*.

2. Data portofolio sebaiknya disimpan pada model alih-alih ditulis langsung di dalam *template* agar logika data terpisah dari tampilan HTML, sehingga proses pemeliharaan, penambahan, maupun pembaruan data dapat dilakukan dengan mudah melalui database atau admin panel tanpa harus merusak struktur kode *template*.

3. Perintah `makemigrations` berfungsi untuk mendeteksi perubahan pada `models.py` dan menghasilkan berkas cetak biru migrasi, sedangkan `migrate` berfungsi mengeksekusi berkas tersebut untuk menerapkan perubahan skema secara nyata ke database, seperti saat saya membuat model `Education` baru untuk menyimpan data riwayat sekolah.

### AI Disclosure
* **Tools yang Digunakan:** Gemini (Google)
* **Bagian yang Dibantu:** Membantu perancangan model `Education`, *debugging* unit test, penataan *styling* CSS halaman *education*, serta penyusunan jawaban pertanyaan reflektif Tugas 2.
* **Strategi Prompting:** Menggunakan pendekatan iteratif dengan memberikan kode yang sedang error atau bagian *markup* yang ingin diubah secara spesifik.

---

## Tugas 3

1. **Mengapa menggunakan `ModelForm` dan perlunya `{% csrf_token %}`?**
   Kita menggunakan `ModelForm` karena Django dapat secara otomatis men-*generate* form HTML berdasarkan *field* yang sudah kita definisikan pada model database. Hal ini sangat efisien, mencegah duplikasi penulisan kode, dan otomatis menangani validasi data dari *input* pengguna.
   Sementara itu, `{% csrf_token %}` wajib ditambahkan pada setiap form yang menggunakan metode POST untuk melindungi situs dari serangan *Cross-Site Request Forgery* (CSRF). Token ini memverifikasi bahwa *request* modifikasi data yang masuk benar-benar berasal dari form di *website* kita sendiri, bukan dari skrip berbahaya di situs pihak ketiga.

2. **Mengapa JSON lebih disukai dibandingkan XML?**
   JSON (*JavaScript Object Notation*) lebih mendominasi pengembangan web modern karena strukturnya yang jauh lebih ringan dan ringkas. Berbeda dengan XML yang menggunakan sistem *tag* pembuka dan penutup yang panjang (*verbose*), JSON menggunakan format pasangan *key-value* yang mudah dibaca oleh manusia maupun mesin. Selain itu, JSON didukung secara *native* oleh JavaScript, sehingga proses *parsing* data di sisi *frontend* (seperti React, Vue, atau Vanilla JS) menjadi sangat cepat dan langsung bisa digunakan sebagai objek.

3. **Alur fungsi *view* JSON dan pentingnya *serialization*:**
   Alurnya dimulai saat *client* meminta data (melalui akses URL). *URL dispatcher* meneruskan *request* ke fungsi *view* terkait. Di dalam *view*, kita melakukan *query* ke database menggunakan ORM Django untuk mendapatkan data portofolio (yang saat ini masih berupa *QuerySet* atau objek Python).
   Kita perlu melakukan **serialization** karena protokol HTTP tidak bisa mengirimkan objek Python mentah secara langsung. *Serialization* bertugas menerjemahkan objek Python kompleks tersebut menjadi format teks standar (JSON). Setelah menjadi *string* JSON, barulah data tersebut dibungkus dalam `HttpResponse` dengan `content_type="application/json"` dan dikembalikan ke *client*.

### AI Disclosure
Dalam pengerjaan tugas minggu ini, saya menggunakan bantuan AI (*Large Language Model*) sebagai *thought partner* dan asisten *debugging*.
* **Prompting Strategy:** Saya memberikan konteks berupa potongan kode (models, forms, views) dan *error traceback* dari terminal untuk mencari akar masalah saat terjadi kegagalan migrasi di PWS.
* **Keterbatasan AI:** AI terkadang tidak mengetahui status terkini dari *database* lokal saya atau salah memberikan asumsi terkait riwayat file migrasi yang bertabrakan.
* **Perbaikan Manual:** Saya secara manual harus memverifikasi urutan *dependencies* pada file migrasi (`0005_...py`), menghapus file migrasi yang *corrupt*, menyesuaikan *styling* CSS menggunakan tema 'Royal Blue' dan 'Gold' yang spesifik untuk UI portofolio saya, dan menjalankan perintah `dumpdata` untuk mengatur fitur *Data Migration* agar sinkron dengan PWS.

---

## Tugas 4

### AI Disclosure
* **Tools yang digunakan:** Google Gemini.
* **Strategi Prompting:** Saya menggunakan pendekatan *iterative prompting* dengan cara memberikan potongan kode (*code snippets*) dan tangkapan layar (*screenshots*) dari UI yang ada, lalu meminta AI untuk memberikan umpan balik desain serta merapikan struktur logika Python/Django yang saya buat agar sesuai dengan praktik terbaik (*best practices*).
* **Spesifikasi Bantuan AI:**
  * **UI/UX Redesign:** AI membantu merombak struktur CSS dan HTML pada `base.html`, `index.html`, `experience.html`, dan `education.html` untuk menyatukan desain menjadi tema "Royal Blue dan Emas" yang konsisten, membuang elemen warna yang bertabrakan, dan merancang kotak pencarian yang lebih elegan.
  * **Implementasi Otorisasi (RBAC):** AI membantu membimbing pembuatan logika berbasis *role* di `views.py` menggunakan `request.user.is_superuser` dan pengecekan grup Editor, serta menyembunyikan tombol-tombol aksi (Tambah, Edit, Hapus) di file *template* berdasarkan hak akses tersebut.
  * **Penyusunan Logika Fitur Star:** AI membantu merancang relasi `ManyToManyField` pada `models.py` dan struktur logika percabangan untuk fitur `toggle_star` di *views*.
  * **Debugging Server:** AI membantu menjelaskan alasan mengapa database lokal SQLite tidak otomatis terunggah ke PWS dan menyarankan alur *testing* menggunakan pembuatan akun baru langsung di server.

---

## Tugas 5

1. ***Debouncing*** adalah teknik menunda eksekusi sebuah fungsi sampai *event* pemicunya berhenti terjadi selama jeda waktu tertentu. Setiap kali *event* baru muncul sebelum jeda habis, timer di-*reset*. Pada fitur pencarian AJAX, *event* `input` terpicu di setiap ketikan. Tanpa *debouncing*, mengetik kata "volunteer" (9 huruf) akan mengirim 9 *request* ke server, padahal yang dibutuhkan hanya hasil untuk kata terakhir. Dengan *debouncing* (di proyek ini `debounce(loadExperiences, 400)`), *request* baru dikirim 400 ms setelah pengguna berhenti mengetik, sehingga hanya 1 *request* yang terkirim. Teknik ini penting karena:
   - mengurangi beban server dan *query* database yang sia-sia;
   - menghemat *bandwidth*, terutama bagi pengguna dengan koneksi lambat;
   - mengurangi *race condition*, yaitu respons dari *request* lama yang datang terlambat lalu menimpa hasil pencarian terbaru (di proyek ini juga ditambah `AbortController` untuk membatalkan *request* yang sudah usang);
   - membuat tampilan lebih stabil karena daftar tidak berkedip di setiap huruf.

2. `fetch()` tidak langsung mengembalikan data, melainkan sebuah **Promise** yang baru selesai (*resolve*) setelah respons dari server tiba. Kata kunci `await` (yang hanya bisa dipakai di dalam fungsi `async`) menjeda eksekusi fungsi tersebut sampai Promise selesai, lalu memberikan nilai hasilnya, yaitu objek `Response`. Selama menunggu, *thread* utama browser **tidak terblokir**, sehingga halaman tetap responsif. `await` juga diperlukan pada `response.json()` karena membaca *body* respons juga bersifat asinkron. Selain itu, jika Promise gagal (*reject*), misalnya karena koneksi terputus, error-nya bisa ditangkap dengan `try...catch` biasa.
   Jika `await` tidak digunakan, variabel `response` akan berisi **Promise yang belum selesai**, bukan objek `Response`. Akibatnya `response.ok` bernilai `undefined` dan pemanggilan `response.json()` akan error karena Promise tidak punya method `json`. Kode setelahnya juga langsung berjalan sebelum data tiba, sehingga daftar dirender kosong atau berisi `undefined`, dan error jaringan tidak tertangkap oleh `try...catch` (menjadi *unhandled promise rejection*). Alternatif tanpa `await` adalah merangkai `.then()`, tetapi kodenya menjadi lebih sulit dibaca.

3. **XSS (*Cross-Site Scripting*)** adalah serangan di mana penyerang menyisipkan kode berbahaya (biasanya JavaScript) ke dalam data yang nantinya ditampilkan di halaman web, sehingga kode tersebut dieksekusi di browser pengguna lain dalam konteks situs kita. Dampaknya antara lain mencuri *cookie* atau data sesi, melakukan aksi atas nama korban, mengubah tampilan halaman, atau mengarahkan korban ke situs *phishing*. Contohnya, jika judul pengalaman diisi `<img src="x" onerror="alert('XSS!')">` lalu ditampilkan apa adanya, atribut `onerror` akan dijalankan oleh browser setiap kali halaman dibuka.
   Data yang ditampilkan lewat AJAX/JavaScript lebih rentan karena **tidak ada *auto-escaping***. *Template* Django secara bawaan meng-*escape* setiap variabel `{{ ... }}` (misalnya `<` menjadi `&lt;`), sehingga data otomatis tampil sebagai teks biasa kecuali kita sengaja memakai filter `|safe`. Sebaliknya, ketika data diambil sebagai JSON lalu disisipkan ke halaman lewat `innerHTML` atau *template literal*, browser mem-*parse* string tersebut sebagai HTML apa adanya, sehingga tanggung jawab *escaping* sepenuhnya ada pada *developer*. Satu tempat saja yang lupa di-*escape* sudah cukup untuk membuka celah. Karena itu, proyek ini memakai pertahanan berlapis:
   - di sisi server, `strip_tags` pada method `clean_<field>` di `ModelForm` menolak atau membersihkan tag HTML sebelum data disimpan;
   - di sisi klien, setiap nilai teks di-*escape* dengan `escapeHtml()` atau disisipkan lewat `textContent`;
   - URL gambar disaring dengan `safeUrl()` agar hanya `http(s)` atau jalur relatif yang diizinkan.

### Ringkasan Implementasi Tugas 5

Pola AJAX dari Tutorial 05 diterapkan pada halaman **Experience** (bagian dari Tugas 3 dan 4 yang memiliki fitur *star*).

| Kebutuhan | Implementasi |
| --- | --- |
| Menampilkan data dengan AJAX | `show_experience` hanya merender kerangka halaman. Data diambil dengan `fetch()` dari endpoint `GET /experience/json/` (`show_experience_json`) yang disusun manual dengan `JsonResponse`, termasuk `star_count` dan `is_starred` untuk pengguna yang sedang login. |
| Loading, kosong, error | *Skeleton* saat memuat, pesan khusus saat data kosong atau tidak ada hasil pencarian, serta pesan error dengan tombol "Coba lagi". |
| Pencarian dengan *debouncing* | Pencarian berdasarkan judul/posisi (`?q=`) dengan jeda 400 ms, ditambah filter kategori. *Request* lama dibatalkan dengan `AbortController`. |
| Tambah data lewat modal | Form `ExperienceForm` di dalam modal, dikirim ke `POST /api/experience/add-ajax/`. Server membalas JSON dengan status **201** (berhasil), **400** (validasi gagal, beserta pesan per *field*), atau **403** (bukan Pemilik). Daftar diperbarui tanpa *reload*. |
| Hak akses | Dicek di dalam *view* (`can_add_data`, `can_edit_data`, `can_delete_data`), bukan hanya dengan menyembunyikan tombol. Pengunjung yang belum login tetap bisa membaca data dan jumlah *star*. |
| CSRF | Tidak ada lagi `@csrf_exempt`. Setiap `POST` membawa `csrfmiddlewaretoken` dari `{% csrf_token %}` dan *header* `X-CSRFToken`. |
| *Toast* | `static/js/toast.js` dengan varian sukses dan error, dipakai untuk tambah, hapus, *star*, dan pesan validasi dari server. |
| XSS | `strip_tags` di `clean_<field>` pada `ExperienceForm` dan `EducationForm`, `escapeHtml()`/`textContent` di klien, dan `safeUrl()` untuk URL gambar. |
| Fitur tambahan | *Star* dan hapus data lewat AJAX tanpa *reload*, filter kategori, validasi tanggal selesai tidak boleh sebelum tanggal mulai, modal yang bisa ditutup dengan tombol Esc, dan fungsi bantu bersama di `static/js/utils.js`. |

**Cara menguji:**
1. Buka `/experience/` tanpa login: data dan jumlah *star* tampil, tombol tambah tidak muncul.
2. Login sebagai pengguna biasa: tombol *star* bisa dipakai, tetapi `POST /api/experience/add-ajax/` membalas 403.
3. Login sebagai Pemilik (superuser): klik **Tambah Pengalaman**, isi form, lalu simpan. Daftar langsung diperbarui dan *toast* muncul.
4. Uji XSS: isi judul dengan `<img src="x" onerror="alert('XSS!')">`. Server menolak dengan status 400 dan pesan validasi tampil di *toast*. Jika teks biasa digabung dengan tag tersebut, tag-nya dibuang dan *alert* tidak pernah muncul.

### AI Disclosure
* **Tools yang digunakan:** Claude (Anthropic) melalui claude.ai.
* **Strategi Prompting:** Saya mengunggah dokumen soal Tugas 5 beserta `models.py`, `views.py`, `forms.py`, `urls.py`, `base.html`, dan `README.md`, lalu meminta AI menganalisis kebutuhan tugas terhadap kode yang sudah ada dan membantu mengimplementasikannya. Setelah itu saya menguji hasilnya secara bertahap di server lokal.
* **Bagian yang dibantu AI:**
  * Menyusun endpoint JSON manual dengan informasi *star*, view `POST` AJAX dengan status 201/400/403, dan pengecekan hak akses di dalam *view*.
  * Menambahkan method `clean_<field>` dengan `strip_tags` pada `ModelForm`.
  * Membuat ulang `experience.html` (kerangka halaman, modal, *skeleton loading*, pencarian dengan *debounce*), serta `static/js/utils.js` dan `static/js/toast.js`.
  * Merapikan format `README.md` dan menyusun draf jawaban pertanyaan reflektif.
* **Keterbatasan AI yang saya temukan:**
  * AI tidak bisa menjalankan proyek Django saya, sehingga semua kode tetap harus saya uji sendiri dengan `python manage.py runserver` untuk setiap peran.
  * AI tidak memiliki `experience.html` versi lama saya, sehingga tampilan kartu dibuat ulang dan perlu saya cocokkan dengan desain sebelumnya.
  * AI menemukan bahwa view lama `add_experience_ajax` dan `add_education_ajax` memakai `@csrf_exempt` dan tidak mengecek hak akses, sehingga keduanya diperbaiki. Saya perlu memastikan halaman Education yang memanggil endpoint tersebut tetap berfungsi.
* **Perbaikan manual yang saya lakukan:** *(isi sesuai yang benar-benar kamu ubah atau temukan saat menguji)*
* **Log prompting:** *(tempel tautan *share* percakapan AI di sini)*