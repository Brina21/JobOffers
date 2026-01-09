# jobs/admin.py
from django.contrib import admin
from .models import Categoria, Oferta, Inscripcion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'categoria', 'estado', 'urgente', 'fecha_evento', 'plazas_disponibles', 'fecha_publicacion')
    list_filter = ('estado', 'urgente', 'categoria', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion', 'empresa__nombre_empresa')
    readonly_fields = ('fecha_publicacion',)
    ordering = ('-fecha_publicacion',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('oferta', 'trabajador', 'estado', 'fecha_inscripcion')
    list_filter = ('estado', 'fecha_inscripcion')
    search_fields = ('oferta__titulo', 'trabajador__id_usuario__nombre')
    readonly_fields = ('fecha_inscripcion',)
    ordering = ('-fecha_inscripcion',)