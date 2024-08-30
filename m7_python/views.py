from django.shortcuts import render, redirect, get_object_or_404, redirect
from m7_python.models import *
from m7_python.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.db import IntegrityError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .forms import InmuebleForm
from .models import Inmuebles  # Importación local para evitar ciclo





def registerView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Verificar si el nombre de usuario ya existe
            if User.objects.filter(username=username).exists():
                return render(request, 'registration/register.html', {
                    'form': form,
                    'error_message': 'Este nombre de usuario ya está en uso.'
                })

            try:
                # Guardar el usuario si no hay duplicados
                user = form.save()
                # Usar reverse para generar la URL correctamente
                return redirect(reverse('register_tipo_url', args=[user.username]))
            except IntegrityError:
                # Capturar cualquier error de integridad en la base de datos
                return render(request, 'registration/register.html', {
                    'form': form,
                    'error_message': 'Hubo un problema al registrar el usuario. Intenta nuevamente.'
                })
        else:
            return render(request, 'registration/register.html', {'form': form})
            
    else:
        form = UserForm()
        return render(request, 'registration/register.html', {'form': form})

def register_tipoView(request, username):
    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            user = User.objects.get(username=username)
            
            
            id_tipo_user = Tipo_user.objects.get(pk=tipo)

            datos = Profile(user=user, id_tipo_user=id_tipo_user, rut=rut, direccion=direccion, telefono=telefono)
            datos.save()

            return HttpResponseRedirect('/login/')
    else:
        form = TipoForm()

    return render(request, 'registration/register_tipo.html', {'form': form})

    

@login_required
def dashboardView(request):
    return render(request, 'dashboard.html', {})

def indexView(request):
    return render(request, 'index.html', {})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        u_form = UserUpdateForm(instance=request.user.profile)
        
    context = {'u_form': u_form}
    return render(request, 'registration/update_profile.html', context)

class MyLoginView(DjangoLoginView):
    registration = 'registration_login.html'
    next_page = '/dashboard/'

class MyLogoutView(DjangoLogoutView):
    next_page = '/'
    
@login_required
def new_inmuebleView(request):
    if request.method == 'POST':
        u_form = InmuebleForm(request.POST)
        if u_form.is_valid():
            u_form = InmuebleForm(request.POST)
            print(u_form)
            id_tipo_inmueble = u_form.cleaned_data['id_tipo_inmueble']
            id_comuna = u_form.cleaned_data['id_comuna']
            id_region = u_form.cleaned_data['id_region']
            nombre_inmueble = u_form.cleaned_data['nombre_inmueble']
            descripcion = u_form.cleaned_data['descripcion']
            m2_construido = u_form.cleaned_data['m2_construido']
            numero_banos = u_form.cleaned_data['numero_banos']
            numero_hab = u_form.cleaned_data['numero_hab']
            direccion = u_form.cleaned_data['direccion']
            m2_terreno = u_form.cleaned_data['m2_terreno']
            numero_est = u_form.cleaned_data['numero_est']
            print(u_form.cleaned_data)
            tipo_inmueble = Tipo_inmueble.objects.filter(id=int(id_tipo_inmueble))[0]
            comuna = Comuna.objects.filter(id=int(id_comuna))[0]
            reg = Region.objects.filter(id=int(id_region))[0]
            current_user = request.user
            
            user = User.objects.filter(id=current_user.id)
            inm = Inmuebles(id_tipo_inmueble=tipo_inmueble,
                            id_comuna=comuna,
                            id_region=reg,
                            nombre_inmueble=nombre_inmueble,
                            descripcion=descripcion,
                            m2_construido=m2_construido,
                            numero_banos=numero_banos,
                            numero_hab=numero_hab,
                            direccion=direccion,
                            m2_terreno=m2_terreno,
                            numero_est=numero_est)

            
            print(user)
            inm.id_user_id = current_user.id
            inm.save()
            return HttpResponseRedirect('/dashboard/')
    else:
       u_form = InmuebleForm()

    context = {'u_form': u_form}
    return render(request, 'new_inmueble.html', context)

def update_inmueble(request, pk):
    inmueble = get_object_or_404(Inmuebles, pk=pk)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)  
        if form.is_valid():
            form.save()
            return redirect('inmuebles')  # Redirigir a la lista de inmuebles
    else:
        form = InmuebleForm(instance=inmueble)  
    return render(request, 'update_inmueble.html', {'form': form})

def delete_inmueble(request, id):
    inmueble = get_object_or_404(Inmuebles, id=id)  # Usa 'Inmuebles' en lugar de 'Inmueble'
    if request.method == 'POST':
        inmueble.delete()
        return redirect('inmuebles')  # Redirigir a la lista de inmuebles
    return render(request, 'delete_inmueble.html', {'inmueble': inmueble})

def list_inmuebles(request):
       # Obtén los filtros desde la solicitud GET
    comuna_id = request.GET.get('comuna')
    region_id = request.GET.get('region')
    com = Comuna.objects.all()
    reg = Region.objects.all()
    
    # Filtra los inmuebles según los parámetros
    inmuebles = Inmuebles.objects.all()
    
    if comuna_id:
        inmuebles = inmuebles.filter(id_comuna=comuna_id)
    if region_id:
        inmuebles = inmuebles.filter(id_region=region_id)
    
    return render(request, 'list_inmuebles.html', {'inmuebles': inmuebles,'com': com,'reg': reg})

def contacto(request):
    if request.method == 'POST':
        
        form = ContactFormModelForm(request.POST)
        
        if form.is_valid():
            
            contact_form = ContactForm.objects.create(**form.cleaned_data)
            
            return HttpResponseRedirect('/exito')
        
        
    else:
        form = ContactFormModelForm()
        
    return render(request, 'contactus.html', {'form': form})

def inmueble_detail(request, pk):
    # Obtén el inmueble con la clave primaria 'pk', o muestra una página 404 si no se encuentra.
    inmueble = get_object_or_404(Inmuebles, pk=pk)
    # Puedes agregar una impresión para depuración
    print(f"Inmueble pk: {inmueble.pk}")  # Esto imprimirá el pk del inmueble en la consola del servidor
    # Renderiza la plantilla con el detalle del inmueble.
    return render(request, 'inmueble_detail.html', {'inmueble': Inmuebles})
