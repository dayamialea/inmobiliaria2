from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Comuna, Region, Inmuebles, ContactForm
from django.forms import ModelForm
 

class UserForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario')  # Agregamos el campo de username
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.EmailField(label='Correo electrónico')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # Validación personalizada para el campo username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso. Elige otro.')
        return username

        
class TipoForm(forms.Form):
    tipos = ((1,'Arrendatario'),(2,'Arrendador'),)
    tipo = forms.ChoiceField(choices=tipos)
    rut = forms.CharField(label='rut', max_length=100)
    direccion = forms.CharField(label='direccion', max_length=100)
    telefono = forms.CharField(label='telefono', max_length=100)
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
        
class InmuebleForm(forms.Form):
    tipos = ((1, "Casa"), (2, "Departamento"), (3, "Parcela"), (4, "Estacionamiento"), (5, "Otro"))
    id_tipo_inmueble = forms.ChoiceField(choices=tipos)
    comunas = [(x.id, x.comuna) for x in list(Comuna.objects.filter())]

    def nombre_comuna(e):
        return e[1]
    
    comunas.sort(key=nombre_comuna)

    id_comuna = forms.ChoiceField(choices=comunas)
    regiones = [(x.id, x.Region) for x in list(Region.objects.filter())]
    id_region = forms.ChoiceField(choices=regiones)
    nombre_inmueble = forms.CharField(label='Nombre Inmueble', max_length=100)
    descripcion = forms.CharField(label='Descripcion del Inmueble', max_length=100)
    m2_construido = forms.CharField(label='M2 construidos', max_length=100)
    numero_banos = forms.CharField(label='Numero de Baños', max_length=100)
    numero_hab = forms.CharField(label='Numero de habitaciones', max_length=100)
    direccion = forms.CharField(label='Direccion', max_length=100)
    m2_terreno = forms.CharField(label='M2 de terreno', max_length=100)
    numero_est = forms.CharField(label='Núm. de Estacionamientos', max_length=100)
    imagen = forms.ImageField(label='Imagen', required=False)
    
class InmuebleModelForm(forms.ModelForm):
    class Meta:
        model = Inmuebles
        fields = ['id_tipo_inmueble','id_comuna','id_region','nombre_inmueble','descripcion','m2_construido', 'numero_banos','numero_hab','direccion','m2_terreno','numero_est', 'imagen']    
    
class ContactFormform(forms.Form):
    
    customer_email = forms.EmailField(label='Correo')
    customer_name = forms.CharField(max_length=64, label='Nombre')
    message = forms.CharField(label='Mensaje')
    
    
class ContactFormModelForm(ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message']

