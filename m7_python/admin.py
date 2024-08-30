from django.contrib import admin
from .models import Usuario, Comuna, Tipo_inmueble, Region, Tipo_user, Profile, Inmuebles

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Tipo_inmueble)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Tipo_user)
admin.site.register(Profile)
admin.site.register(Inmuebles)



