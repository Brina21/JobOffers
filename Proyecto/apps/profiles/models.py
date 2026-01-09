# profiles/models.py
from django.db import models

class Administrador(models.Model):
    id_usuario = models.OneToOneField('users.Usuario', on_delete=models.CASCADE, primary_key=True, related_name='administrador')

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        ordering = ['id_usuario']

    def __str__(self):
        return f"Admin: {self.id_usuario.email}"

class Empresa(models.Model):
    
    class Establecimientos(models.TextChoices):
        class TipoEstablecimiento(models.TextChoices):
            HOTEL = 'Hotel', 'Hotel'
            HOSTAL = 'Hostal', 'Hostal'
            RESTAURANTE = 'Restaurante', 'Restaurante'
            CAFETERIA = 'Cafetería', 'Cafetería'
            BAR = 'Bar', 'Bar'
            GASTROBAR = 'Gastrobar', 'Gastrobar'
            CATERING = 'Catering', 'Catering'
            SALA_EVENTOS = 'Sala de eventos', 'Sala de eventos'
            OTRO = 'Otro', 'Otro'
    
    id_usuario = models.OneToOneField('users.Usuario', on_delete=models.CASCADE, primary_key=True, related_name='empresa')
    
    nombre_empresa = models.CharField(max_length=200, verbose_name="Nombre de la Empresa", null=False)
    cif = models.CharField(max_length=20, unique=True, verbose_name="CIF", null=False)
    calle = models.CharField(max_length=300, verbose_name="Calle", null=False)
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", blank=True)
    localidad = models.CharField(max_length=200, verbose_name="Localidad", blank=True)
    codigo_postal = models.CharField(max_length=100, verbose_name="Código Postal", blank=True)
    tipo_establecimiento = models.CharField(max_length=50, verbose_name="Tipo Establecimiento", choices=Establecimientos.choices)
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    valoracion_media = models.FloatField(verbose_name="Valoración Media", default=0.0)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre_empresa']

    def __str__(self):
        return self.nombre_empresa

class Trabajador(models.Model):
    id_usuario = models.OneToOneField('users.Usuario', on_delete=models.CASCADE, primary_key=True, related_name='trabajador')
    
    calle = models.CharField(max_length=300, verbose_name="Calle", null=False)
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", blank=True)
    codigo_postal = models.CharField(max_length=100, verbose_name="Código Postal", blank=True)
    experiencia_laboral = models.TextField(verbose_name="Experiencia Laboral", blank=True)
    disponibilidad_horaria = models.TextField(verbose_name="Disponibilidad Horaria", blank=True)
    valoracion_media = models.FloatField(verbose_name="Valoración Media", default=0.0)
    bloqueado = models.BooleanField(default=False)
    motivo_bloqueo = models.TextField(verbose_name="Motivo de Bloqueo", blank=True, null=True)
    fecha_fin_bloqueo = models.DateTimeField(verbose_name="Fecha de Fin de Bloqueo", blank=True, null=True)
    cancelaciones_totales = models.IntegerField(verbose_name="Cancelaciones Totales", default=0)

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ['id_usuario__nombre']

    def __str__(self):
        return f"{self.id_usuario.nombre} {self.id_usuario.apellidos}"