from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import MensajesRecibidos, Error, Flow, Cliente,Key


# Register your models here.\\
@admin.register(MensajesRecibidos)
class MensajesRecibidosAdmin(admin.ModelAdmin):
    list_display=('telefono_cliente','mensaje','creado','id_wa')

class ClienteResource(resources.ModelResource):
    fields = (
        'nombre',
        'telefono',
        'preventa',
        'patente',
        'entrega',
        'pregunta_1',
        'pregunta_2',
        'pregunta_3',
        'pregunta_4',
        'pregunta_5 ',
    )
    
    class Meta:
        model = Cliente

@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    list_display=('nombre','telefono','entrega','contacto','iniciar','completo')
    list_filter = ['completo',]
    date_hierarchy = ['entrega',]
    resource_class = ClienteResource
    

@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display=('flow_id','respuesta_ok','next_flow','respuesta_nook')


admin.site.register(Error)
admin.site.register(Key)

