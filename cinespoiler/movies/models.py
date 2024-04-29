from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ========== MODELOS EXISTENTES ==========
class Genre(models.Model):
    name = models.CharField('Nombre', max_length=100, unique=True)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)

    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'
        ordering = ['id']

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField('Título', max_length=200)
    release_year = models.PositiveIntegerField('Año de estreno')
    director = models.CharField('Director', max_length=200)
    duration_minutes = models.PositiveIntegerField('Duración (minutos)')
    synopsis = models.TextField('Sinopsis', blank=True)
    poster_url = models.URLField('URL del póster', max_length=500, blank=True, null=True)
    trailer_url = models.URLField('URL del trailer', max_length=500, blank=True, null=True)
    rating = models.DecimalField('Puntuación', max_digits=3, decimal_places=1, default=0,
                                 validators=[MinValueValidator(0), MaxValueValidator(10)])
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name='Géneros', blank=True)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)

    class Meta:
        verbose_name = 'Película'
        verbose_name_plural = 'Películas'
        ordering = ['id']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

# ========== NUEVOS MODELOS ==========
class Room(models.Model):
    """Sala de cine"""
    name = models.CharField('Nombre de sala', max_length=50)
    capacity = models.PositiveIntegerField('Capacidad total')
    rows = models.PositiveIntegerField('Número de filas', default=5)
    columns = models.PositiveIntegerField('Número de columnas', default=10)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} - {self.capacity} asientos"

class Showtime(models.Model):
    """Horario de función"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField('Fecha')
    show_time = models.TimeField('Hora')
    price = models.DecimalField('Precio', max_digits=6, decimal_places=2)
    
    class Meta:
        verbose_name = 'Función'
        verbose_name_plural = 'Funciones'
        ordering = ['show_date', 'show_time']
        unique_together = ['room', 'show_date', 'show_time']

    @property
    def available_seats(self):
        confirmed_bookings = self.bookings.filter(status='confirmed').count()
        return self.room.capacity - confirmed_bookings

    def __str__(self):
        return f"{self.movie.title} - {self.room.name} - {self.show_date} {self.show_time}"

class Booking(models.Model):
    """Reserva de entradas"""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    seats_count = models.PositiveIntegerField('Número de asientos')
    total_price = models.DecimalField('Precio total', max_digits=8, decimal_places=2)
    status = models.CharField('Estado', max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.seats_count * self.showtime.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.showtime.movie.title} - {self.seats_count} asientos"