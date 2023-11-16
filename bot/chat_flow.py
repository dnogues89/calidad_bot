

modelos = {
    1:{'modelo':'Amarok','ficha':'\n*Motor 2.0l:* https://bit.ly/3npJSfV\n*Motor V6:* https://bit.ly/3Vr63ix'},
    2:{'modelo':'Taos','ficha':'http://bit.ly/3X4d49L'},
    3:{'modelo':'T-Cross','ficha':'https://bit.ly/3p9gf2U'},
    4:{'modelo':'Nivus','ficha':'https://bit.ly/422l5h1'},
    5:{'modelo':'Polo','ficha':'https://bit.ly/3P7xjBv'},
    6:{'modelo':'Tiguan','ficha':'https://bit.ly/3p0mZQB'},
    7:'Otros'
}

"""""

STATUS FLOW

NONE / 0 = No te conozco pido nombre
1 = Tengo tu nombre pido mail
2 = Tengo tu mail pido confirmacion
22 = Tengo confirmacion pido canal
3 = Tengo tu canal pido modelo con opciones
44 = Me pediste 'otro' Modelo
4 = tengo tu modelo.. mando ficha tecnica, pido comentario

5 = tengo todo, mando lead al crm.

Clientes Ya conocidos
30 = Lo saludo (nombre) y arranco pidiendo canal, recategorizo con 2

Clientes esperando ser atendidos
50 = Esperen que alguien se comunique.

"""

class ChatFlow():
    def __init__(self,client,msg,timestamp) -> None:
        self.msg = msg
        self.timestamp = timestamp
        self.client = client
        self.status = 
        self.client_flow_by_status()

    def length_check(self,param):
        if len(self.msg) > param:
            self.answer = f'🚫 Por favor que sean menos de {param} caracteres 🚫️'
            return False
        else:
            return True


    def get_status(self):
        try:
            return self.repo.get_client_status(self.client)[0]
        except:
            return None

    def client_flow_by_status(self):

        if self.status == None or self.status == 0:
            try:
                self.repo.insert_new_client(self.client,self.timestamp)
            except:
                pass
            self.repo.update_client_canal(self.client,1)
            self.repo.update_client_status(self.client,1,self.timestamp)
            self.answer = '🏡¡Hola! Bienvenido a *Espasa* 🚗\n\nUn Asesor Comercial se pondrá en contacto con vos. 👨‍💼\nMientras tanto, te pedimos que nos respondas estas *preguntas* para darte la mejor atención. 🤔\nEn caso que lo necesites, solicitanos una videollamada y te brindamos asesoramiento 100% virtual. 🤳\n*Muchas gracias*\n\n🏷️ ¿Cuál es tu nombre? 🏷️'

        if self.status == 1:
            if self.length_check(60):
                self.repo.update_client_name(self.client,self.msg)
                self.repo.update_client_status(self.client,2,self.timestamp)
                self.answer = '📧 ¿Me decis cual es tu mail? 📧'

        if self.status == 2:
            if self.length_check(110):
                if self.validate_mail(self.msg):
                    self.repo.update_client_mail(self.client,self.msg.lower())
                    self.repo.update_client_status(self.client,22,self.timestamp)
                    lead = self.repo.get_lead_info(self.client)
                    self.answer = f"Como soy un 🤖... ¿Me podes confirmar si estan bien mis 📝?\n\n🏷️ *Nombre:* {lead[0]}\n📱 *Telefono:* {str(lead[2])[3:]}\n📧 *Mail:* {lead[1]}\n\n*Envía*\n1️⃣ Si es correcto\n2️⃣ Si queres modificar"
                else:
                    self.answer = "📧 *Mail invalido* 📧\nRecorda no incluir espacios ni tildes 🚫\nAgregar *@*  e incluir *.com*"

        if self.status == 22:
            if self.validate_numero(self.msg):
                if int(self.msg) ==1:
                    self.repo.update_client_status(self.client,3,self.timestamp)
                    self.answer = '🤖 Soy mas inteligente de lo que pensaba! 🦾\n\nElegí una de las siguientes *opciones:*\n\n1️⃣ Ventas 🚗\n2️⃣ Taller 🔧 \n3️⃣ Auto Ahorro 🚙'
                elif int(self.msg) ==2:
                    self.repo.update_client_status(self.client,1,self.timestamp)
                    self.answer = '🏷️ ¿Cual es tu nombre y apellido? 🏷️'
                else:
                    self.answer = '🚫 Opcion Invalida 🚫\n\nRecuerda enviar\n1️⃣Confirmar\n2️⃣Modificar'
            else:
                self.answer = "🚫 Mensaje invalido 🚫\n\nRecorda escribir solo el numero con tu respuesta\n\n1️⃣ Confirmar\n2️⃣ Modificar"


        if self.status == 3:
            if self.validate_numero(self.msg) and int(self.msg) <=3:
                self.repo.update_client_canal(self.client,self.msg)
                if int(self.msg) == 1:
                    self.repo.update_client_status(self.client,4,self.timestamp)
                    self.answer = '🚗¿Que *modelo* estas buscando?🚙\n\nTe comparto las *opciones:*\n1️⃣ Amarok\n2️⃣ Taos\n3️⃣ T-Cross\n4️⃣ Nivus\n5️⃣ Polo\n6️⃣ Tiguan\n7️⃣ Otro'
                elif int(self.msg) == 3:
                    self.repo.update_client_status(self.client,50,self.timestamp)
                    self.answer = '📱En cualquier momento un *vendedor de Auto Ahorro* se estará comunicando con vos. 👨‍💼 🚗\n\nNormalmente tardamos menos de 30 minutos.⏰\n\n‼️Ah y tene en cuenta que te va a escribir desde un 📱corporativo🏡'
                    lead = self.repo.get_lead_info(self.client)
                    LeadAA(lead[0],lead[1],lead[2],"Tradicional")
            else:
                self.answer = "🚫 Mensaje invalido 🚫\n\nRecorda escribir solo el numero con tu respuesta\n\n1️⃣ Ventas 🚗\n2️⃣ Taller 🔧 \n3️⃣ Auto Ahorro 🚙"


        if self.status == 4:
            if self.validate_numero(self.msg) and int(self.msg)<=6:
                self.repo.update_client_modelo(self.client,modelos[int(self.msg)]['modelo'])
                self.repo.update_client_status(self.client,5,self.timestamp)
                #tengo q configurar el link con la fecha tecnica
                self.answer = f"🦾 *Buena eleccion!* 🚙\n\nAca tenes mas info de *{modelos[int(self.msg)]['modelo']}:*\n{modelos[int(self.msg)]['ficha']}\n\n¿Cual es tu *consulta*? 🤔💬"
                if int(self.msg)==7:
                    self.answer = '🚗 ¿Que *modelo* estas buscando? 🚙'
                    self.repo.update_client_status(self.client,44,self.timestamp)
            else:
                self.answer = '🚫 Mensaje invalido 🚫\n\nRecorda escribir solo el *numero* con tu respuesta\n1️⃣ Amarok\n2️⃣ Taos\n3️⃣ T-Cross\n4️⃣ Nivus\n5️⃣ Polo\n6️⃣ Tiguan\n7️⃣ Otro'

        if self.status ==44:
            self.repo.update_client_modelo(self.client,self.msg)
            self.repo.update_client_status(self.client,5,self.timestamp)
            self.answer = '🦾 *Buena eleccion!* 🚙 \n\n¿Cual es tu *consulta*? 🤔💬'

        if self.status == 5:
            if self.length_check(90):
                self.repo.update_client_comentario(self.client,self.msg)
                self.repo.update_client_status(self.client,50,self.timestamp)
                self.repo.add_client_contact(self.client)
                lead = self.repo.get_lead_info(self.client)
                SendLead(lead[0],lead[1],lead[2],lead[3],lead[4])
                self.answer = '🤖*Ya esta todo listo*✅\n\n📱En cualquier momento un *vendedor* se estará comunicando con vos. 👨‍💼 🚗\n'

        if self.status == 30:
            self.repo.update_client_status(self.client,22,self.timestamp)
            lead = self.repo.get_lead_info(self.client)
            self.answer = f"*Bienvenido de vuelta!* 🤗\nConfirmemos los datos para brindarte una mejor atencion ✅\n\n🏷️ *Nombre:* {lead[0]}\n📱 *Telefono:* {str(lead[2])[3:]}\n📧 *Mail:* {lead[1]}\n\nEnvia\n1️⃣ *Correcto*\n2️⃣ *Modificar*"

        if self.status == 50:
            self.answer = '📱En cualquier momento un *vendedor* se estará comunicando con vos. 👨‍💼 🚗\n\nNormalmente tardamos menos de 30 minutos.⏰\n\n‼️Ah y tene en cuenta que te va a escribir desde un 📱corporativo🏡'

    def validate_mail(self, correo):
        patron = r'^[A-Za-z0-9\s\._%+-]+@[\w\.-]+\.\w+$'
        if re.match(patron, correo):
            return True
        else:
            return False

    def validate_numero(self,numero):
        try:
            numero = int(numero)
            return True
        except:
            return False



"""""

STATUS FLOW

NONE / 0 = No te conozco pido nombre
1 = Tengo tu nombre pido mail
2 = Tengo tu mail pido confirmacion
22 = Tengo confirmacion pido canal
3 = Tengo tu canal pido modelo con opciones
44 = Me pediste 'otro' Modelo
4 = tengo tu modelo.. mando ficha tecnica, pido comentario

5 = tengo todo, mando lead al crm.

Clientes Ya conocidos
30 = Lo saludo (nombre) y arranco pidiendo canal, recategorizo con 2

Clientes esperando ser atendidos
50 = Esperen que alguien se comunique.

"""


class ChatFlowAA():
    def __init__(self,client,msg,timestamp) -> None:
        self.repo = Repository()
        self.msg = msg
        self.timestamp = timestamp
        self.client = client
        self.status = self.get_status()
        self.client_flow_by_status()

    def length_check(self,param):
        if len(self.msg) > param:
            self.answer = f'🚫 Por favor que sean menos de {param} caracteres 🚫️'
            return False
        else:
            return True


    def get_status(self):
        try:
            return self.repo.get_client_status(self.client)[0]
        except:
            return None

    def client_flow_by_status(self):

        if self.status == None or self.status == 0:
            try:
                self.repo.insert_new_client(self.client,self.timestamp)
            except:
                pass

            try:
                modelo = self.msg.split('|')[-1].split('-')[0]
                self.repo.update_client_modelo(self.client,modelo)
                comentario = self.msg.split('|')
                comentario.pop(2)
                print(comentario)
                comentario = ",".join(comentario)
                print(comentario)
                self.repo.update_client_comentario(self.client,comentario)
            except:
                pass

            self.repo.update_client_canal(self.client,3)
            self.repo.update_client_status(self.client,1,self.timestamp)
            self.answer = '🏡¡Hola! Bienvenido a *Espasa AUTO AHORRO* 🚗\n\nUn Asesor Comercial se pondrá en contacto con vos. 👨‍💼\nMientras tanto, te pedimos que nos respondas estas *preguntas* para darte la mejor atención. 🤔\nEn caso que lo necesites, solicitanos una videollamada y te brindamos asesoramiento 100% virtual. 🤳\n*Muchas gracias*\n\n🏷️ ¿Cuál es tu nombre? 🏷️'

        if self.status == 1:
            if self.length_check(60):
                self.repo.update_client_name(self.client,self.msg)
                self.repo.update_client_status(self.client,2,self.timestamp)
                self.answer = '📧 ¿Me decis cual es tu mail? 📧'

        if self.status == 2:
            if self.length_check(110):
                if self.validate_mail(self.msg):
                    self.repo.update_client_mail(self.client,self.msg.lower())
                    self.repo.update_client_status(self.client,22,self.timestamp)
                    lead = self.repo.get_lead_info(self.client)
                    self.answer = f"Como soy un 🤖... ¿Me podes confirmar si estan bien mis 📝?\n\n🏷️ *Nombre:* {lead[0]}\n📱 *Telefono:* {str(lead[2])[3:]}\n📧 *Mail:* {lead[1]}\n\n*Envía*\n1️⃣ Si es correcto\n2️⃣ Si queres modificar"
                else:
                    self.answer = "📧 *Mail invalido* 📧\nRecorda no incluir espacios ni tildes 🚫\nAgregar *@*  e incluir *.com*"

        if self.status == 22:
            if self.validate_numero(self.msg):
                if int(self.msg) ==1:
                    self.repo.update_client_status(self.client,50,self.timestamp)
                    self.answer = '📱En cualquier momento un *vendedor de Auto Ahorro* se estará comunicando con vos. 👨‍💼 🚗\n\nNormalmente tardamos menos de 30 minutos.⏰\n\n‼️Ah y tene en cuenta que te va a escribir desde un 📱corporativo🏡'
                    lead = self.repo.get_lead_info(self.client)
                    LeadAA(lead[0],lead[1],lead[2],lead[3],lead[4])
                elif int(self.msg) ==2:
                    self.repo.update_client_status(self.client,1,self.timestamp)
                    self.answer = '🏷️ ¿Cual es tu nombre y apellido? 🏷️'
                else:
                    self.answer = '🚫 Opcion Invalida 🚫\n\nRecuerda enviar\n1️⃣Confirmar\n2️⃣Modificar'
            else:
                self.answer = "🚫 Mensaje invalido 🚫\n\nRecorda escribir solo el numero con tu respuesta\n\n1️⃣ Confirmar\n2️⃣ Modificar"

        if self.status == 30:
            try:
                modelo = self.msg.split('|')[-1].split('-')[0]
                self.repo.update_client_modelo(self.client,modelo)
                comentario = self.msg.split('|')[0:1]
                comentario = " ".join(comentario)
                self.repo.update_client_comentario(self.client,comentario)
            except:
                pass
            self.repo.update_client_status(self.client,22,self.timestamp)
            lead = self.repo.get_lead_info(self.client)
            self.answer = f"*Bienvenido de vuelta!* 🤗\nConfirmemos los datos para brindarte una mejor atencion ✅\n\n🏷️ *Nombre:* {lead[0]}\n📱 *Telefono:* {str(lead[2])[3:]}\n📧 *Mail:* {lead[1]}\n\nEnvia\n1️⃣ *Correcto*\n2️⃣ *Modificar*"

        if self.status == 50:
            self.answer = '📱En cualquier momento un *vendedor de planes* se estará comunicando con vos. 👨‍💼 🚗\n\nNormalmente tardamos menos de 30 minutos.⏰\n\n‼️Ah y tene en cuenta que te va a escribir desde un 📱corporativo🏡'

    def validate_mail(self, correo):
        patron = r'^[A-Za-z0-9\s\._%+-]+@[\w\.-]+\.\w+$'
        if re.match(patron, correo):
            return True
        else:
            return False

    def validate_numero(self,numero):
        try:
            numero = int(numero)
            return True
        except:
            return False


