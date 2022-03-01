# Spider 

import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore

import requests
from bs4 import BeautifulSoup
from datetime import *
import os
from PIL import Image,ImageDraw,ImageFont

from dotenv import load_dotenv

dotenvvals = load_dotenv()

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

# Configuración de Firebase
cred = credentials.Certificate(dataCredentials)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Inicio del procesamiento
print('Proceso iniciado')

# Determinar la fecha actual
hoy = date.today()
ahora = datetime.now()
horario = ahora.strftime('%H:%M:%S')

# Verifica si es hora de correr la consulta
if (horario >= "00:00:01" and horario <= "23:59:00"):
# if (horario >= "13:45:00" and horario <= "14:30:00"):

    ano_hoy = ahora.strftime('%Y')
    mes_hoy = ahora.strftime('%m')

    # Periodo que buscará
    anos = [ano_hoy]
    mes = ['02']

    # Recorrido
    ia = 0
    im = 0
    for a in anos:
        print('ia: ',ia)
        im = 0
        for m in mes:
            url = 'http://www.lnb.gob.pa/numerosjugados.php?tiposorteo=T&ano='+anos[ia]+'&meses='+mes[im]+'&Consultar=Buscar'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            data = soup.find_all('strong')
        

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
                            print('No existe') 
                            doc_ref = db.collection(u'sorteos').document()
                            doc_ref.set(datasorteo)                                 

                            img = Image.open("./source-images/bg.png")

                            font_h1 = ImageFont.truetype('./fonts/Roboto-Medium.ttf',70)
                            font_h2 = ImageFont.truetype('./fonts/Roboto-Medium.ttf',40)

                            color_a = (0,0,0)
                            x = 20
                            y = 100
                            draw = ImageDraw.Draw(img)
                            draw.text((440+x, 65+y), "SORTEO",fill=color_a,font=font_h2)
                            draw.text((360+x, 110+y), tipo_sorteo,fill=color_a,font=font_h1)
                            draw.text((320+x, 180+y), fecha_sorteo,fill=color_a,font=font_h2)

                            draw.text((400+x, 280+y), "Primer Premio",fill=color_a,font=font_h2)
                            draw.text((450+x, 320+y), primer_premio,fill=color_a,font=font_h1)

                            draw.text((200+x, 420+y), "Letras",fill=color_a,font=font_h2)
                            draw.text((480+x, 420+y), "Serie",fill=color_a,font=font_h2)
                            draw.text((770+x, 420+y), "Folio",fill=color_a,font=font_h2)

                            draw.text((170+x, 460+y), letras,fill=color_a,font=font_h1)
                            draw.text((490+x, 460+y), str(serie),fill=color_a,font=font_h1)
                            draw.text((790+x, 460+y), str(folio),fill=color_a,font=font_h1)

                            draw.text((390+x, 560+y), "Segundo Premio",fill=color_a,font=font_h2)
                            draw.text((450+x, 600+y), segundo_premio,fill=color_a,font=font_h1)

                            draw.text((420+x, 700+y), "Tercer Premio",fill=color_a,font=font_h2)
                            draw.text((450+x, 740+y), tercer_premio,fill=color_a,font=font_h1)

                            img.save("./saved-images/post.png")
                        
                        i = i+8
                        print('i: ',i)
                    except IndexError:
                        pass
                    else:
                        print ('No exception occurred')
                else:
                        print ('No hay más datos')

            im = im+1
        
        ia=ia+1
else:
    print('Estamos fuera de horario')     