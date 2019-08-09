from django.db import models
from django.conf import settings

#Paises aceptados
COUNTRY_CHOICES = [
    ('ES', 'Spain'),
]

# Modelo de los directores de castings
class CastingManager(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True,
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.last_name

# Modelo del personaje a interpretar
class Character(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Modelo de los actores
class Contestan(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date = models.DateField()
    phone = models.PositiveIntegerField()
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=2)
    email = models.EmailField()
    character = models.ForeignKey(Character, on_delete=models.SET_NULL ,null=True,blank=True)

    def __str__(self):
        return self.last_name
    

