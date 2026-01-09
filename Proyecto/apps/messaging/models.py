# messages/models.py
from django.db import models

class MensajePrivado(models.Model):
    id = models.AutoField(primary_key=True)
    contenido = models.TextField(verbose_name="Contenido", null=False)
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Envío")
    leido = models.BooleanField(default=False, verbose_name="Leído")

    emisor = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, related_name='mensajes_enviados', verbose_name="Emisor")
    receptor = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, related_name='mensajes_recibidos', verbose_name="Receptor")
    
    class Meta:
        verbose_name = "Mensaje Privado"
        verbose_name_plural = "Mensajes Privados"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.emisor} → {self.receptor}"

class ChatGrupal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=200, verbose_name="Nombre del Grupo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    fecha_desactivacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha desactivación")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    oferta = models.OneToOneField('jobs.Oferta', on_delete=models.CASCADE, verbose_name="Oferta", related_name='chat_grupal')

    class Meta:
        verbose_name = "Chat Grupal"
        verbose_name_plural = "Chats Grupales"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre_grupo

class MensajeGrupal(models.Model):
    id = models.AutoField(primary_key=True)
    contenido = models.TextField(verbose_name="Contenido")
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha envío")

    chat_grupal = models.ForeignKey(ChatGrupal, on_delete=models.CASCADE, related_name='mensajes', verbose_name="Chat Grupal")
    usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, verbose_name="Usuario", related_name='mensajes_grupales')

    class Meta:
        verbose_name = "Mensaje Grupal"
        verbose_name_plural = "Mensajes Grupales"
        ordering = ['fecha_envio']

    def __str__(self):
        return f"Mensaje en {self.chat_grupal.nombre_grupo}"

class ParticipanteChat(models.Model):
    id = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=50, verbose_name="Rol")
    fecha_union = models.DateTimeField(auto_now_add=True, verbose_name="Fecha unión")

    chat_grupal = models.ForeignKey(ChatGrupal, on_delete=models.CASCADE, related_name='participantes', verbose_name="Chat grupal")
    usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE, verbose_name="Usuario", related_name='participaciones_chat')

    class Meta:
        verbose_name = "Participante de Chat"
        verbose_name_plural = "Participantes de Chat"
        unique_together = [['chat_grupal', 'usuario']]
        ordering = ['-fecha_union']

    def __str__(self):
        return f"{self.usuario} en {self.chat_grupal.nombre_grupo}"