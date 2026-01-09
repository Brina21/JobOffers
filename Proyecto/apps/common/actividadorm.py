from django.db import models, transaction
from apps.users.models import Usuario
from apps.profiles.models import Trabajador, Empresa
from apps.jobs.models import Categoria, Oferta, Inscripcion

# CRUD Usuarios
# Usuario base
@transaction.atomic # Operaciones dentro de la función son atómicas y se deben completar todas o ninguna
def crear_usuario(
    nombre,
    apellidos,
    fecha_nacimiento,
    dni,
    email,
    password,
    telefono
):
    # comprobar que el usuario no exista
    if Usuario.objects.filter(email=email).exists():
        raise ValueError("El correo electrónico ya existe.")
    
    # si no existe el correo crear el usuario
    usuario = Usuario.objects.create(
        nombre = nombre,
        apellidos = apellidos,
        fecha_nacimiento = fecha_nacimiento,
        dni = dni,
        email = email,
        password = password,
        telefono = telefono
    )
    return usuario

# Usuario Trabajador
@transaction.atomic
def crear_trabajador(
    nombre,
    apellidos,
    fecha_nacimiento,
    dni,
    email,
    password,
    telefono,
    calle,
    ciudad,
    codigo_postal,
    experiencia_laboral,
    disponibilidad_horaria
):
    # crear usuario
    usuario = crear_usuario(
        nombre = nombre,
        apellidos = apellidos,
        fecha_nacimiento = fecha_nacimiento,
        dni = dni,
        email = email,
        password = password,
        telefono = telefono,
        tipo_usuario = Usuario.Roles.TRABAJADOR
    )
    
    if not usuario:
        raise ValueError("Error al crear el usuario.")
    
    # crear trabajador
    trabajador = Trabajador.objects.create(
        id_usuario = usuario,
        calle = calle,
        ciudad = ciudad,
        codigo_postal = codigo_postal,
        experiencia_laboral = experiencia_laboral,
        disponibilidad_horaria = disponibilidad_horaria
    )
    return trabajador


# Usuario Empresa
@transaction.atomic
def crear_empresa(
    nombre,
    apellidos,
    fecha_nacimiento,
    dni,
    email,
    password,
    telefono,
    nombre_empresa,
    cif,
    calle,
    ciudad,
    localidad,
    codigo_postal,
    tipo_establecimiento,
    descripcion
):
    # crear usuario
    usuario = crear_usuario(
        nombre = nombre,
        apellidos = apellidos,
        fecha_nacimiento = fecha_nacimiento,
        dni = dni,
        email = email,
        password = password,
        telefono = telefono,
        tipo_usuario = Usuario.Roles.EMPRESA
    )
    
    if not usuario:
        raise ValueError("Error al crear el usuario.")
    
    empresa = Empresa.objects.create(
        id_usuario = usuario,
        nombre_empresa = nombre_empresa,
        cif = cif,
        calle = calle,
        ciudad = ciudad,
        localidad = localidad,
        codigo_postal = codigo_postal,
        tipo_establecimiento = tipo_establecimiento,
        descripcion = descripcion
    )
    return empresa

# Obtener todos los usuarios
def obtener_todos_usuarios():
    return Usuario.objects.all()

# Obtener usuarios por id
def obtener_usuario_id(usuario_id):
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        raise ValueError("Usuario no encontrado.")
    return usuario

# Obtener usuarios por rol
def obtener_usuarios_rol(usuario_rol):
    usuario = Usuario.objects.filter(tipo_usuario=usuario_rol)
    # filter si no encunetra devuelve queryset vacio
    
    if not usuario.exists():
        raise ValueError("No se encontraron usuarios con ese rol.")
    return usuario

# actualizar usuario
@transaction.atomic
def actualizar_usuario(usuario_id, **kwargs): # kwargs: diccionario de atributos a actualizar
    usuario = obtener_usuario_id(usuario_id)
    
    for clave, valor in kwargs.items(): # iteracion clave valor
        if hasattr(usuario, clave): # comprobar si el usuario tiene el atributo dado
            setattr(usuario, clave, valor) # actualizar atributos dinámicamente
    usuario.save()

# eliminar usuario
@transaction.atomic
def eliminar_usuario(usuario_id):
    usuario = obtener_usuario_id(usuario_id)
    if not usuario:
        raise ValueError("Usuario no encontrado.")
    
    usuario.delete()

# CRUD Ofertas y filtrado
# Crear oferta
@transaction.atomic
def crear_oferta(
    titulo,
    descripcion,
    precio_hora,
    total,
    tipo_contrato,
    jornada,
    plazas_totales,
    plazas_disponibles,
    horario,
    urgente,
    fecha_evento,
    estado,
    fecha_publicacion,
    fecha_cierre,
    empresa,
    categoria
):
    empresa_obj = Empresa.objects.filter(id=empresa).first() # obtener empresa
    categoria_obj = Categoria.objects.filter(id=categoria).first() # obtener categoria
    
    if not empresa_obj:
        raise ValueError("Empresa vacía o no encontrada.")
    
    if not categoria_obj:
        raise ValueError("Categoría vacía o no encontrada.")
    
    oferta = Oferta.objects.create(
        titulo = titulo,
        descripcion = descripcion,
        precio_hora = precio_hora,
        total = total,
        tipo_contrato = tipo_contrato,
        jornada = jornada,
        plazas_totales = plazas_totales,
        plazas_disponibles = plazas_disponibles,
        horario = horario,
        urgente = urgente,
        fecha_evento = fecha_evento,
        estado = estado,
        fecha_publicacion = fecha_publicacion,
        fecha_cierre = fecha_cierre,
        empresa = empresa_obj,
        categoria = categoria_obj
    )
    
    return oferta

# Obtener todas las ofertas
def obtener_todas_ofertas():
    return Oferta.objects.all()

# Obtener las ofertas por nombre
def obtener_ofertas_titulo(titulo):
    # icontains: búsqueda insensible a mayúsculas/minúsculas
    oferta = Oferta.objects.filter(titulo__icontains = titulo)
    if not oferta.exists():
        raise ValueError("No se encontraron ofertas con ese título.")
    return oferta

# Actualizar oferta
@transaction.atomic
def actualizar_oferta(oferta_id, **kwargs):
    oferta = Oferta.objects.filter(id = oferta_id).first()
    if not oferta:
        raise ValueError("Oferta no encontrada.")
    
    for clave, valor in kwargs.items():
        if hasattr(oferta, clave):
            setattr(oferta, clave, valor)
    oferta.save()
    return oferta

# Eliminar oferta
@transaction.atomic
def eliminar_oferta(oferta_id):
    oferta = Oferta.objects.filter(id = oferta_id).first()
    if not oferta:
        raise ValueError("Oferta no encontrada.")
    
    oferta.delete()