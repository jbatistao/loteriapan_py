# Spider 

import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore

import requests
from bs4 import BeautifulSoup
from datetime import *

# Configuración de Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Determinar la fecha actual
hoy = date.today()
ahora = datetime.now()
horario = ahora.strftime('%H:%M:%S')

if (horario >= "13:45:00" and horario <= "14:15:00"):

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
        # print('Fecha Sorteo: ',fecha_sorteo)

        # Fecha del sorteo
        # fecha_sorteo = data[0].text
        fecha_sorteo_len = len(fecha_sorteo)
        fecha_sorteo_dia = fecha_sorteo[0:2]
        fecha_sorteo_ano = fecha_sorteo[len(fecha_sorteo)-4:]
        fecha_sorteo_mes = fecha_sorteo[6:len(fecha_sorteo)-8]
        
        if fecha_sorteo_mes == 'Enero':
            fecha_sorteo_mesnum = 0
        if fecha_sorteo_mes == 'Febrero':
            fecha_sorteo_mesnum = 1


    
        fecha_sorteo_capturada = datetime(int(fecha_sorteo_ano),int(fecha_sorteo_mesnum),int(fecha_sorteo_dia))
        # print('Fecha Sorteo: ',fecha_sorteo)

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
            'fecha_sorteo_cap': fecha_sorteo_capturada,
            'fecha_sort': fecha_sorteo_capturada.strftime("%Y%m%d"),
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
        docs = db.collection(u'sorteos').where(u'num_sorteo', u'==', num_sorteo).where(u'tipo_sorteo', u'==', tipo_sorteo).get()
        print('Docs: ',docs)

        # Graba el documento si no existe en la BD
        if docs == []:
            print('No existe')
            doc_ref = db.collection(u'sorteos').document()
            doc_ref.set(datasorteo)