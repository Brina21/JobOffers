# users/admin.py
from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'apellidos', 'dni', 'tipo_usuario', 'activo', 'fecha_registro')
    list_filter = ('tipo_usuario', 'activo', 'fecha_registro')
    search_fields = ('email', 'nombre', 'apellidos', 'dni')
    ordering = ('-fecha_registro',)
    readonly_fields = ('fecha_registro',)