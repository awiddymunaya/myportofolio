/**
 * utils.js — fungsi bantu yang dipakai bersama oleh halaman-halaman AJAX.
 * Dimuat sekali lewat base.html, jadi bisa dipanggil dari skrip halaman mana pun.
 */

/** Mengambil nilai cookie berdasarkan nama (dipakai untuk token CSRF). */
function getCookie(name) {
    if (!document.cookie) return null;
    const prefix = name + "=";
    for (const rawCookie of document.cookie.split(";")) {
        const cookie = rawCookie.trim();
        if (cookie.startsWith(prefix)) {
            return decodeURIComponent(cookie.substring(prefix.length));
        }
    }
    return null;
}

/**
 * Token CSRF untuk request POST.
 * Utamakan input tersembunyi dari {% csrf_token %} di halaman, lalu cookie "csrftoken".
 */
function getCsrfToken() {
    const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return (input && input.value) || getCookie("csrftoken") || "";
}

/**
 * Meng-escape karakter khusus HTML agar teks dari server tidak dieksekusi
 * sebagai HTML/JavaScript ketika disisipkan dengan innerHTML (pencegahan XSS).
 */
function escapeHtml(value) {
    if (value === null || value === undefined) return "";
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * Hanya mengizinkan URL gambar http(s) atau jalur relatif seperti /static/img/foto.jpg.
 * Skema lain (javascript:, data:, dsb.) dikembalikan sebagai string kosong.
 */
function safeUrl(value) {
    if (!value) return "";
    try {
        const url = new URL(String(value).trim(), window.location.origin);
        return url.protocol === "http:" || url.protocol === "https:" ? url.href : "";
    } catch (error) {
        return "";
    }
}

/**
 * Debounce: menunda pemanggilan `fn` sampai pengguna berhenti memicu event
 * selama `delay` milidetik. Setiap pemicu baru membatalkan timer sebelumnya.
 */
function debounce(fn, delay = 400) {
    let timerId;
    return function (...args) {
        clearTimeout(timerId);
        timerId = setTimeout(() => fn.apply(this, args), delay);
    };
}

/** Mengubah "2024-08-01" menjadi "Agu 2024" (format Indonesia). */
function formatMonthYear(isoDate) {
    if (!isoDate) return "";
    const [year, month] = isoDate.split("-").map(Number);
    if (!year || !month) return "";
    return new Date(year, month - 1, 1).toLocaleDateString("id-ID", {
        month: "short",
        year: "numeric",
    });
}

/** Membaca body respons sebagai JSON tanpa melempar error jika body bukan JSON. */
async function readJsonSafely(response) {
    try {
        return await response.json();
    } catch (error) {
        return {};
    }
}