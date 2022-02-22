# Spider 

import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore

import requests
from bs4 import BeautifulSoup
from datetime import *
import os
# import dotenv
from dotenv import load_dotenv
import base64


dotenvvals = load_dotenv()


firebase_private_key_b64 = base64.b64encode(os.getenv('PRIVATE_KEY'))
firebase_private_key = firebase_private_key_b64.decode(firebase_private_key_b64)


dataCredentials = {
  "type": os.getenv('TYPE'),
  "project_id": os.getenv('PROJECT_ID'),
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": firebase_private_key,
  "client_email": os.getenv('CLIENT_EMAIL'),
  "client_id": os.getenv('CLIENT_ID'),
  "auth_uri": os.getenv('AUTH_URI'),
  "token_uri": os.getenv('TOKEN_URI'),
  "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
  "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
}

# jsoncred = json.dumps(dataCredentials)

# Configuración de Firebase
cred = credentials.Certificate(dataCredentials)

print(cred)

firebase_admin.initialize_app(cred)

db = firestore.client()

# Determinar la fecha actual
hoy = date.today()
ahora = datetime.now()
horario = ahora.strftime('%H:%M:%S')

print('Proceso iniciado')

if (horario >= "00:45:00" and horario <= "14:15:00"):

    dataframe = [
        'http://www.lnb.gob.pa/domleft.php',
        'http://www.lnb.gob.pa/miertab.php',
        'http://www.lnb.gob.pa/gordito.php'
        ]

    datasorteo = ''

    for url in dataframe:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find_all('strong')

    # Colocar variables en 0
        fecha_sorteo = ''
        fecha_sorteo_cap = ''
        num_sorteo = ''
        tipo_sorteo = ''
        primer_premio = ''
        primer_premio_prov = ''
        letras = ''
        serie = ''
        folio = ''
        segundo_premio = ''
        segundo_premio_prov = ''
        tercer_premio = ''
        tercer_premio_prov = ''

        # Coloca los valores obtenidos por BS

        # Fecha del sorteo
        fecha_sorteo = data[0].text
        fecha_sorteo = fecha_sorteo.strip()
        print('Fecha Sorteo: ',fecha_sorteo)

        # Fecha del sorteo
        # fecha_sorteo = data[0].text
        fecha_sorteo_len = len(fecha_sorteo)
        fecha_sorteo_dia = fecha_sorteo[0:2]
        print(fecha_sorteo_dia)
        fecha_sorteo_ano = fecha_sorteo[len(fecha_sorteo)-4:]
        fecha_sorteo_mes = fecha_sorteo[6:len(fecha_sorteo)-8]
        
        if fecha_sorteo_mes == 'Enero':
            fecha_sorteo_mesnum = 1
        if fecha_sorteo_mes == 'Febrero':
            fecha_sorteo_mesnum = 2
        if fecha_sorteo_mes == 'Marzo':
            fecha_sorteo_mesnum = 3
        if fecha_sorteo_mes == 'Abril':
            fecha_sorteo_mesnum = 4
        if fecha_sorteo_mes == 'Mayo':
            fecha_sorteo_mesnum = 5
        if fecha_sorteo_mes == 'Junio':
            fecha_sorteo_mesnum = 6
        if fecha_sorteo_mes == 'Julio':
            fecha_sorteo_mesnum = 7
        if fecha_sorteo_mes == 'Agosto':
            fecha_sorteo_mesnum = 8
        if fecha_sorteo_mes == 'Septiembre':
            fecha_sorteo_mesnum = 9
        if fecha_sorteo_mes == 'Octubre':
            fecha_sorteo_mesnum = 10
        if fecha_sorteo_mes == 'Noviembre':
            fecha_sorteo_mesnum = 11
        if fecha_sorteo_mes == 'Diciembre':
            fecha_sorteo_mesnum = 12

        print(fecha_sorteo)
    
        fecha_sorteo_cap = datetime(int(fecha_sorteo_ano),int(fecha_sorteo_mesnum),int(fecha_sorteo_dia))
        fecha_sort = fecha_sorteo_cap.strftime("%Y%m%d")
        # print('Fecha Sorteo: ',fecha_sort)

        # No de sorteo
        num_sorteo = data[2].text.replace(":","")
        num_sorteo = int(num_sorteo.strip())
        # print('Sorteo: ',num_sorteo)


        if url == 'http://www.lnb.gob.pa/domleft.php':
            tipo_sorteo = 'Dominical'
        if url == 'http://www.lnb.gob.pa/miertab.php':
            tipo_sorteo = 'Miercolito'
        if url == 'http://www.lnb.gob.pa/gordito.php':
            tipo_sorteo = 'Gordito del Zodiaco'
        
        # print('Tipo de sorteo: ',tipo_sorteo)

        # Primer Premio
        primer_premio = data[4].text
        # print('Primer Premio: ',primer_premio)

        # Letras del Primer Premio
        letras = data[7].text
        # print('Letras: ',letras)

        # Serie del Primer Premio
        serie = int(data[9].text)
        # print('Serie: ',serie)

        # Serie del Primer Premio
        folio = int(data[11].text)
        # print('Folio: ',folio)

        # Segundo Premio
        segundo_premio = data[13].text
        # print('Segundo Premio: ',segundo_premio)

        # Completa los valores diferentes entre los sorteos regulares y el gordito

        if url != 'http://www.lnb.gob.pa/gordito.php':

            # Provincia donde jugó el Primer Premio
            primer_premio_prov = data[5].text
            # print('Primer Premio Provincia: ',primer_premio_prov)

            # Provincia donde jugó el Segundo Premio
            segundo_premio_prov = data[14].text
            # print('Segundo Premio Provincia: ',segundo_premio_prov)

            # Tercer Premio
            tercer_premio = data[16].text
            # print('Tercer Premio: ',tercer_premio)

            # Provincia donde jugó el Tercer Premio
            tercer_premio_prov = data[17].text
            # print('Tercer Premio Provincia: ',tercer_premio_prov)
        
        if url == 'http://www.lnb.gob.pa/gordito.php':

            # Tercer Premio
            tercer_premio = data[15].text
            # print('Tercer Premio: ',tercer_premio)

        # Crea el objeto que se grabará

        datasorteo = {
            'fecha_sorteo': fecha_sorteo,
            'fecha_sort': fecha_sort,
            'num_sorteo': num_sorteo,
            'tipo_sorteo': tipo_sorteo,
            'primer_premio': primer_premio,
            'primer_premio_prov': primer_premio_prov,
            'letras': letras,
            'serie': serie,
            'folio': folio,
            'segundo_premio': segundo_premio,
            'segundo_premio_prov': segundo_premio_prov,
            'tercer_premio': tercer_premio,
            'tercer_premio_prov': tercer_premio_prov,
            'creado': ahora
        }

        # Verifica si el número y tipo de sorteo existe 
        docs = db.collection(u'sorteos').where(u'fecha_sort', u'==', fecha_sort).get()
        print('Docs: ',docs)

        # Graba el documento si no existe en la BD
        if docs == []:
            print('No existe')
            doc_ref = db.collection(u'sorteos').document()
            doc_ref.set(datasorteo)
else:
    print('No es hora todavía')