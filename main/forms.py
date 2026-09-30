{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- Sesuai Langkah 3: Menambahkan block meta -->
    {% block meta %} {% endblock meta %}
    
    <title>Awiddy Munaya</title>
    
    <!-- Link font dan CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">

    <!-- CSS TAMBAHAN UNTUK TOAST NOTIFICATION -->
    <style>
        #toast-container {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .custom-toast {
            min-width: 250px;
            background-color: #0f2b5b; /* Tema Royal Blue */
            color: #ffffff;
            padding: 16px 20px;
            border-radius: 8px;
            border-left: 6px solid #D4AF37; /* Aksen Gold */
            box-shadow: 0 10px 25px rgba(15, 43, 91, 0.2);
            font-family: 'Segoe UI', system-ui, sans-serif;
            font-size: 14px;
            font-weight: 600;
            opacity: 0;
            transform: translateX(100%);
            transition: opacity 0.4s ease, transform 0.4s ease;
        }

        .custom-toast.show {
            opacity: 1;
            transform: translateX(0);
        }
    </style>
</head>
<body style="background-color: #fafbfc; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    
    <!-- Animasi Mahkota Background -->
    <div class="floating-crown crown1">👑</div>
    <div class="floating-crown crown2">👑</div>
    <div class="floating-crown crown3">👑</div>
    <div class="floating-crown crown4">👑</div>
    <div class="floating-crown crown5">👑</div>

    <!-- HEADER BARU: Desain Elegan Royal Blue & Gold -->
    <header class="site-header" style="background-color: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 15px rgba(15, 43, 91, 0.08); padding: 15px 0;">
      <div class="container" style="display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto; padding: 0 20px;">
          
          <!-- Logo / Nama Brand -->
          <a href="{% url 'main:show_main' %}" class="brand" style="font-size: 22px; font-weight: 900; color: #0f2b5b; text-decoration: none; letter-spacing: 0.5px;">{{ name }}</a>
          
          <!-- Navigasi Utama -->
          <nav style="display: flex; align-items: center; gap: 25px;">
              <a href="{% url 'main:show_main' %}" style="color: #0f2b5b; font-weight: 700; text-decoration: none; font-size: 15px; transition: color 0.2s;">Profile</a>
              <a href="{% url 'main:show_experience' %}" style="color: #0f2b5b; font-weight: 700; text-decoration: none; font-size: 15px; transition: color 0.2s;">Experience</a>
              <a href="{% url 'main:show_education' %}" style="color: #0f2b5b; font-weight: 700; text-decoration: none; font-size: 15px; transition: color 0.2s;">Education</a>

              <!-- Garis Pemisah Vertikal -->
              <div style="width: 1px; height: 20px; background-color: #ddd; margin: 0 5px;"></div>

              {% if user.is_authenticated %}
                  <span style="color: #D4AF37; font-weight: bold; font-size: 15px;">Halo, {{ user.username }}</span>
                  <!-- Tombol Logout Merah Elegan -->
                  <a href="{% url 'main:logout' %}" style="color: #c62828; border: 1px solid #c62828; padding: 6px 16px; border-radius: 20px; text-decoration: none; font-size: 13px; font-weight: bold; transition: all 0.2s;">Logout</a>
              {% else %}
                  <!-- Tombol Login -->
                  <a href="{% url 'main:login' %}" style="color: #0f2b5b; font-weight: bold; text-decoration: none; font-size: 15px;">Login</a>
                  <!-- Tombol Register (Gradasi Emas) -->
                  <a href="{% url 'main:register' %}" style="background: linear-gradient(135deg, #D4AF37, #B5952F); color: white; padding: 8px 22px; border-radius: 20px; text-decoration: none; font-weight: bold; font-size: 14px; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.3); transition: transform 0.2s;">Register</a>
              {% endif %}
          </nav>
      </div>
    </header>

    <!-- Sesuai Langkah 4: Menambahkan block content -->
    <main style="min-height: 80vh;">
        {% block content %}
        {% endblock content %}
    </main>

    <!-- FOOTER BARU: Diselaraskan dengan Royal Blue & Gold -->
    <footer class="site-footer" style="background-color: #0f2b5b; color: rgba(255, 255, 255, 0.8); text-align: center; padding: 25px 0; border-top: 4px solid #D4AF37; margin-top: auto;">
        <div class="container">
            <p style="margin: 0; font-size: 14px;">&copy; 2026 <strong>{{ name }}</strong>. Fakultas Ilmu Komputer, Universitas Indonesia.</p>
        </div>
    </footer>

    <!-- WADAH & SKRIP TOAST NOTIFICATION -->
    <div id="toast-container"></div>
    <script>
        function showToast(message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.classList.add('custom-toast');
            toast.innerText = message;
            container.appendChild(toast);

            setTimeout(() => { toast.classList.add('show'); }, 10);
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => { toast.remove(); }, 400);
            }, 3000);
        }

        {% if messages %}
            {% for message in messages %}
                showToast("{{ message }}");
            {% endfor %}
        {% endif %}
    </script>
</body>
</html>