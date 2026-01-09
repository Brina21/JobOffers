# UD6.4 - Configuración del administrador de Django
# reviews/admin.py
from django.contrib import admin
from .models import Valoracion

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'trabajador', 'puntuacion', 'fecha_valoracion')  # Columnas visibles
    list_filter = ('puntuacion', 'fecha_valoracion')  # Filtros por puntuación y fecha
    search_fields = ('empresa__nombre_empresa', 'trabajador__id_usuario__nombre', 'comentario')  # Búsqueda
    readonly_fields = ('fecha_valoracion',)  # Fecha automática, no editable
    ordering = ('-fecha_valoracion',)