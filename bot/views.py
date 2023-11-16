from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MensajesRecibidos, Error,Key, Cliente, Flow
from django.views.decorators.csrf import csrf_exempt
from . import services
import re

from calidad.models import Encuesta


import json

modelos = {
1:{'modelo':'Amarok','ficha':'\n*Motor 2.0l:* https://bit.ly/3npJSfV\n*Motor V6:* https://bit.ly/3Vr63ix'},
2:{'modelo':'Taos','ficha':'http://bit.ly/3X4d49L'},
3:{'modelo':'T-Cross','ficha':'https://bit.ly/3p9gf2U'},
4:{'modelo':'Nivus','ficha':'https://bit.ly/422l5h1'},
5:{'modelo':'Polo','ficha':'https://bit.ly/3P7xjBv'},
6:{'modelo':'Tiguan','ficha':'https://bit.ly/3p0mZQB'},
}

class ChatFlow():
    def __init__(self, cliente, mensaje) -> None:
        self.cliente = cliente
        self.mensaje = mensaje
        self.flow = Flow.objects.get(flow_id=self.cliente.flow)
        self.get_respuesta()
        

    
    def get_respuesta(self):
        hash_map = {
            0:True,
            1:True,
            2:self.validate_mail(self.mensaje),
            22:self.validate_numero(self.mensaje,2),
            3:self.validate_numero(self.mensaje,3),
            4:self.validate_numero(self.mensaje,6),
            30:True,
            50:True,
        }
        
        if hash_map[self.flow.flow_id]:
            self.update_cliente()
            self.answer = self.flow.respuesta_ok
            self.answer = self.answer.replace('{self.cliente.nombre}',str(self.cliente.nombre)).replace('{self.cliente.telefono}',str(self.cliente.telefono)).replace('{self.cliente.email}',str(self.cliente.email))
            try:
                self.answer = self.answer.replace('{self.cliente.nombre}',str(self.cliente.nombre)).replace('{self.cliente.telefono}',str(self.cliente.telefono)).replace('{self.cliente.email}',str(self.cliente.email)).replace("{modelos[int(self.mensaje)]['modelo']}",modelos[int(self.mensaje)]['modelo']).replace("{modelos[int(self.mensaje)]['ficha']}",modelos[int(self.mensaje)]['ficha'])
            except:
                pass
            self.cliente.flow=self.flow.next_flow
            self.cliente.save()
        else:
            self.answer = Flow.objects.filter(next_flow=self.flow.flow_id)[0].respuesta_nook

              
    def update_cliente(self):
        if self.flow.flow_id == 1:
            self.cliente.nombre = self.mensaje
        if self.flow.flow_id == 2:
            self.cliente.email = self.mensaje
        if self.flow.flow_id == 22:
            if str(self.mensaje) != '1':
                self.cliente.flow = 0
                self.flow = Flow.objects.get(flow_id=0)
        if self.flow.flow_id == 3:
            self.cliente.canal = self.mensaje
        if self.flow.flow_id == 4:
            self.cliente.modelo = modelos[int(self.mensaje)]['modelo']
        if self.flow.flow_id == 50:
            if self.cliente.comentario == None:
                self.cliente.comentario = self.mensaje


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


class ChatEncuesta():
    def __init__(self,encuesta,mensaje) -> None:
        self.cliente = encuesta.cliente
        try:
            self.id_wa_enviado = mensaje["entry"][0]['changes'][0]['value']['messages'][0]['context']['id']
            self.mensaje = len(mensaje["entry"][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply']['title'])
        except:
            pass
        self.encuesta = encuesta
        self.token = Key.objects.get(name='wap')
        self.get_respuesta()
        self.enviar_mensaje()
    

    
    def get_respuesta(self):
        hash_map = {
            0:[self.encuesta.pregunta_1,""],
            1:[self.encuesta.pregunta_2,self.encuesta.respuesta_1],
            2:[self.encuesta.pregunta_3,self.encuesta.respuesta_2],
            3:[self.encuesta.pregunta_4,self.encuesta.respuesta_3],
            4:[self.encuesta.pregunta_5,self.encuesta.respuesta_4],
            5:['Muchas gracias',self.encuesta.respuesta_5],
        }
        
        self.answer = hash_map[self.encuesta.flow][0]
        self.respuesta_1 = self.mensaje
        self.encuesta.flow = int(self.encuesta.flow) + 1
        self.encuesta.save()

    def enviar_mensaje(self):
        if self.encuesta.flow < 5:
            list = []
            body = self.answer
            footer = "Calidad Espasa"
            options = ["⭐​", "⭐​⭐​","⭐​⭐​⭐​","⭐​⭐​⭐​⭐​","⭐​⭐​⭐​⭐​⭐​"]

            replyButtonData = services.listReply_Message(self.cliente.telefono, options, body, footer, "sed1",1)
            list.append(replyButtonData)
            for item in list:
                envio = services.enviar_Mensaje_whatsapp(self.token.token,self.token.url,item)       
                print(envio)
        else:
            data = services.text_Message(self.cliente.telefono,self.answer)
            envio = services.enviar_Mensaje_whatsapp(self.token.token,self.token.url,data)        
            print(envio)
        
    

# Create your views here.
@csrf_exempt
def webhook(request):
    # SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        # SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.GET.get('hub.verify_token') == "FransiBOT":
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
                        cliente=Cliente.objects.create(telefono = telefonoCliente,flow = 0).save()
                    MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=cliente,telefono_receptor='baires',json=data).save()
                    
                    try:
                        encuesta = Encuesta.objects.get(cliente=cliente)

                        if int(encuesta.flow) <=5:
                            ChatEncuesta(encuesta,data)
                    except:                
                        respuesta = 'Recorda que soy un 🤖 y mi creador no me dio la capacidad de 👀 o👂, pero enviame un *Texto* que estoy para ayudarte. 🦾'
                        data = services.text_Message(telefonoCliente,respuesta)
                        services.enviar_Mensaje_whatsapp(token.token,token.url,data)
                        
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
                        services.enviar_Mensaje_whatsapp(token.token,token.url,data)             
                        
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