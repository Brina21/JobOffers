# UD6.4 - Configuración del administrador de Django
# messages/admin.py
from django.contrib import admin
from .models import MensajePrivado, ChatGrupal, MensajeGrupal, ParticipanteChat

@admin.register(MensajePrivado)
class MensajePrivadoAdmin(admin.ModelAdmin):
    list_display = ('emisor', 'receptor', 'fecha_envio', 'leido')  # Columnas visibles en la lista
    list_filter = ('leido', 'fecha_envio')  # Filtros por estado de lectura y fecha
    search_fields = ('emisor__email', 'receptor__email', 'contenido')  # Búsqueda en emails y contenido
    readonly_fields = ('fecha_envio',)  # Fecha de envío automática, no editable
    ordering = ('-fecha_envio',)

@admin.register(ChatGrupal)
class ChatGrupalAdmin(admin.ModelAdmin):
    list_display = ('nombre_grupo', 'oferta', 'activo', 'fecha_creacion')  # Información del chat grupal
    list_filter = ('activo', 'fecha_creacion')  # Filtros por estado y fecha de creación
    search_fields = ('nombre_grupo', 'oferta__titulo')  # Búsqueda por nombre y oferta
    readonly_fields = ('fecha_creacion',)  # Fecha de creación automática
    ordering = ('-fecha_creacion',)  # Orden por fecha descendente

@admin.register(MensajeGrupal)
class MensajeGrupalAdmin(admin.ModelAdmin):
    list_display = ('chat_grupal', 'usuario', 'fecha_envio')  # Datos del mensaje grupal
    list_filter = ('fecha_envio', 'chat_grupal')  # Filtros por fecha y chat
    search_fields = ('contenido', 'usuario__email')  # Búsqueda en contenido y usuario
    readonly_fields = ('fecha_envio',)  # Fecha automática
    ordering = ('fecha_envio',)  # Orden cronológico

@admin.register(ParticipanteChat)
class ParticipanteChatAdmin(admin.ModelAdmin):
    list_display = ('chat_grupal', 'usuario', 'rol', 'fecha_union')  # Información del participante
    list_filter = ('rol', 'fecha_union')  # Filtros por rol y fecha de unión
    search_fields = ('usuario__email', 'chat_grupal__nombre_grupo')  # Búsqueda por usuario y chat
    readonly_fields = ('fecha_union',)  # Fecha de unión automática
    ordering = ('-fecha_union',)