from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Movie, Genre, Room, Showtime, Booking
from .serializers import MovieSerializer, GenreSerializer, RoomSerializer, ShowtimeSerializer, BookingSerializer
import random

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.prefetch_related('genres').all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['get'], url_path='random')
    def random_movie(self, request):
        movies = list(Movie.objects.all())
        if not movies:
            return Response({'message': 'No hay películas disponibles'}, status=404)
        random_movie = random.choice(movies)
        serializer = self.get_serializer(random_movie)
        return Response(serializer.data)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.annotate(movies_count=Count('movies')).all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.select_related('movie', 'room').all()
    serializer_class = ShowtimeSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['post'], url_path='book')
    def book_tickets(self, request, pk=None):
        showtime = self.get_object()
        seats = request.data.get('seats_count', 1)
        
        if showtime.available_seats < seats:
            return Response({'error': 'No hay suficientes asientos disponibles'}, status=400)
        
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            seats_count=seats,
            status='confirmed'
        )
        
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

@api_view(['GET'])
def pelicula_aleatoria(request):
    from .models import Movie
    peliculas = list(Movie.objects.all())
    if not peliculas:
        return Response({"mensaje": "No hay películas en la base de datos"})
    pelicula = random.choice(peliculas)
    return Response({
        "id": pelicula.id,
        "titulo": pelicula.title,
        "director": pelicula.director,
        "año": pelicula.release_year,
        "duracion": pelicula.duration_minutes,
        "sinopsis": pelicula.synopsis
    })