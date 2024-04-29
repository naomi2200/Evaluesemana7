from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, RoomViewSet, ShowtimeViewSet, BookingViewSet, pelicula_aleatoria
from .auth_views import register, user_profile
from .stats_advanced import stats_advanced

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'showtimes', ShowtimeViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('recomendar/', pelicula_aleatoria, name='recomendar'),
    path('register/', register, name='register'),
    path('profile/', user_profile, name='profile'),
    path('stats/advanced/', stats_advanced, name='stats-advanced'),
    path('', include(router.urls)),
]