/**
 * toast.js — notifikasi toast yang bisa dipakai di semua halaman (dimuat lewat base.html).
 *
 * Pemakaian:
 *   showToast("Data berhasil ditambahkan!");          // sukses (default)
 *   showToast("Judul tidak boleh kosong.", "error");  // gagal
 *   showToast("Sedang memuat...", "info");
 *
 * Pesan disisipkan dengan textContent sehingga aman dari XSS.
 */
function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const icons = {
        success: "fa-circle-check",
        error: "fa-circle-exclamation",
        info: "fa-circle-info",
    };
    const variant = icons[type] ? type : "success";

    const toast = document.createElement("div");
    toast.className = `custom-toast ${variant}`;
    toast.setAttribute("role", variant === "error" ? "alert" : "status");

    const icon = document.createElement("i");
    icon.className = `fa-solid ${icons[variant]}`;
    icon.setAttribute("aria-hidden", "true");

    const text = document.createElement("span");
    text.textContent = message;

    toast.append(icon, text);
    container.appendChild(toast);

    // Pesan error ditampilkan sedikit lebih lama agar sempat dibaca
    const duration = variant === "error" ? 4500 : 3000;

    setTimeout(() => toast.classList.add("show"), 10);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 400);
    }, duration);
}