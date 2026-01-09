# reviews/models.py
from django.db import models

class Valoracion(models.Model):
    id = models.AutoField(primary_key=True)
    puntuacion = models.IntegerField(verbose_name="Puntuación", null=False)
    comentario = models.TextField(verbose_name="Comentario", null=True, blank=True)
    fecha_valoracion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Valoración", null=False)
    
    trabajador = models.ForeignKey('profiles.Trabajador', on_delete=models.CASCADE, verbose_name="Trabajador", null=False, related_name='valoraciones_recibidas')
    empresa = models.ForeignKey('profiles.Empresa', on_delete=models.CASCADE, verbose_name="Empresa", null=False, related_name='valoraciones_realizadas')

    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"
        ordering = ['-fecha_valoracion']

    def __str__(self):
        return f"{self.empresa} → {self.trabajador}: {self.puntuacion}/5"