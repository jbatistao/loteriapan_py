# Spider 

import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore

from bs4 import BeautifulSoup

from PIL import Image,ImageDraw,ImageFont

import facebook

from datetime import *
import requests
import os
import time

import boto3

from dotenv import load_dotenv

dotenvvals = load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')

s3 = boto3.resource('s3')
print("Conectando al bucket...")

dataCredentials = {
  "type": os.getenv('TYPE'),
  "project_id": os.getenv('PROJECT_ID'),
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
  "client_email": os.getenv('CLIENT_EMAIL'),
  "client_id": os.getenv('CLIENT_ID'),
  "auth_uri": os.getenv('AUTH_URI'),
  "token_uri": os.getenv('TOKEN_URI'),
  "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
  "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
}

# Facebook SDK
token = os.getenv('FB_TOKEN')
graph = facebook.GraphAPI(token)

# Configuración de Firebase
cred = credentials.Certificate(dataCredentials)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Inicio del procesamiento
print(datetime.now(),' - Proceso iniciado')

# Determinar la fecha actual
hoy = date.today()
ahora = datetime.now()
horario = ahora.strftime('%H:%M:%S')

# Verifica si es hora de correr la consulta
# if (horario >= "00: 00:01" and horario <= "23:59:00"):
if (horario >= "13:45:00" and horario <= "14:45:00"):

    ano_hoy = ahora.strftime('%Y')
    mes_hoy = ahora.strftime('%m')

    # Periodo que buscará
    anos = [ano_hoy]
    mes = [mes_hoy]

    # Recorrido
    ia = 0
    im = 0
    for a in anos:
        # print('ia: ',ia)
        im = 0
        for m in mes:
            url = 'http://www.lnb.gob.pa/numerosjugados.php?tiposorteo=T&ano='+anos[ia]+'&meses='+mes[im]+'&Consultar=Buscar'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            data = soup.find_all('strong')
        
            # Verifica si hay datos de sorteos
            if len(data) > 11:

                # Coloca los valores obtenidos por BS
                i = 10
                dias = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado']
                meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

                data_len = len(data)
                for d in data:
                    if i < data_len:
                        try:
                            # Define campos según fecha del sorteo
                            tipo_sorteo = data[i].text
                            if tipo_sorteo == 'Intermedio':
                                tipo_sorteo = 'Miercolito'
                            if tipo_sorteo == 'Dominical':
                                tipo_sorteo = 'Dominical'
                            if tipo_sorteo == 'Zodiaco':
                                tipo_sorteo = 'Gordito del Zodiaco'
                            if tipo_sorteo == 'Extraordinaria':
                                tipo_sorteo = 'Extraordinario'

                            fecha_sorteo = datetime(int(data[i+1].text[-4:]),int(data[i+1].text[3:5]),int(data[i+1].text[:2]))

                            fecha_sorteo_cap = datetime(int(data[i+1].text[-4:]),int(data[i+1].text[3:5]),int(data[i+1].text[:2]))
                            fecha_sorteo = str(fecha_sorteo.day) + ' de ' + meses[int(fecha_sorteo.strftime("%m"))-1] + ' de ' + fecha_sorteo.strftime("%Y")
                            fecha_sort = fecha_sorteo_cap.strftime("%Y%m%d")
                            primer_premio = data[i+2].text
                            letras = data[i+3].text
                            serie = int(data[i+4].text)
                            folio = int(data[i+5].text)
                            segundo_premio = data[i+6].text
                            tercer_premio = data[i+7].text
                            creado = ahora

                            print(tipo_sorteo,fecha_sorteo,fecha_sorteo_cap,fecha_sort,primer_premio,letras,serie,folio,segundo_premio,tercer_premio)
                            
                            datasorteo = {
                                'fecha_sorteo': fecha_sorteo,
                                'fecha_sort': fecha_sort,
                                'tipo_sorteo': tipo_sorteo,
                                'primer_premio': primer_premio,
                                'letras': letras,
                                'serie': serie,
                                'folio': folio,
                                'segundo_premio': segundo_premio,
                                'tercer_premio': tercer_premio,
                                'creado': ahora
                            }
                            
                            # Verifica los datos están completos
                            if (tipo_sorteo != 'Gordito del Zodiaco' and len(tercer_premio) == 4) or (tipo_sorteo == 'Gordito del Zodiaco' and len(tercer_premio) == 2):
                                # Verifica si el número y tipo de sorteo existe 
                                docs = db.collection(u'sorteos').where(u'fecha_sort', u'==', fecha_sort).get()

                            # Verifica si el número y tipo de sorteo existe
                            if docs == []: 
                                print(datetime.now(),' - No existe... debe guardarse')                             

                                img = Image.open("./source-images/temp_bot.jpg")

                                font_base = './fonts/Roboto-Medium.ttf'

                                font_h1 = ImageFont.truetype(font_base,70)
                                font_h2 = ImageFont.truetype(font_base,40)
                                font_h3 = ImageFont.truetype(font_base,50)

                                color_a = (255,255,255)
                                x = 0
                                y = 45
                                draw = ImageDraw.Draw(img)
                                draw.text((460+x, 0+y), "Sorteo",fill=color_a,font=font_h3)
                                draw.text((380+x, 60+y), tipo_sorteo,fill=color_a,font=font_h1)
                                draw.text((350+x, 150+y), fecha_sorteo,fill=color_a,font=font_h2)

                                draw.text((150+x, 280+y), "Primer Premio",fill=color_a,font=font_h2)
                                draw.text((700+x, 265+y), primer_premio,fill=color_a,font=font_h1)

                                draw.text((200+x, 400+y), "Letras",fill=color_a,font=font_h2)
                                draw.text((490+x, 400+y), "Serie",fill=color_a,font=font_h2)
                                draw.text((770+x, 400+y), "Folio",fill=color_a,font=font_h2)

                                draw.text((170+x, 450+y), letras,fill=color_a,font=font_h1)
                                draw.text((500+x, 450+y), str(serie),fill=color_a,font=font_h1)
                                draw.text((790+x, 450+y), str(folio),fill=color_a,font=font_h1)

                                draw.text((150+x, 620+y), "Segundo Premio",fill=color_a,font=font_h2)
                                draw.text((700+x, 600+y), segundo_premio,fill=color_a,font=font_h1)

                                draw.text((150+x, 790+y), "Tercer Premio",fill=color_a,font=font_h2)
                                draw.text((700+x, 770+y), tercer_premio,fill=color_a,font=font_h1)

                                img_name = 'post'+fecha_sort+'.jpg'
                            img_fullroute = '.\source-images\\'+fecha_sort+'.jpg'

                            img.save('./saved-images/'+img_name)
                            print(datetime.now(),' - Imagen guardada')

                            time.sleep(3)
                            
                            urls3 = 'https://infoloteria.s3.amazonaws.com/'+img_name

                            # rr = os.path()

                            s3.Object('infoloteria',img_name).upload_file(img_fullroute)
                            print(datetime.now(),' - Publicada en S3!')
                            time.sleep(5)

                            msg_regular = 'En el soteo ' + tipo_sorteo + ' de ' + fecha_sorteo + ' los números ganadores fueron: ' + '\n' + 'Primer Premio: ' + primer_premio + '\n' + 'Letras: ' + letras + '\n' + 'Serie: ' + str(serie) + '\n' + 'Folio: ' + str(folio) + '\n' + 'Segundo Premio: ' + segundo_premio + '\n' + 'Tercer Premio: ' + tercer_premio

                            fb_rx = graph.put_object('102607489042095','photos',url=urls3,caption=msg_regular)
                            print(datetime.now(),' - Publicada en FB!')

                            fb_rx_a = graph.put_object('17841452380183145','media',image_url=urls3,caption=msg_regular)
                            # print(fb_rx_a)

                            fb_rx_b = graph.put_object('17841452380183145','media_publish',creation_id=fb_rx_a['id'])
                            # print(fb_rx_b)

                            print(datetime.now(),' - Publicada en IG!')

                            os.remove('./saved-images/'+img_name)
                            print(datetime.now(),' - Se han borrado las imagenes!')

                                 
                                doc_ref = db.collection(u'sorteos').document()
                                doc_ref.set(datasorteo)
                                print(datetime.now(),' - Registro creado en Firebase')
                            
                            i = i+8
                            # print('i: ',i)
                        except IndexError:
                            pass
                        else:
                            print(datetime.now(),' - No exception occurred')

                im = im+1
        
        ia=ia+1
    
    print(datetime.now(),' - No hay más datos')

else:
    print(datetime.now(),' - Estamos fuera de horario')    