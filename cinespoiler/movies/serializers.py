from rest_framework import serializers
from .models import Movie, Genre, Room, Showtime, Booking
from django.contrib.auth.models import User

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'created_at', 'updated_at']

class MovieSerializer(serializers.ModelSerializer):
    genres_detail = GenreSerializer(source='genres', many=True, read_only=True)
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), write_only=True, required=False
    )
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_year', 'director', 'duration_minutes',
                  'synopsis', 'poster_url', 'trailer_url', 'rating',
                  'genres', 'genres_detail', 'created_at', 'updated_at']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ShowtimeSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'movie_title', 'room', 'room_name', 
                  'show_date', 'show_time', 'price', 'available_seats']

class BookingSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='showtime.movie.title', read_only=True)
    show_date = serializers.DateField(source='showtime.show_date', read_only=True)
    show_time = serializers.TimeField(source='showtime.show_time', read_only=True)
    room_name = serializers.CharField(source='showtime.room.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'user_name', 'showtime', 'movie_title', 
                  'room_name', 'show_date', 'show_time', 'seats_count', 
                  'total_price', 'status', 'created_at']
        read_only_fields = ['user', 'total_price']