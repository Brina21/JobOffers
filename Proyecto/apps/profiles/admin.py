# UD6.4 - Configuración del administrador de Django
# profiles/admin.py
from django.contrib import admin
from .models import Administrador, Empresa, Trabajador

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('id_usuario',)  # Muestra el usuario en la lista
    search_fields = ('id_usuario__email',)  # Permite buscar por email del usuario
    ordering = ('id_usuario',)  # Ordena por usuario

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'cif', 'ciudad', 'tipo_establecimiento', 'valoracion_media')  # Columnas mostradas
    list_filter = ('ciudad', 'tipo_establecimiento')  # Filtros laterales
    search_fields = ('nombre_empresa', 'cif')  # Campos de búsqueda
    readonly_fields = ('valoracion_media',)  # Campos de solo lectura (se calculan automáticamente)
    ordering = ('nombre_empresa',)  # Ordenación predeterminada

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'ciudad', 'valoracion_media', 'bloqueado', 'cancelaciones_totales')  # Columnas visibles
    list_filter = ('bloqueado', 'ciudad')  # Filtros por estado de bloqueo y ciudad
    search_fields = ('id_usuario__nombre', 'id_usuario__apellidos', 'id_usuario__email')  # Búsqueda en campos relacionados
    readonly_fields = ('valoracion_media', 'cancelaciones_totales')  # Campos calculados, no editables
    ordering = ('id_usuario__nombre',)  # Orden alfabético por nombre