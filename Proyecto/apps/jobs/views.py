# UD6.7 - Programación de la aplicación - Vistas de Empresa y Trabajador
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from datetime import datetime
from apps.users.models import Usuario
from apps.profiles.models import Trabajador, Empresa
from .models import Oferta, Categoria, Inscripcion


# ========================================
# VISTAS PARA EMPRESA
# ========================================

# UD6.7a - Dashboard Empresa
def empresa_dashboard(request):
    """
    Panel de control principal para empresas
    """
    # Por ahora simulamos que tenemos la empresa del request
    # En producción se obtendría de request.user.empresa
    empresa = Empresa.objects.first()  # TEMPORAL: cambiar por request.user.empresa
    
    if not empresa:
        messages.error(request, "No se encontró el perfil de empresa")
        return redirect('index')
    
    # Estadísticas de la empresa
    total_ofertas = Oferta.objects.filter(empresa=empresa).count()
    ofertas_activas = Oferta.objects.filter(empresa=empresa, estado=Oferta.Estados.ABIERTA).count()
    
    # Total de candidaturas recibidas
    total_candidaturas = Inscripcion.objects.filter(oferta__empresa=empresa).count()
    candidaturas_pendientes = Inscripcion.objects.filter(
        oferta__empresa=empresa, 
        estado=Inscripcion.Estados.PENDIENTE
    ).count()
    
    # Contrataciones realizadas (aceptadas)
    contrataciones = Inscripcion.objects.filter(
        oferta__empresa=empresa,
        estado=Inscripcion.Estados.ACEPTADA
    ).count()
    
    # Ofertas activas recientes
    ofertas_activas_list = Oferta.objects.filter(
        empresa=empresa,
        estado=Oferta.Estados.ABIERTA
    ).order_by('-fecha_publicacion')[:6]
    
    # Candidaturas recientes
    candidaturas_recientes = Inscripcion.objects.filter(
        oferta__empresa=empresa
    ).select_related('trabajador__id_usuario', 'oferta').order_by('-fecha_inscripcion')[:10]
    
    context = {
        'empresa': empresa,
        'total_ofertas': total_ofertas,
        'ofertas_activas': ofertas_activas,
        'total_candidaturas': total_candidaturas,
        'candidaturas_pendientes': candidaturas_pendientes,
        'contrataciones': contrataciones,
        'ofertas_activas_list': ofertas_activas_list,
        'candidaturas_recientes': candidaturas_recientes,
    }
    
    return render(request, 'jobs/empresa_dashboard.html', context)


# UD6.7b - Lista de Ofertas de la Empresa
def empresa_mis_ofertas(request):
    """
    Lista todas las ofertas publicadas por la empresa
    """
    empresa = Empresa.objects.first()  # TEMPORAL
    
    if not empresa:
        messages.error(request, "No se encontró el perfil de empresa")
        return redirect('index')
    
    # Filtros
    estado_filtro = request.GET.get('estado', '')
    busqueda = request.GET.get('q', '')
    
    # Query base
    ofertas = Oferta.objects.filter(empresa=empresa).select_related('categoria')
    
    # Aplicar filtros
    if estado_filtro:
        ofertas = ofertas.filter(estado=estado_filtro)
    
    if busqueda:
        ofertas = ofertas.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    # Ordenar
    ofertas = ofertas.order_by('-fecha_publicacion')
    
    # Paginación
    paginator = Paginator(ofertas, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'empresa': empresa,
        'page_obj': page_obj,
        'ofertas': page_obj,
        'estado_filtro': estado_filtro,
        'busqueda': busqueda,
        'estados': Oferta.Estados.choices,
    }
    
    return render(request, 'jobs/empresa_mis_ofertas.html', context)


# UD6.7c - Crear Nueva Oferta
def empresa_crear_oferta(request):
    """
    Formulario para crear una nueva oferta de empleo
    """
    empresa = Empresa.objects.first()  # TEMPORAL
    
    if not empresa:
        messages.error(request, "No se encontró el perfil de empresa")
        return redirect('index')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria')
        precio_hora = request.POST.get('precio_hora')
        total = request.POST.get('total')
        tipo_contrato = request.POST.get('tipo_contrato')
        jornada = request.POST.get('jornada')
        plazas_totales = request.POST.get('plazas_totales')
        horario = request.POST.get('horario')
        urgente = request.POST.get('urgente') == 'on'
        fecha_evento = request.POST.get('fecha_evento')
        fecha_cierre = request.POST.get('fecha_cierre')
        
        # Validaciones básicas
        if not titulo or not descripcion or not categoria_id:
            messages.error(request, "Por favor completa todos los campos obligatorios")
            return redirect('jobs:empresa_crear_oferta')
        
        # Crear la oferta
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            plazas_totales_int = int(plazas_totales) if plazas_totales else 1
            
            oferta = Oferta.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                categoria=categoria,
                empresa=empresa,
                precio_hora=precio_hora if precio_hora else None,
                total=total if total else None,
                tipo_contrato=tipo_contrato if tipo_contrato else None,
                jornada=jornada if jornada else None,
                plazas_totales=plazas_totales_int,
                plazas_disponibles=plazas_totales_int,
                horario=horario if horario else None,
                urgente=urgente,
                fecha_evento=fecha_evento if fecha_evento else None,
                fecha_cierre=fecha_cierre if fecha_cierre else None,
                estado=Oferta.Estados.ABIERTA
            )
            
            messages.success(request, f"Oferta '{titulo}' creada exitosamente")
            return redirect('jobs:empresa_oferta_detalle', oferta_id=oferta.id)
            
        except Exception as e:
            messages.error(request, f"Error al crear la oferta: {str(e)}")
            return redirect('jobs:empresa_crear_oferta')
    
    # GET: Mostrar formulario
    categorias = Categoria.objects.all().order_by('nombre')
    
    context = {
        'empresa': empresa,
        'categorias': categorias,
    }
    
    return render(request, 'jobs/empresa_crear_oferta.html', context)


# UD6.7d - Detalle de Oferta (Empresa)
def empresa_oferta_detalle(request, oferta_id):
    """
    Muestra el detalle de una oferta con sus candidatos
    """
    empresa = Empresa.objects.first()  # TEMPORAL
    
    oferta = get_object_or_404(
        Oferta.objects.select_related('categoria'),
        id=oferta_id,
        empresa=empresa
    )
    
    # Obtener candidatos
    inscripciones = Inscripcion.objects.filter(
        oferta=oferta
    ).select_related('trabajador__id_usuario').order_by('-fecha_inscripcion')
    
    # Estadísticas de inscripciones
    total_inscripciones = inscripciones.count()
    pendientes = inscripciones.filter(estado=Inscripcion.Estados.PENDIENTE).count()
    aceptadas = inscripciones.filter(estado=Inscripcion.Estados.ACEPTADA).count()
    rechazadas = inscripciones.filter(estado=Inscripcion.Estados.RECHAZADA).count()
    
    context = {
        'empresa': empresa,
        'oferta': oferta,
        'inscripciones': inscripciones,
        'total_inscripciones': total_inscripciones,
        'pendientes': pendientes,
        'aceptadas': aceptadas,
        'rechazadas': rechazadas,
    }
    
    return render(request, 'jobs/empresa_oferta_detalle.html', context)


# UD6.7e - Editar Oferta
def empresa_editar_oferta(request, oferta_id):
    """
    Formulario para editar una oferta existente
    """
    empresa = Empresa.objects.first()  # TEMPORAL
    
    oferta = get_object_or_404(Oferta, id=oferta_id, empresa=empresa)
    
    if request.method == 'POST':
        # Actualizar datos
        oferta.titulo = request.POST.get('titulo')
        oferta.descripcion = request.POST.get('descripcion')
        
        categoria_id = request.POST.get('categoria')
        if categoria_id:
            oferta.categoria = Categoria.objects.get(id=categoria_id)
        
        oferta.precio_hora = request.POST.get('precio_hora') or None
        oferta.total = request.POST.get('total') or None
        oferta.tipo_contrato = request.POST.get('tipo_contrato') or None
        oferta.jornada = request.POST.get('jornada') or None
        
        plazas = request.POST.get('plazas_totales')
        if plazas:
            oferta.plazas_totales = int(plazas)
            # Ajustar disponibles si es necesario
            if oferta.plazas_disponibles > oferta.plazas_totales:
                oferta.plazas_disponibles = oferta.plazas_totales
        
        oferta.horario = request.POST.get('horario') or None
        oferta.urgente = request.POST.get('urgente') == 'on'
        oferta.fecha_evento = request.POST.get('fecha_evento') or None
        oferta.fecha_cierre = request.POST.get('fecha_cierre') or None
        oferta.estado = request.POST.get('estado', Oferta.Estados.ABIERTA)
        
        oferta.save()
        
        messages.success(request, f"Oferta '{oferta.titulo}' actualizada exitosamente")
        return redirect('jobs:empresa_oferta_detalle', oferta_id=oferta.id)
    
    # GET: Mostrar formulario con datos actuales
    categorias = Categoria.objects.all().order_by('nombre')
    
    context = {
        'empresa': empresa,
        'oferta': oferta,
        'categorias': categorias,
        'estados': Oferta.Estados.choices,
    }
    
    return render(request, 'jobs/empresa_editar_oferta.html', context)


# UD6.7f - Gestionar Inscripción (Aceptar/Rechazar)
def empresa_gestionar_inscripcion(request, inscripcion_id):
    """
    Permite a la empresa aceptar o rechazar una candidatura
    """
    empresa = Empresa.objects.first()  # TEMPORAL
    
    inscripcion = get_object_or_404(
        Inscripcion.objects.select_related('oferta', 'trabajador__id_usuario'),
        id=inscripcion_id,
        oferta__empresa=empresa
    )
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'aceptar':
            inscripcion.estado = Inscripcion.Estados.ACEPTADA
            # Reducir plazas disponibles
            if inscripcion.oferta.plazas_disponibles > 0:
                inscripcion.oferta.plazas_disponibles -= 1
                inscripcion.oferta.save()
            
            inscripcion.save()
            messages.success(request, f"Candidatura de {inscripcion.trabajador.id_usuario.nombre} aceptada")
            
        elif accion == 'rechazar':
            inscripcion.estado = Inscripcion.Estados.RECHAZADA
            inscripcion.save()
            messages.success(request, f"Candidatura de {inscripcion.trabajador.id_usuario.nombre} rechazada")
        
        return redirect('jobs:empresa_oferta_detalle', oferta_id=inscripcion.oferta.id)
    
    return redirect('jobs:empresa_oferta_detalle', oferta_id=inscripcion.oferta.id)


# ========================================
# VISTAS PARA TRABAJADOR
# ========================================

# UD6.7g - Dashboard Trabajador
def trabajador_dashboard(request):
    """
    Panel de control principal para trabajadores
    """
    # TEMPORAL: obtener primer trabajador
    trabajador = Trabajador.objects.first()
    
    if not trabajador:
        messages.error(request, "No se encontró el perfil de trabajador")
        return redirect('index')
    
    # Estadísticas del trabajador
    total_candidaturas = Inscripcion.objects.filter(trabajador=trabajador).count()
    en_proceso = Inscripcion.objects.filter(
        trabajador=trabajador,
        estado=Inscripcion.Estados.PENDIENTE
    ).count()
    aceptadas = Inscripcion.objects.filter(
        trabajador=trabajador,
        estado=Inscripcion.Estados.ACEPTADA
    ).count()
    
    # Candidaturas activas
    candidaturas_activas = Inscripcion.objects.filter(
        trabajador=trabajador,
        estado__in=[Inscripcion.Estados.PENDIENTE, Inscripcion.Estados.ACEPTADA]
    ).select_related('oferta__empresa', 'oferta__categoria').order_by('-fecha_inscripcion')[:10]
    
    # Ofertas recomendadas (últimas 6)
    ofertas_recomendadas = Oferta.objects.filter(
        estado=Oferta.Estados.ABIERTA,
        plazas_disponibles__gt=0
    ).select_related('empresa', 'categoria').order_by('-fecha_publicacion')[:6]
    
    context = {
        'trabajador': trabajador,
        'total_candidaturas': total_candidaturas,
        'en_proceso': en_proceso,
        'aceptadas': aceptadas,
        'candidaturas_activas': candidaturas_activas,
        'ofertas_recomendadas': ofertas_recomendadas,
    }
    
    return render(request, 'jobs/trabajador_dashboard.html', context)


# UD6.7h - Explorar Ofertas (Trabajador)
def trabajador_explorar_ofertas(request):
    """
    Lista de ofertas disponibles para que el trabajador explore y postule
    """
    trabajador = Trabajador.objects.first()  # TEMPORAL
    
    if not trabajador:
        messages.error(request, "No se encontró el perfil de trabajador")
        return redirect('index')
    
    # Filtros
    categoria_filtro = request.GET.get('categoria', '')
    ciudad_filtro = request.GET.get('ciudad', '')
    urgente_filtro = request.GET.get('urgente', '')
    busqueda = request.GET.get('q', '')
    
    # Query base - solo ofertas abiertas con plazas
    ofertas = Oferta.objects.filter(
        estado=Oferta.Estados.ABIERTA,
        plazas_disponibles__gt=0
    ).select_related('empresa', 'categoria')
    
    # Aplicar filtros
    if categoria_filtro:
        ofertas = ofertas.filter(categoria_id=categoria_filtro)
    
    if ciudad_filtro:
        ofertas = ofertas.filter(empresa__ciudad__icontains=ciudad_filtro)
    
    if urgente_filtro == 'true':
        ofertas = ofertas.filter(urgente=True)
    
    if busqueda:
        ofertas = ofertas.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(empresa__nombre_empresa__icontains=busqueda)
        )
    
    # Ordenar
    ofertas = ofertas.order_by('-urgente', '-fecha_publicacion')
    
    # Obtener inscripciones del trabajador para marcar ofertas ya postuladas
    inscripciones_ids = Inscripcion.objects.filter(
        trabajador=trabajador
    ).values_list('oferta_id', flat=True)
    
    # Paginación
    paginator = Paginator(ofertas, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener categorías para filtro
    categorias = Categoria.objects.all().order_by('nombre')
    
    context = {
        'trabajador': trabajador,
        'page_obj': page_obj,
        'ofertas': page_obj,
        'inscripciones_ids': list(inscripciones_ids),
        'categorias': categorias,
        'categoria_filtro': categoria_filtro,
        'ciudad_filtro': ciudad_filtro,
        'urgente_filtro': urgente_filtro,
        'busqueda': busqueda,
    }
    
    return render(request, 'jobs/trabajador_explorar_ofertas.html', context)


# UD6.7i - Detalle de Oferta (Trabajador)
def trabajador_oferta_detalle(request, oferta_id):
    """
    Muestra el detalle completo de una oferta para el trabajador
    """
    trabajador = Trabajador.objects.first()  # TEMPORAL
    
    oferta = get_object_or_404(
        Oferta.objects.select_related('empresa', 'categoria'),
        id=oferta_id
    )
    
    # Verificar si ya postuló
    ya_postulado = Inscripcion.objects.filter(
        trabajador=trabajador,
        oferta=oferta
    ).first()
    
    context = {
        'trabajador': trabajador,
        'oferta': oferta,
        'ya_postulado': ya_postulado,
    }
    
    return render(request, 'jobs/trabajador_oferta_detalle.html', context)


# UD6.7j - Postular a Oferta
def trabajador_postular(request, oferta_id):
    """
    Permite al trabajador postularse a una oferta
    """
    trabajador = Trabajador.objects.first()  # TEMPORAL
    
    if not trabajador:
        messages.error(request, "No se encontró el perfil de trabajador")
        return redirect('index')
    
    oferta = get_object_or_404(Oferta, id=oferta_id)
    
    # Validaciones
    if oferta.estado != Oferta.Estados.ABIERTA:
        messages.error(request, "Esta oferta ya no está disponible")
        return redirect('jobs:trabajador_explorar_ofertas')
    
    if oferta.plazas_disponibles <= 0:
        messages.error(request, "Esta oferta ya no tiene plazas disponibles")
        return redirect('jobs:trabajador_explorar_ofertas')
    
    # Verificar si ya postuló
    inscripcion_existente = Inscripcion.objects.filter(
        trabajador=trabajador,
        oferta=oferta
    ).first()
    
    if inscripcion_existente:
        messages.warning(request, "Ya te has postulado a esta oferta anteriormente")
        return redirect('jobs:trabajador_oferta_detalle', oferta_id=oferta.id)
    
    # Crear inscripción
    Inscripcion.objects.create(
        trabajador=trabajador,
        oferta=oferta,
        estado=Inscripcion.Estados.PENDIENTE
    )
    
    messages.success(request, f"Te has postulado exitosamente a '{oferta.titulo}'")
    return redirect('jobs:trabajador_mis_candidaturas')


# UD6.7k - Mis Candidaturas (Trabajador)
def trabajador_mis_candidaturas(request):
    """
    Lista todas las candidaturas del trabajador
    """
    trabajador = Trabajador.objects.first()  # TEMPORAL
    
    if not trabajador:
        messages.error(request, "No se encontró el perfil de trabajador")
        return redirect('index')
    
    # Filtros
    estado_filtro = request.GET.get('estado', '')
    
    # Query base
    candidaturas = Inscripcion.objects.filter(
        trabajador=trabajador
    ).select_related('oferta__empresa', 'oferta__categoria')
    
    # Aplicar filtros
    if estado_filtro:
        candidaturas = candidaturas.filter(estado=estado_filtro)
    
    # Ordenar
    candidaturas = candidaturas.order_by('-fecha_inscripcion')
    
    # Paginación
    paginator = Paginator(candidaturas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'trabajador': trabajador,
        'page_obj': page_obj,
        'candidaturas': page_obj,
        'estado_filtro': estado_filtro,
        'estados': Inscripcion.Estados.choices,
    }
    
    return render(request, 'jobs/trabajador_mis_candidaturas.html', context)
