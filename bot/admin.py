from django.contrib import admin
from .models import MensajesRecibidos, Error, Flow, Cliente,Key

# Register your models here.\\
class MensajesRecibidosAdmin(admin.ModelAdmin):
    list_display=('telefono_cliente','mensaje','creado','id_wa')

class ClienteAdmin(admin.ModelAdmin):
    list_display=('nombre','telefono','email','flow','contacto')

class FlowAdmin(admin.ModelAdmin):
    list_display=('flow_id','respuesta_ok','next_flow','respuesta_nook')

admin.site.register(MensajesRecibidos, MensajesRecibidosAdmin)
admin.site.register(Error)
admin.site.register(Flow,FlowAdmin)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Key)

