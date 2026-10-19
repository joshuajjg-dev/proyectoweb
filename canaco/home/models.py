from django.db import models
from django.contrib.auth.models import User

class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    nombre_temporal = models.CharField(max_length=255)
    ruta = models.FileField(upload_to='uploads/')
    tipo = models.CharField(max_length=100, blank=True)
    tamano = models.PositiveIntegerField(default=0)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    createdat = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'archivo'
        verbose_name_plural = 'Archivo'

    @property
    def display_url(self):
        ruta = str(self.ruta)
        if ruta.startswith(('images/', 'css/', 'js/', 'fonts/', 'uploads/profile-default')):
            return f'/static/{ruta}'
        return self.ruta.url


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ForeignKey(Archivo, null=True, blank=True, on_delete=models.SET_NULL)
    apellido_paterno = models.CharField(max_length=80, blank=True)
    apellido_materno = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    createdat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    ESTADO_BORRADOR = 'borrador'
    ESTADO_PUBLICADO = 'publicado'
    ESTADO_CHOICES = [
        (ESTADO_BORRADOR, 'Borrador'),
        (ESTADO_PUBLICADO, 'Publicado'),
    ]

    titulo = models.CharField(max_length=200)
    resumen = models.TextField(blank=True)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='publicaciones')
    imagen_portada = models.ForeignKey(Archivo, on_delete=models.SET_NULL, null=True, blank=True, related_name='portadas')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_BORRADOR)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    visitas = models.PositiveIntegerField(default=0)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)

    @property
    def publicada(self):
        return self.estado == self.ESTADO_PUBLICADO

    def __str__(self):
        return self.titulo


class GaleriaPublicacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='galeria')
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    createdat = models.DateTimeField(auto_now_add=True)


class Comentario(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_APROBADO = 'aprobado'
    ESTADO_BLOQUEADO = 'bloqueado'
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APROBADO, 'Aprobado'),
        (ESTADO_BLOQUEADO, 'Bloqueado'),
    ]

    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PENDIENTE)
    createdat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.publicacion.titulo}'