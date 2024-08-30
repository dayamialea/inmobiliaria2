from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import MyLoginView, MyLogoutView, delete_inmueble, update_inmueble, list_inmuebles, contacto


urlpatterns = [
    path('',views.indexView,name='home'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', views.registerView, name='register'),
    path('tipo_registro_usuario/<str:nombre_usuario>/', views.register_tipoView, name='register_tipo'), 
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('update_profile/', views.profile, name='update_profile'),
    path('new_inmueble/', views.new_inmuebleView, name='new_inmueble_url'),
    path('delete_inmueble/<int:pk>/', views.delete_inmueble, name='delete_inmueble'),
    path('update_inmueble/<int:pk>/', views.update_inmueble, name='update_inmueble'),
    path('inmuebles/', list_inmuebles, name='inmuebles'),
    path('contacto/', contacto, name='contacto'),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('password_reset_confirm/', password_reset_confirm, name='password_reset_confirm'),
    path('inmueble/<int:pk>/', views.inmueble_detail, name='inmueble_detail'),
]    



    
    


