# Spider 

import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore

import requests
from bs4 import BeautifulSoup
from datetime import *
# import pandas as pd

# Configuración de Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Determinar la fecha actual
hoy = date.today()
ahora = datetime.now()
horario = ahora.strftime('%H:%M:%S')

# anos = ['2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2011','2010']
# mes = ['01','02','03','04','05','06','07','08','09','10','11','12']

anos = ['2021']
mes = ['12']


ia = 0
im = 0
for a in anos:
    print('ia: ',ia)
    im = 0
    for m in mes:
        url = 'http://www.lnb.gob.pa/numerosjugados.php?tiposorteo=T&ano='+anos[ia]+'&meses='+mes[im]+'&Consultar=Buscar'
        print(url)    
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find_all('strong')
      

        # Coloca los valores obtenidos por BS
        i = 10
        dias = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado']
        meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']


        for d in data:
            try:
                # Fecha del sorteo
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
                    'num_sorteo': '',
                    'tipo_sorteo': tipo_sorteo,
                    'primer_premio': 1234,
                    'primer_premio': primer_premio,
                    'primer_premio_prov': '',
                    'letras': letras,
                    'serie': serie,
                    'folio': folio,
                    'segundo_premio': segundo_premio,
                    'segundo_premio_prov': '',
                    'tercer_premio': tercer_premio,
                    'tercer_premio_prov': '',
                    'creado': ahora
                }

                # Verifica si el número y tipo de sorteo existe 
                docs = db.collection(u'sorteos').where(u'fecha_sort', u'==', fecha_sort).get()
                print('Docs: ',docs)

                # Verifica si el número y tipo de sorteo existe
                if docs == []:
                    print('No existe') 
                    doc_ref = db.collection(u'sorteos').document()
                    doc_ref.set(datasorteo)                                 

                i = i+8
                print('i: ',i)
            except IndexError:
                pass
        #  match /{document=**} {
        im = im+1
        print('im: ',im)
    
    ia=ia+1
    print('ia: ',ia)