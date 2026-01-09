# jobs/models.py
from django.db import models

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre", null=False)
    descripcion = models.TextField(verbose_name="Descripción", null=False)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Oferta(models.Model):
    
    class Estados(models.TextChoices):
        ABIERTA = 'Abierta', 'Abierta'
        CERRADA = 'Cerrada', 'Cerrada'
        EN_PROCESO = 'En Proceso', 'En Proceso'
    
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200, verbose_name="Título", null=True)
    descripcion = models.TextField(null=False)
    precio_hora = models.DecimalField(verbose_name="Precio por Hora €", max_digits=8, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(verbose_name="Total €", max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_contrato = models.CharField(max_length=100, verbose_name="Tipo de Contrato", null=True, blank=True)
    jornada = models.CharField(max_length=100, verbose_name="Jornada", null=True, blank=True)
    plazas_totales = models.IntegerField(verbose_name="Plazas Totales", null=True, default=0)
    plazas_disponibles = models.IntegerField(verbose_name="Plazas Disponibles", null=True, default=0)
    horario = models.CharField(max_length=200, verbose_name="Horario", null=True, blank=True)
    urgente = models.BooleanField(default=False)
    fecha_evento = models.DateField(verbose_name="Fecha del Evento", null=True, blank=True)
    estado = models.CharField(max_length=50, verbose_name="Estado", choices=Estados.choices, null=True, default=Estados.ABIERTA)
    fecha_publicacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Publicación", null=False, blank=True)
    fecha_cierre = models.DateField(verbose_name="Fecha de Cierre", null=True, blank=True)
    
    empresa = models.ForeignKey('profiles.Empresa', on_delete=models.SET_NULL, verbose_name="Empresa", null=True, related_name='ofertas')
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, verbose_name="Categoría", null=True, related_name='ofertas')

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo or f"Oferta #{self.id}"

class Inscripcion(models.Model):
    
    class Estados(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente'
        ACEPTADA = 'Aceptada', 'Aceptada'
        RECHAZADA = 'Rechazada', 'Rechazada'
    
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, verbose_name="Estado", choices=Estados.choices, null=False, default=Estados.PENDIENTE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inscripción", null=False)
    
    oferta = models.ForeignKey('Oferta', on_delete=models.CASCADE, verbose_name="Oferta", null=False, related_name='inscripciones')
    trabajador = models.ForeignKey('profiles.Trabajador', on_delete=models.CASCADE, verbose_name="Trabajador", null=False, related_name='inscripciones')

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = [['oferta', 'trabajador']]
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        return f"{self.trabajador} - {self.oferta}"