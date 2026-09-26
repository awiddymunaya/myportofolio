Nama : Awiddy Munaya Rajanadoli



NPM : 2506622872



Kelas : PBP D



\### Tugas 1



1\. Di tugas ini, aku lumayan banyak pakai elemen semantik HTML5 kayak `<section>`, `<main>`, `<header>`, dan `<footer>`. Ternyata elemen-elemen ini ngebantu banget buat menstrukturkan \*codingan\*. Dibanding cuma pakai `<div>` di mana-mana yang bikin pusing pas lagi \*nge-debug\*, pakai elemen semantik bikin kode HTML jauh lebih rapi dan jelas pembagiannya (mana blok untuk profil, mana yang khusus untuk \*experience\*). Selain lebih gampang dibaca oleh manusia, dari yang aku pelajari ini juga praktik yang bagus buat SEO dan \*accessibility\* \*website\*-nya.



2\. tantangan paling berasa pas ngatur CSS supaya \*responsive\* itu waktu masukin foto-foto kegiatan ke dalam kotak (\*card\*) \*experience\*. Karena ukuran asli fotonya beda-beda, tinggi kotaknya sempat jadi berantakan dan nggak sejajar. Akhirnya aku ngakalin pakai CSS Grid dan nambahin `object-fit: cover` serta `width: 100%` di gambarnya biar otomatis rapi dan nggak gepeng. Buat tampilan \*mobile\* (layar kecil), aku mutusin buat ngubah susunan \*grid\*-nya jadi satu kolom memanjang ke bawah. Alasannya simpel: kalau dipaksa berjejer ke samping di HP, kontennya bakal kekecilan dan malah susah dibaca \*user\*.



3\. Karena ini masih \*static web\* murni, batasan yang paling bikin repot adalah proses \*update\* kontennya. Kalau misalnya bulan depan aku mau nambahin pengalaman organisasi baru atau sekadar ganti foto profil, aku harus buka \*file\* HTML-nya lagi, nulis kode secara manual (\*hardcode\*), terus ngulang proses \*commit\* dan \*push\* ke GitHub dan PWS. Lumayan ribet. Makanya buat iterasi proyek selanjutnya, aku pengen banget nambahin fungsionalitas dinamis pakai \*database\*. Jadi nanti kalau mau nambah portofolio, tinggal masukin data lewat semacam halaman admin, dan \*website\*-nya bisa otomatis ter- \*update\* tanpa harus nyentuh-nyentuh kode HTML lagi.



\### AI Disclosure \& Collaboration Notes



dalam mengerjakan tugas portofolio ini, saya berkolaborasi dengan AI Gemini sebagai thought partner. Berikut adalah rincian transparan mengenai pemanfaatannya:



1\. Tools yang Digunakan: 

&#x20;  - Gemini (sebagai asisten pengembang dan pemecah masalah teknis).

&#x20;  - Git Bash \& Python untuk implementasi kode.



2\. Bagian Spesifik yang Dibantu oleh AI:

&#x20;  - Membantu menyusun struktur kode CSS Grid untuk tata letak kotak pengalaman (card layout) dan properti object-fit agar gambar seragam.

&#x20;  - Mengatasi kendala teknis saat server lokal gagal terhubung (localhost refused to connect) dan masalah format gambar `.HEIC` dari perangkat seluler yang tidak terbaca oleh browser.

&#x20;  - Memberikan alternatif palet warna tema Royal Navy \& Muted Gold menggunakan variabel CSS (`:root`).



3\. Strategi Prompt \& Evaluasi Kritis (Perbaikan Manual):

&#x20;  - Prompt awal: Meminta bantuan untuk merancang kotak \*experience\* agar responsif dan sejajar tingginya.

&#x20;  - Evaluasi dan Perbaikan Manual: Meskipun AI memberikan solusi tata letak dasar, saya harus melakukan penyesuaian manual secara aktif. Contohnya, ketika kotak pengalaman memanjang sebelah akibat ada kartu yang belum memiliki foto, saya mengevaluasi ulang solusinya dengan menerapkan Flexbox (`flex-direction: column`) dan margin-top: auto agar posisi teks durasi tetap konsisten di bagian bawah kartu. Saya juga harus secara manual mengonversi format foto `.HEIC` ke `.JPG` dan memperbaiki kesalahan penulisan nama file (typo) pada direktori `static/img/` agar gambar dapat dimuat dengan sempurna di server PWS.



4\. Cuplikan Log Prompting Utama:

&#x20;  - Prompt 1: "Bagaimana cara membuat section Experience dengan card grid di Django dan CSS agar responsif?"

&#x20;  - Prompt 2: "Kenapa foto berformat .HEIC tidak muncul di browser dan bagaimana cara mengatasinya?"

&#x20;  - Prompt 3: "Bagaimana cara meratakan tinggi card Experience di CSS Grid meskipun salah satu card belum memiliki foto?"


\### Tugas 2

1\. Ketika pengguna membuka halaman baru, urls.py proyek menerima request dan mengarahkannya ke urls.py aplikasi, yang kemudian memanggil fungsi view untuk mengambil data dari model di database sebelum akhirnya merender dan mengembalikan halaman tersebut ke browser menggunakan template.

2\. Data portofolio sebaiknya disimpan pada model alih-alih ditulis langsung di dalam template agar logika data terpisah dari tampilan HTML, sehingga proses pemeliharaan, penambahan, maupun pembaruan data dapat dilakukan dengan mudah melalui database atau admin panel tanpa harus merusak struktur kode template.

3\. Perintah makemigrations berfungsi untuk mendeteksi perubahan pada models.py dan menghasilkan berkas cetak biru migrasi, sedangkan migrate berfungsi mengeksekusi berkas tersebut untuk menerapkan perubahan skema secara nyata ke database—seperti saat Anda membuat model Education baru untuk menyimpan data riwayat sekolah.

### AI Disclosure
* **Tools yang Digunakan:** Gemini (Google)
* **Bagian yang Dibantu:** Membantu perancangan model `Education`, *debugging* unit test, penataan *styling* CSS halaman *education*, serta penyusunan jawaban pertanyaan reflektif Tugas 2.
* **Strategi Prompting:** Menggunakan pendekatan iteratif dengan memberikan kode yang sedang error atau bagian *markup* yang ingin diubah secara spesifik.


### Tugas 3

1. **Mengapa menggunakan `ModelForm` dan perlunya `{% csrf_token %}`?**
   Kita menggunakan `ModelForm` karena Django dapat secara otomatis men-*generate* form HTML berdasarkan *field* yang sudah kita definisikan pada model database. Hal ini sangat efisien, mencegah duplikasi penulisan kode, dan otomatis menangani validasi data dari *input* pengguna. 
   Sementara itu, `{% csrf_token %}` wajib ditambahkan pada setiap form yang menggunakan metode POST untuk melindungi situs dari serangan *Cross-Site Request Forgery* (CSRF). Token ini memverifikasi bahwa *request* modifikasi data yang masuk benar-benar berasal dari form di *website* kita sendiri, bukan dari skrip berbahaya di situs pihak ketiga.

2. **Mengapa JSON lebih disukai dibandingkan XML?**
   JSON (*JavaScript Object Notation*) lebih mendominasi pengembangan web modern karena strukturnya yang jauh lebih ringan dan ringkas. Berbeda dengan XML yang menggunakan sistem *tag* pembuka dan penutup yang panjang (*verbose*), JSON menggunakan format pasangan *key-value* yang mudah dibaca oleh manusia maupun mesin. Selain itu, JSON didukung secara *native* oleh JavaScript, sehingga proses *parsing* data di sisi *frontend* (seperti React, Vue, atau Vanilla JS) menjadi sangat cepat dan langsung bisa digunakan sebagai objek.

3. **Alur fungsi *view* JSON dan pentingnya *serialization*:**
   Alurnya dimulai saat *client* meminta data (melalui akses URL). *URL dispatcher* meneruskan *request* ke fungsi *view* terkait. Di dalam *view*, kita melakukan *query* ke database menggunakan ORM Django untuk mendapatkan data portofolio (yang saat ini masih berupa *QuerySet* atau objek Python). 
   Kita perlu melakukan **serialization** karena protokol HTTP tidak bisa mengirimkan objek Python mentah secara langsung. *Serialization* bertugas menerjemahkan/mengubah objek Python kompleks tersebut menjadi format teks standar (JSON). Setelah menjadi *string* JSON, barulah data tersebut dibungkus dalam `HttpResponse` dengan `content_type="application/json"` dan dikembalikan ke *client*.

   ### AI Disclosure
Dalam pengerjaan tugas minggu ini, saya menggunakan bantuan AI (Large Language Model) sebagai *thought partner* dan asisten *debugging*.
* **Prompting Strategy:** Saya memberikan konteks berupa potongan kode (models, forms, views) dan *error traceback* dari terminal untuk mencari akar masalah saat terjadi kegagalan migrasi di PWS.
* **Keterbatasan AI:** AI terkadang tidak mengetahui status terkini dari *database* lokal saya atau salah memberikan asumsi terkait riwayat file migrasi yang bertabrakan.
* **Perbaikan Manual:** Saya secara manual harus memverifikasi urutan *dependencies* pada file migrasi (`0005_...py`), menghapus file migrasi yang *corrupt*, menyesuaikan *styling* CSS menggunakan tema 'Royal Blue' dan 'Gold' yang spesifik untuk UI portofolio saya, dan menjalankan perintah `dumpdata` untuk mengatur fitur *Data Migration* agar sinkron dengan PWS.


#Tugas 4
# 👑 Royal Portfolio - Awiddy Munaya

Proyek ini adalah sebuah aplikasi web portofolio pribadi berbasis Django yang dirancang untuk menampilkan profil, riwayat pengalaman, dan riwayat pendidikan dengan balutan antarmuka eksklusif bertema **Royal Blue & Gold**. Aplikasi ini dikembangkan sebagai pemenuhan Tugas Individu mata kuliah Pemrograman Berbasis Platform (CSGE602022) di Fakultas Ilmu Komputer, Universitas Indonesia.

## 🚀 Fitur Utama
* **Desain Eksklusif:** Antarmuka responsif dengan skema warna yang konsisten dan animasi interaktif.
* **Role-Based Access Control (RBAC):** Sistem otorisasi 4 tingkat (Superuser, Editor, Pengguna Biasa, dan Pengunjung Anonim) yang membatasi hak akses CRUD di sisi server maupun tampilan UI.
* **Fitur Interaktif (Star):** Pengguna yang sudah *login* dapat memberikan *star* (bintang) pada riwayat pengalaman favorit layaknya platform profesional.

---

## 🛠️ Instruksi Setup Lokal

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di mesin lokalmu:

1. **Kloning Repositori**
   ```bash
   git clone <URL_REPOSITORI_GITHUB_KAMU>
   cd myportofolio