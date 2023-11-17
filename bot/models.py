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
    telefono = models.CharField(max_length=50,unique=True, blank=True,null=True)
    nombre = models.CharField(max_length=50, blank=True,null=True)
    preventa = models.CharField(max_length=30,primary_key=True)
    patente = models.CharField(max_length=30, blank=True,null=True)
    entrega = models.DateField(blank=True,null=True)
    modelo = models.CharField(max_length=50, blank=True,null=True)
    pregunta_1 = models.IntegerField(blank=True,null=True)
    pregunta_2 = models.IntegerField(blank=True,null=True)
    pregunta_3 = models.IntegerField(blank=True,null=True)
    pregunta_4 = models.IntegerField(blank=True,null=True)
    pregunta_5 = models.IntegerField(blank=True,null=True)
    flow = models.IntegerField(blank=True,null=True)
    contacto = models.DateTimeField(blank=True,null=True)
    iniciar = models.BooleanField(blank=True,default=False)
    completo = models.BooleanField(blank=True,default=False)
    
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
    