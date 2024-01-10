from .models import Key
import requests


class Notificaciones:
    def __init__(self, cliente) -> None:
        self.cliente = cliente
        webhook = Key.objects.get(name='teams')
        self.webhook = f'{webhook.url}{webhook.token}'
        self.set_data()

    def set_data(self):
        self.data = {
                        "title": "{} - {}".format(self.cliente.preventa,self.cliente.pregunta_1),
                        "text": "Comentario:{}".format(self.cliente.comentario),
                        "sections": [
                                {
                                    "activityTitle": "{}".format(self.cliente.fecha_finalizacion.strftime('%d-%m-%Y')),
                                    "facts": [
                                        {
                                            "name": "Nota",
                                            "value": "{}".format(self.cliente.pregunta_1)
                                        },
                                        {
                                            "name": "Comentario",
                                            "value": "{}".format(self.cliente.comentario)
                                        }
                                    ]
                                }
                            ]
                    }

    def card(self):
        return {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "Resumen de la tarjeta",
        "themeColor": "0078D7",
        "title": self.data['title'],
        "text": self.data['text'],
        # "sections": self.data['sections']
    }
        
    def send_card(self):
        response = requests.post(self.webhook,json=self.card())
        print(response)
        print(response.text)

