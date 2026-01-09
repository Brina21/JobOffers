# UD6.7 - Programación de la aplicación - Vistas Administrador
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Avg
from django.core.paginator import Paginator
from apps.users.models import Usuario
from apps.profiles.models import Administrador, Empresa, Trabajador
from apps.jobs.models import Oferta, Categoria, Inscripcion
from apps.reviews.models import Valoracion
from apps.messaging.models import MensajePrivado
from apps.notifications.models import Notificacion
from datetime import datetime, timedelta


# UD6.7a - Vista Dashboard Global Administrador
def admin_dashboard(request):
    """
    Dashboard principal del administrador con estadísticas globales
    """
    # Estadísticas generales
    total_usuarios = Usuario.objects.count()
    total_trabajadores = Trabajador.objects.count()
    total_empresas = Empresa.objects.count()
    total_ofertas = Oferta.objects.count()
    ofertas_activas = Oferta.objects.filter(estado=Oferta.Estados.ABIERTA).count()
    total_inscripciones = Inscripcion.objects.count()
    
    # Ofertas recientes (últimas 10)
    ofertas_recientes = Oferta.objects.select_related('empresa', 'categoria').order_by('-fecha_publicacion')[:10]
    
    # Usuarios recientes (últimos 10)
    usuarios_recientes = Usuario.objects.order_by('-fecha_registro')[:10]
    
    # Trabajadores bloqueados
    trabajadores_bloqueados = Trabajador.objects.filter(bloqueado=True).count()
    
    # Estadísticas de inscripciones por estado
    inscripciones_pendientes = Inscripcion.objects.filter(estado=Inscripcion.Estados.PENDIENTE).count()
    inscripciones_aceptadas = Inscripcion.objects.filter(estado=Inscripcion.Estados.ACEPTADA).count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_trabajadores': total_trabajadores,
        'total_empresas': total_empresas,
        'total_ofertas': total_ofertas,
        'ofertas_activas': ofertas_activas,
        'total_inscripciones': total_inscripciones,
        'ofertas_recientes': ofertas_recientes,
        'usuarios_recientes': usuarios_recientes,
        'trabajadores_bloqueados': trabajadores_bloqueados,
        'inscripciones_pendientes': inscripciones_pendientes,
        'inscripciones_aceptadas': inscripciones_aceptadas,
    }
    
    return render(request, 'core/admin_dashboard.html', context)


# UD6.7b - Vista Gestión de Usuarios
def admin_usuarios_lista(request):
    """
    Lista todos los usuarios del sistema con filtros
    """
    # Obtener parámetros de búsqueda y filtro
    busqueda = request.GET.get('q', '')
    tipo_usuario = request.GET.get('tipo', '')
    activo = request.GET.get('activo', '')
    
    # Query base
    usuarios = Usuario.objects.all()
    
    # Aplicar filtros
    if busqueda:
        usuarios = usuarios.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellidos__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(dni__icontains=busqueda)
        )
    
    if tipo_usuario:
        usuarios = usuarios.filter(tipo_usuario=tipo_usuario)
    
    if activo:
        usuarios = usuarios.filter(activo=(activo == 'true'))
    
    # Ordenar por fecha de registro descendente
    usuarios = usuarios.order_by('-fecha_registro')
    
    # Paginación
    paginator = Paginator(usuarios, 20)  # 20 usuarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'usuarios': page_obj,
        'busqueda': busqueda,
        'tipo_usuario': tipo_usuario,
        'activo': activo,
        'tipos_usuario': Usuario.Roles.choices,
    }
    
    return render(request, 'core/admin_usuarios_lista.html', context)


# UD6.7c - Vista Detalle de Usuario
def admin_usuario_detalle(request, usuario_id):
    """
    Muestra el detalle completo de un usuario
    """
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Obtener perfil específico según tipo
    perfil_especifico = None
    datos_adicionales = {}
    
    if usuario.tipo_usuario == Usuario.Roles.TRABAJADOR:
        try:
            perfil_especifico = usuario.trabajador
            datos_adicionales['inscripciones'] = Inscripcion.objects.filter(trabajador=perfil_especifico)[:10]
            datos_adicionales['valoraciones'] = Valoracion.objects.filter(trabajador=perfil_especifico)[:10]
        except Trabajador.DoesNotExist:
            pass
    
    elif usuario.tipo_usuario == Usuario.Roles.EMPRESA:
        try:
            perfil_especifico = usuario.empresa
            datos_adicionales['ofertas'] = Oferta.objects.filter(empresa=perfil_especifico)[:10]
            datos_adicionales['valoraciones_dadas'] = Valoracion.objects.filter(empresa=perfil_especifico)[:10]
        except Empresa.DoesNotExist:
            pass
    
    context = {
        'usuario': usuario,
        'perfil_especifico': perfil_especifico,
        'datos_adicionales': datos_adicionales,
    }
    
    return render(request, 'core/admin_usuario_detalle.html', context)


# UD6.7d - Vista Gestión de Ofertas
def admin_ofertas_lista(request):
    """
    Lista todas las ofertas del sistema con filtros
    """
    # Obtener parámetros de búsqueda y filtro
    busqueda = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    categoria_id = request.GET.get('categoria', '')
    urgente = request.GET.get('urgente', '')
    
    # Query base
    ofertas = Oferta.objects.select_related('empresa', 'categoria').all()
    
    # Aplicar filtros
    if busqueda:
        ofertas = ofertas.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(empresa__nombre_empresa__icontains=busqueda)
        )
    
    if estado:
        ofertas = ofertas.filter(estado=estado)
    
    if categoria_id:
        ofertas = ofertas.filter(categoria_id=categoria_id)
    
    if urgente:
        ofertas = ofertas.filter(urgente=(urgente == 'true'))
    
    # Ordenar por fecha de publicación descendente
    ofertas = ofertas.order_by('-fecha_publicacion')
    
    # Paginación
    paginator = Paginator(ofertas, 15)  # 15 ofertas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener categorías para el filtro
    categorias = Categoria.objects.all()
    
    context = {
        'page_obj': page_obj,
        'ofertas': page_obj,
        'busqueda': busqueda,
        'estado_filtro': estado,
        'categoria_id': categoria_id,
        'urgente': urgente,
        'estados': Oferta.Estados.choices,
        'categorias': categorias,
    }
    
    return render(request, 'core/admin_ofertas_lista.html', context)


# UD6.7e - Vista Detalle de Oferta (Admin)
def admin_oferta_detalle(request, oferta_id):
    """
    Muestra el detalle completo de una oferta con inscripciones
    """
    oferta = get_object_or_404(Oferta.objects.select_related('empresa', 'categoria'), id=oferta_id)
    inscripciones = Inscripcion.objects.filter(oferta=oferta).select_related('trabajador__id_usuario')
    
    # Estadísticas de la oferta
    total_inscripciones = inscripciones.count()
    inscripciones_pendientes = inscripciones.filter(estado=Inscripcion.Estados.PENDIENTE).count()
    inscripciones_aceptadas = inscripciones.filter(estado=Inscripcion.Estados.ACEPTADA).count()
    inscripciones_rechazadas = inscripciones.filter(estado=Inscripcion.Estados.RECHAZADA).count()
    
    context = {
        'oferta': oferta,
        'inscripciones': inscripciones,
        'total_inscripciones': total_inscripciones,
        'inscripciones_pendientes': inscripciones_pendientes,
        'inscripciones_aceptadas': inscripciones_aceptadas,
        'inscripciones_rechazadas': inscripciones_rechazadas,
    }
    
    return render(request, 'core/admin_oferta_detalle.html', context)


# UD6.7f - Vista Moderación (Trabajadores Bloqueados)
def admin_moderacion(request):
    """
    Panel de moderación para gestionar trabajadores bloqueados y reportes
    """
    # Trabajadores bloqueados
    trabajadores_bloqueados = Trabajador.objects.filter(bloqueado=True).select_related('id_usuario')
    
    # Trabajadores con más cancelaciones
    trabajadores_cancelaciones = Trabajador.objects.filter(
        cancelaciones_totales__gt=0
    ).select_related('id_usuario').order_by('-cancelaciones_totales')[:20]
    
    context = {
        'trabajadores_bloqueados': trabajadores_bloqueados,
        'trabajadores_cancelaciones': trabajadores_cancelaciones,
    }
    
    return render(request, 'core/admin_moderacion.html', context)


# UD6.7g - Vista Reportes y Estadísticas
def admin_reportes(request):
    """
    Página de reportes y estadísticas avanzadas
    """
    # Estadísticas por categoría
    ofertas_por_categoria = Categoria.objects.annotate(
        total_ofertas=Count('ofertas')
    ).order_by('-total_ofertas')
    
    # Empresas más activas
    empresas_activas = Empresa.objects.annotate(
        total_ofertas=Count('ofertas')
    ).select_related('id_usuario').order_by('-total_ofertas')[:10]
    
    # Trabajadores con mejor valoración
    trabajadores_top = Trabajador.objects.filter(
        valoracion_media__gt=0
    ).select_related('id_usuario').order_by('-valoracion_media')[:10]
    
    # Ofertas por estado
    ofertas_por_estado = Oferta.objects.values('estado').annotate(
        total=Count('id')
    )
    
    # Inscripciones por estado
    inscripciones_por_estado = Inscripcion.objects.values('estado').annotate(
        total=Count('id')
    )
    
    # Usuarios registrados últimos 30 días
    fecha_limite = datetime.now() - timedelta(days=30)
    usuarios_mes = Usuario.objects.filter(fecha_registro__gte=fecha_limite).count()
    
    context = {
        'ofertas_por_categoria': ofertas_por_categoria,
        'empresas_activas': empresas_activas,
        'trabajadores_top': trabajadores_top,
        'ofertas_por_estado': ofertas_por_estado,
        'inscripciones_por_estado': inscripciones_por_estado,
        'usuarios_mes': usuarios_mes,
    }
    
    return render(request, 'core/admin_reportes.html', context)


# UD6.7h - Vista para Bloquear/Desbloquear Trabajador
def admin_toggle_bloqueo_trabajador(request, trabajador_id):
    """
    Bloquea o desbloquea un trabajador
    """
    trabajador = get_object_or_404(Trabajador, id_usuario_id=trabajador_id)
    
    if request.method == 'POST':
        trabajador.bloqueado = not trabajador.bloqueado
        
        if trabajador.bloqueado:
            trabajador.motivo_bloqueo = request.POST.get('motivo', 'Bloqueado por administrador')
            trabajador.fecha_fin_bloqueo = None  # Bloqueo indefinido
            messages.success(request, f'Trabajador {trabajador.id_usuario.nombre} bloqueado exitosamente.')
        else:
            trabajador.motivo_bloqueo = None
            trabajador.fecha_fin_bloqueo = None
            messages.success(request, f'Trabajador {trabajador.id_usuario.nombre} desbloqueado exitosamente.')
        
        trabajador.save()
        
        return redirect('admin_moderacion')
    
    return redirect('admin_usuario_detalle', usuario_id=trabajador_id)


# UD6.7i - Vista para Cambiar Estado de Oferta
def admin_cambiar_estado_oferta(request, oferta_id):
    """
    Permite al administrador cambiar el estado de una oferta
    """
    oferta = get_object_or_404(Oferta, id=oferta_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in dict(Oferta.Estados.choices):
            oferta.estado = nuevo_estado
            oferta.save()
            messages.success(request, f'Estado de la oferta actualizado a {nuevo_estado}.')
        else:
            messages.error(request, 'Estado no válido.')
        
        return redirect('admin_oferta_detalle', oferta_id=oferta_id)
    
    return redirect('admin_oferta_detalle', oferta_id=oferta_id)
