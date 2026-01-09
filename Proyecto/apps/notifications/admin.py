# UD6.4 - Configuración del administrador de Django
# notifications/admin.py
from django.contrib import admin
from .models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'leida', 'fecha_creacion')  # Campos mostrados en la lista
    list_filter = ('tipo', 'leida', 'fecha_creacion')  # Filtros por tipo, lectura y fecha
    search_fields = ('titulo', 'mensaje', 'usuario__email')  # Búsqueda en título, mensaje y email
    readonly_fields = ('fecha_creacion',)  # Fecha de creación automática
    ordering = ('-fecha_creacion',)