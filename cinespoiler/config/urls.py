from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Funciones para las vistas
def home(request):
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cinespoiler - API</title>
            <style>
                body { font-family: Arial; text-align: center; margin-top: 50px; background: #1e3c72; color: white; }
                .container { max-width: 600px; margin: auto; background: white; color: #333; padding: 30px; border-radius: 20px; }
                a { color: #2a5298; text-decoration: none; }
                button { background: #2a5298; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎬 Cinespoiler API</h1>
                <p>Bienvenido a la API del sistema de cine</p>
                <p>📡 Endpoints disponibles:</p>
                <ul style="text-align: left;">
                    <li><code>/api/movies/</code> - Películas</li>
                    <li><code>/api/genres/</code> - Géneros</li>
                    <li><code>/api/rooms/</code> - Salas</li>
                    <li><code>/api/showtimes/</code> - Funciones</li>
                    <li><code>/api/stats/advanced/</code> - Estadísticas</li>
                    <li><code>/api/movies/random/</code> - Recomendación aleatoria</li>
                </ul>
                <a href="/frontend/"><button>🎨 Ir al Frontend</button></a>
                <br><br>
                <a href="/admin/">🔐 Panel Admin</a>
            </div>
        </body>
        </html>
    """)

def frontend(request):
    from django.conf import settings
    import os
    file_path = os.path.join(settings.BASE_DIR, 'static', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read())

urlpatterns = [
    path('', home, name='home'),
    path('frontend/', frontend, name='frontend'),
    path('admin/', admin.site.urls, name='admin'),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API
    path('api/', include('movies.urls')),
]