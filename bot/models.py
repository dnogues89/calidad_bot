from django.db import models

# Create your models here.
class Key(models.Model):
    name = models.CharField(max_length=50)
    url=models.CharField(max_length=100)
    token=models.CharField(max_length=500)


class Error(models.Model):
    error = models.TextField()
    json = models.JSONField()
    
class Cliente(models.Model):
    telefono = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True,null=True)
    email = models.CharField(max_length=50, blank=True,null=True)
    flow = models.IntegerField(blank=True,null=True)
    pregunta_1 = models.IntegerField()
    pregunta_2 = models.IntegerField()
    pregunta_3 = models.IntegerField()
    pregunta_4 = models.IntegerField()
    pregunta_5 = models.IntegerField()
    contacto = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
    
class Flow(models.Model):
    flow_id = models.IntegerField()
    respuesta_ok = models.TextField()
    next_flow = models.IntegerField(blank=True,null=True)
    respuesta_nook = models.TextField(blank=True,null=True)
    
class MensajesRecibidos(models.Model):
    id_wa = models.CharField(max_length=100, unique=True)
    mensaje = models.TextField()
    timestamp = models.IntegerField()
    telefono_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    telefono_receptor = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_now_add=True)
    json = models.JSONField(blank=True)
    
    class Meta:
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
    