# notifications/models.py
from django.db import models

class Notificacion(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, verbose_name="Tipo", null=False)
    titulo = models.CharField(max_length=200, verbose_name="Título", null=False)
    mensaje = models.TextField(verbose_name="Mensaje", null=False)
    id_referencia = models.IntegerField(verbose_name="ID de Referencia", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación", null=False)
    leida = models.BooleanField(default=False, verbose_name="Leída")
    
    usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, verbose_name="Usuario", null=False, related_name='notificaciones')

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} - {self.usuario}"