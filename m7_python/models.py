import uuid
from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    id_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

class Tipo_inmueble(models.Model):
    tipo_inmueble = models.TextField()
    def __str__(self):
       return self.tipo_inmueble

class Comuna(models.Model):
    comuna = models.TextField()
    def __str__(self):
       return self.comuna
    

class Region(models.Model):
    Region = models.TextField()
    def __str__(self):
       return self.Region

class Tipo_user(models.Model):
    tipo_user = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_tipo_user = models.ForeignKey(Tipo_user, on_delete=models.CASCADE, default=1)  # Proporcionar un valor predeterminado
    rut = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)


class Inmuebles(models.Model):
    id_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    id_tipo_inmueble = models.ForeignKey('m7_python.Tipo_inmueble', on_delete=models.CASCADE, null=True)
    id_comuna = models.ForeignKey('m7_python.Comuna', on_delete=models.CASCADE, null=True)
    id_region = models.ForeignKey('m7_python.Region', on_delete=models.CASCADE, null=True)
    nombre_inmueble = models.TextField()
    descripcion = models.CharField(max_length=200)
    m2_construido = models.FloatField()
    numero_banos = models.IntegerField(default=0)
    numero_hab = models.IntegerField(default=0)
    direccion = models.CharField(max_length=200)
    # agregado.datos faltantes
    m2_terreno = models.FloatField(default =0)
    numero_est = models.IntegerField(default =0)
    imagen = models.ImageField(upload_to='inmuebles/', null=True, blank=True)
    
class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()
