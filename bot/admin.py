from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import MensajesRecibidos, Error, Flow, Cliente,Key


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
    list_display=('nombre','telefono','entrega','pregunta_1','comentario','contacto','iniciar','completo')
    list_filter = ['completo','iniciar']
    date_hierarchy = 'entrega'
    resource_class = ClienteResource
    

@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display=('flow_id','respuesta_ok','next_flow','respuesta_nook')


admin.site.register(Error)
admin.site.register(Key)

