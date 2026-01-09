# UD6.7 - URLs de la app core (Administrador)
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # UD6.7a - Dashboard y vistas principales del administrador
    path('panel-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # UD6.7b - Gestión de usuarios
    path('panel-admin/usuarios/', views.admin_usuarios_lista, name='admin_usuarios_lista'),
    path('panel-admin/usuarios/<int:usuario_id>/', views.admin_usuario_detalle, name='admin_usuario_detalle'),
    path('panel-admin/usuarios/<int:trabajador_id>/toggle-bloqueo/', views.admin_toggle_bloqueo_trabajador, name='admin_toggle_bloqueo'),
    
    # UD6.7c - Gestión de ofertas
    path('panel-admin/ofertas/', views.admin_ofertas_lista, name='admin_ofertas_lista'),
    path('panel-admin/ofertas/<int:oferta_id>/', views.admin_oferta_detalle, name='admin_oferta_detalle'),
    path('panel-admin/ofertas/<int:oferta_id>/cambiar-estado/', views.admin_cambiar_estado_oferta, name='admin_cambiar_estado_oferta'),
    
    # UD6.7d - Moderación
    path('panel-admin/moderacion/', views.admin_moderacion, name='admin_moderacion'),
    
    # UD6.7e - Reportes y estadísticas
    path('panel-admin/reportes/', views.admin_reportes, name='admin_reportes'),
]
