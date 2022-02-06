import requests 
from bs4 import BeautifulSoup
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://loteriapanama-b70b9-default-rtdb.firebaseio.com/'})


# Determinar qué día es el sorteo
hoy = datetime.datetime.now()
diasorteo = datetime.date(int(hoy.year),int(hoy.month),int(hoy.day))
wdia = diasorteo.weekday()


if wdia == 0:
    print('lunes')
if wdia == 1:
    print('martes')
if wdia == 2:
    print('miércoles')
start = 'http://www.lnb.gob.pa/miertab.php'
if wdia == 3:
    print('jueves')
if wdia == 4:
    print('viernes')
if wdia == 5:
    print('sábado')
if wdia == 6:
    print('domingo')
start = 'http://www.lnb.gob.pa/domleft.php'
if wdia < 0 or wdia > 6:
    print('error')


# start = 'http://www.lnb.gob.pa/domleft.php'
# start = 'http://www.lnb.gob.pa/gordito.php'
# start = "http://www.lnb.gob.pa/miertab.php"
URL = start

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
data = soup.find_all('strong')
fecha = data[0].text.strip()
dia = (fecha[0:2]).strip()

ano = fecha[len(fecha)-4:len(fecha)]

mes = hoy.month
# print(ano)
# print(dia)
# print(hoy.month)

x = len(str(hoy.month))
# print(x)

# hoy2 = '0'+str(hoy.month)

if(x == 1):
    hoy2 = '0'+str(hoy.month)
else:
    hoy2 = str(hoy.month)

# print('hoy', hoy)
# d = int(dia)
# print('dia',dia)

sorteo_fechax = diasorteo
sorteo_day = sorteo_fechax.weekday

# print(sorteo_fechax)

# No de sorteo
sorteo_num = data[2].text.replace(":","")
sorteo = sorteo_num.strip()
# print(sorteo)

# Primer Premio
premio1 = data[4].text
# print(premio1)

# Provincia donde jugó el Primer Premio
premio1_provincia = data[5].text
# print(premio1_provincia)

# Letras del Primer Premio
letras = data[7].text
# print(letras)

# Serie del Primer Premio
serie = data[9].text
# print(serie)

# Folio del Primer Premio
folio = data[11].text
# print(folio)

# Segundo Premio
premio2 = data[13].text
# print(premio2)

# Provincia donde jugó el Segundo Premio
premio2_provincia = data[14].text
# print(premio2_provincia)

# Tercer Premio
premio3 = data[16].text
# print(premio3)

# Provincia donde jugó el Tercer Premio
premio3_provincia = data[17].text
# print(premio3_provincia)



ref = db.reference('/Sorteos')
ref.push({
    'fecha': str(ano) + '-' + str(hoy2) + '-' + str(dia),
    'sorteo':sorteo,
    'tipo':'Dominical',
    'primer': premio1,
    'provincia1': premio1_provincia,
    'letras': letras,
    'serie': serie,
    'folio': folio,
    'segundo': premio2,
    'provincia2': premio2_provincia,
    'tercer': premio3,
    'provincia3': premio3_provincia 
    })
