from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Movie, Genre, Room, Showtime, Booking
from django.db.models import Count, Sum, Avg
from datetime import datetime

@api_view(['GET'])
@permission_classes([AllowAny])
def stats_advanced(request):
    genres_stats = Genre.objects.annotate(
        movie_count=Count('movies')
    ).values('name', 'movie_count')
    
    today = datetime.now().date()
    upcoming = Showtime.objects.filter(show_date__gte=today).select_related('movie', 'room')[:10]
    
    upcoming_data = [{
        'pelicula': s.movie.title,
        'sala': s.room.name,
        'fecha': str(s.show_date),
        'hora': str(s.show_time),
        'precio': float(s.price),
        'asientos_disponibles': s.available_seats
    } for s in upcoming]
    
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    
    top_movie = Movie.objects.order_by('-rating').first()
    
    return Response({
        'resumen_general': {
            'total_peliculas': Movie.objects.count(),
            'total_generos': Genre.objects.count(),
            'total_salas': Room.objects.count(),
            'total_funciones': Showtime.objects.count(),
            'total_reservas': total_bookings,
            'reservas_confirmadas': confirmed_bookings,
        },
        'peliculas_por_genero': list(genres_stats),
        'proximas_funciones': upcoming_data,
        'pelicula_mejor_valorada': {
            'titulo': top_movie.title if top_movie else None,
            'rating': float(top_movie.rating) if top_movie else None
        } if top_movie else None,
        'sistema': {
            'nombre': 'Cinespoiler',
            'version': '2.0',
            'status': 'operativo'
        }
    })