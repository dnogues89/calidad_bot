from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MensajesRecibidos, Error,Key, Cliente, Flow
from django.views.decorators.csrf import csrf_exempt
from . import services
import re


import json

class ChatFlow():
    def __init__(self, cliente, mensaje) -> None:
        self.cliente = cliente
        self.mensaje = mensaje
        self.flow = Flow.objects.get(flow_id=self.cliente.flow)
        self.get_respuesta()
        

    
    def get_respuesta(self):
        hash_map = {
            0:True,
            1:self.validate_numero(self.mensaje,5),
            2:self.validate_numero(self.mensaje,5),
            3:self.validate_numero(self.mensaje,5),
            4:self.validate_numero(self.mensaje,5),
            5:True,
            10:True,
        }
        
        if hash_map[self.flow.flow_id]:
            self.update_cliente()
            self.answer = self.flow.respuesta_ok
            self.cliente.flow=self.flow.next_flow
            self.cliente.save()
        else:
            self.answer = Flow.objects.filter(next_flow=self.flow.flow_id)[0].respuesta_nook

              
    def update_cliente(self):
        if self.flow.flow_id == 1:
            self.cliente.pregunta_1 = self.mensaje
        if self.flow.flow_id == 2:
            self.cliente.pregunta_2 = self.mensaje
        if self.flow.flow_id == 3:
            self.cliente.pregunta_3 = self.mensaje
        if self.flow.flow_id == 4:
            self.cliente.pregunta_4 = self.mensaje
        if self.flow.flow_id == 5:
            self.cliente.pregunta_5 = self.mensaje



    def validate_mail(self, correo):
        patron = r'^[A-Za-z0-9\s\._%+-]+@[\w\.-]+\.\w+$'
        if re.match(patron, correo):
            return True
        else:
            return False

    def validate_numero(self,numero,numero_max):
        try:
            numero = int(numero)
            if numero <= numero_max:
                return True
        except:
            return False
    
def procesar_mensaje(body):
    try:
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)
        return text

    except Exception as e:
        return 'No procesado' + str(e)




# Create your views here.
@csrf_exempt
def webhook(request):
    # SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        # SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.GET.get('hub.verify_token') == "CalidadESPASA":
            # ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return HttpResponse(request.GET.get('hub.challenge'))
        else:
            # SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            return HttpResponse("Error de autentificacion.")
    
    if request.method == "POST":    
        data = json.loads(request.body.decode('utf-8'))
        token = Key.objects.get(name='wap')
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            
            if data['entry'][0]['changes'][0]['value']['messages'][0]['type']!='text':
                telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                telefonoCliente=f'54{str(telefonoCliente[3:])}'
                mensaje='Imagen o Audio'
                idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
                timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
                try:
                    MensajesRecibidos.objects.get(id_wa=idWA)
                except:
                    try:
                        cliente = Cliente.objects.get(telefono = telefonoCliente)
                    except:
                        cliente=Cliente.objects.create(telefono = telefonoCliente,flow = 50).save()
                    MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=cliente,telefono_receptor='espasa_calidad',json=data).save()             
                    
                    try:
                        iniciar = data["entry"][0]['changes'][0]['value']['messages'][0]['button']['text'] == 'Ir a la encuesta'
                        if iniciar:
                            cliente.flow = 0
                            cliente.save()
                            respuesta = ChatFlow(cliente,mensaje).answer
                    except:
                        respuesta = 'Recorda que soy un 🤖 y mi creador no me dio la capacidad de 👀 o👂, pero enviame un *Texto* que estoy para ayudarte. 🦾'
                    
                    data = services.text_Message(telefonoCliente,respuesta)
                    print(services.enviar_Mensaje_whatsapp(token.token,token.url,data))
                        
        try:  
            if 'messages' in data['entry'][0]['changes'][0]['value']:
                if data['entry'][0]['changes'][0]['value']['messages'][0]['type']=='text':
                    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                    telefonoCliente=f'54{str(telefonoCliente[3:])}'
                    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
                    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
                    try:
                        MensajesRecibidos.objects.get(id_wa=idWA)
                    except:
                        try:
                            cliente = Cliente.objects.get(telefono = telefonoCliente)
                        except:
                            cliente=Cliente.objects.create(telefono = telefonoCliente,flow = 0).save()
                        
                        MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=cliente,telefono_receptor='baires',json=data).save()
                        chat = ChatFlow(cliente,mensaje)
                        data = services.text_Message(chat.cliente.telefono,chat.answer)
                        print(services.enviar_Mensaje_whatsapp(token.token,token.url,data))
                        
        except json.JSONDecodeError:
            
            Error.objects.create(error='No se pudo decodificar el JSON').save()
            return JsonResponse({"error": "Error al decodificar JSON"}, status=400)

        Error.objects.create(error='OK',json=data).save()

    return HttpResponse('Hola mundo')

def clientes_abandonados(request):
    from datetime import datetime, timedelta
    limit = datetime.now() - timedelta(minutes=30)
    clientes = Cliente.objects.filter(flow=50)
    for cliente in clientes:
        if cliente.contacto < limit:
            cliente.flow = 30
            cliente.save()
    
    # Filtra los clientes según tus condiciones
    clientes = Cliente.objects.exclude(
        flow__in=['30', '50', '0'],
        contacto__lt=limit
    )
    for cliente in clientes:
        cliente.flow=0
        #ACA SE MANDA AL CRM!
        
        cliente.save()
        
        
def realizar_encuesta(request): 
    cliente = Cliente.objects.get(pk=1)
    data = json.dumps(
            {
   "messaging_product": "whatsapp",
   "to": cliente.telefono,
   "type": "template",
   "template": {
       "name": "encuesta_calidad",
       "language": {
           "code": "es_AR",
           "policy": "deterministic"
       },
       "components": [
           {
               "type": "body",
               "parameters": [
                   {
                       "type": "text",
                       "text": cliente.nombre
                   },
                   {
                       "type": "text",
                       "text": str(cliente.entrega.strftime("%d-%m-%Y"))
                   },
                   {
                       "type": "text",
                       "text": cliente.modelo
                   },
               ]
           },
           {
               "type": "button",
               "sub_type": "quick_reply",
               "index": 0,
               "parameters": [
                   {
                       "type": "text",
                       "text": "Ir a la encuesta"
                   }
               ]
           }
       ]
   }
}
    )
    print(data)
    
    token = Key.objects.get(name='wap')
    resp = services.enviar_Mensaje_whatsapp(token.token,token.url,data)
    return HttpResponse(f'{str(resp)} - {str(data)} ')