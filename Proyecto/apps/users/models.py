# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(
        self, email, first_name=None, last_name=None, password=None, type=None
    ):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Ha de proporcionar un e-mail válido")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Ha de proporcionar un e-mail válido")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    
    class Roles(models.TextChoices):
        ADMINISTRADOR = 'Administrador', 'Administrador'
        TRABAJADOR = 'Trabajador', 'Trabajador'
        EMPRESA = 'Empresa', 'Empresa'
    
    id = models.AutoField(primary_key=True)
    nombreUsuario = models.CharField(max_length=100, verbose_name="Nombre Usuario", blank=True, null=True) ##
    nombre = models.CharField(max_length=100, verbose_name="Nombre", blank=True, default='')
    apellidos = models.CharField(max_length=200, verbose_name="Apellidos", blank=True, default='')
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI", blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True, verbose_name="Correo Electrónico", null=False) ##
    password = models.CharField(max_length=100, verbose_name="Contraseña", null=False)
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True)
    tipo_usuario = models.CharField(max_length=50, verbose_name="Tipo de Usuario", null=False, choices=Roles.choices, default=Roles.TRABAJADOR)
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro", null=False) ##
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización", null=False) ##
    activo = models.BooleanField(default=True) ##

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-fecha_registro']

    def __str__(self):
        return self.email
    
    # Usuario Manager personalizado
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
