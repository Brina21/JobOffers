from django.shortcuts import render
from apps.users.models import Usuario
from apps.jobs.models import Oferta
from django.db.models import Q

# UD6.2g - Vistas de prueba para templates
# UD6.7 - Vista principal de acceso
def index_view(request):
    """
    Landing page con acceso a los diferentes paneles
    """
    from datetime import datetime
    
    # Estadísticas generales para mostrar en la landing
    total_ofertas = Oferta.objects.filter(estado='Abierta').count()
    total_empresas = Usuario.objects.filter(tipo_usuario='Empresa').count()
    total_trabajadores = Usuario.objects.filter(tipo_usuario='Trabajador').count()
    
    context = {
        'fecha': datetime.now(),
        'total_ofertas': total_ofertas,
        'total_empresas': total_empresas,
        'total_trabajadores': total_trabajadores,
    }
    
    return render(request, 'landing.html', context)

def test_view(request):
    q = request.GET.get('q', '')
    usuarios = []
    
    if q:
        usuarios = Usuario.objects.filter(
            Q(nombre__icontains=q) | 
            Q(apellidos__icontains=q)
        )
    
    return render(request, 'test.html', {'usuarios': usuarios})
