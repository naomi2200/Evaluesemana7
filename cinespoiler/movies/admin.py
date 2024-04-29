from django.contrib import admin
from .models import Movie, Genre, Room, Showtime, Booking

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    ordering = ['id']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'release_year', 'director', 'rating']
    list_filter = ['release_year', 'genres']
    search_fields = ['title', 'director']
    filter_horizontal = ['genres']
    ordering = ['id']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'capacity']
    ordering = ['id']

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'room', 'show_date', 'show_time', 'price']
    list_filter = ['show_date', 'room']
    ordering = ['id']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'showtime', 'seats_count', 'total_price', 'status']
    list_filter = ['status', 'created_at']
    ordering = ['-created_at']