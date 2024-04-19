from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import MensajesRecibidos, Error, Flow, Cliente,Key
from django.utils import timezone

import json
from . import services

def resp_ok(resp,name):
    if resp.status_code == 200:
        return True
    else:
        try:
            Error.objects.create(error=name,json=resp.json()).save()
        except:
            Error.objects.create(error=name,json=resp.text).save()
        return False

# Register your models here.\\
@admin.register(MensajesRecibidos)
class MensajesRecibidosAdmin(admin.ModelAdmin):
    list_display=('telefono_cliente','mensaje','creado','id_wa')

class ClienteResource(resources.ModelResource):
    
    class Meta:
        model = Cliente
        import_id_fields = ('preventa',)


@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    list_display=('preventa','nombre','telefono','pregunta_1','comentario','contacto','iniciar','completo','cant_envios','fecha_finalizacion')
    list_filter = ['completo','iniciar']
    date_hierarchy = 'fecha_finalizacion'
    resource_class = ClienteResource
    actions = ('envio_campana',)

    @admin.action(description='Enviar csi')
    def envio_campana(self,request,objetos):
        token = Key.objects.get(name='wap')
        envios_ok = 0
        envios_no_ok = 0
        for obj in objetos:
            data = json.dumps(
                    {
        "messaging_product": "whatsapp",
        "to": obj.telefono,
        "type": "template",
        "template": {
            "name": 'encuesta_csi',
            "language": {
                "code": "es",
                "policy": "deterministic"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": obj.nombre
                        },
                        {
                            "type": "text",
                            "text": obj.modelo
                        },
                        {
                            "type": "text",
                            "text": obj.patente
                        },
                        {
                            "type": "text",
                            "text": obj.entrega
                        }
                    ]
                }
            ]
        }
        }
            )
            resp = services.enviar_Mensaje_whatsapp(token.token,token.url,data)
            
            if resp_ok(resp,'Enviando plantilla'):
                envios_ok += 1
                obj.contacto = timezone.now()
                obj.cant_envios += 1
                obj.save()
                Error.objects.create(error=str(obj.f_envio),json=resp.json()).save()
            else:
                envios_no_ok += 1

        if envios_no_ok == 0:
            self.message_user(request, f'{envios_ok} mensajes enviados')
        else:
            self.message_user(request, f'{envios_ok} mensajes enviados y {envios_no_ok} No enviados', level='ERROR')

                
  

@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display=('flow_id','respuesta_ok','next_flow','respuesta_nook')
    

admin.site.register(Error)
admin.site.register(Key)

