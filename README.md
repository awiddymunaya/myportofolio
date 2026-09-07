Nama : Awiddy Munaya Rajanadoli



NPM : 2506622872



Kelas : PBP D



\### Tugas 1



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

