# UD6.7 - URLs de la app jobs (Empresa y Trabajador)
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # ========================================
    # URLs PARA EMPRESA
    # ========================================
    
    # UD6.7a - Dashboard y gestión de ofertas
    path('empresa/dashboard/', views.empresa_dashboard, name='empresa_dashboard'),
    path('empresa/ofertas/', views.empresa_mis_ofertas, name='empresa_mis_ofertas'),
    path('empresa/ofertas/crear/', views.empresa_crear_oferta, name='empresa_crear_oferta'),
    path('empresa/ofertas/<int:oferta_id>/', views.empresa_oferta_detalle, name='empresa_oferta_detalle'),
    path('empresa/ofertas/<int:oferta_id>/editar/', views.empresa_editar_oferta, name='empresa_editar_oferta'),
    
    # UD6.7b - Gestión de candidatos
    path('empresa/inscripcion/<int:inscripcion_id>/gestionar/', views.empresa_gestionar_inscripcion, name='empresa_gestionar_inscripcion'),
    
    # ========================================
    # URLs PARA TRABAJADOR
    # ========================================
    
    # UD6.7c - Dashboard y explorar ofertas
    path('trabajador/dashboard/', views.trabajador_dashboard, name='trabajador_dashboard'),
    path('trabajador/ofertas/', views.trabajador_explorar_ofertas, name='trabajador_explorar_ofertas'),
    path('trabajador/ofertas/<int:oferta_id>/', views.trabajador_oferta_detalle, name='trabajador_oferta_detalle'),
    
    # UD6.7d - Postular y gestionar candidaturas
    path('trabajador/ofertas/<int:oferta_id>/postular/', views.trabajador_postular, name='trabajador_postular'),
    path('trabajador/mis-candidaturas/', views.trabajador_mis_candidaturas, name='trabajador_mis_candidaturas'),
]
