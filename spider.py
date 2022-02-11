# import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
from bs4 import BeautifulSoup
from datetime import *
from calendar import monthrange

# def spider():
# Configuración de Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://loteriapanama-b70b9-default-rtdb.firebaseio.com/'})

# Determinar qué día es el sorteo
# Determinar qué día es el sorteo

# start = 'http://www.lnb.gob.pa/domleft.php'
# start = "http://www.lnb.gob.pa/miertab.php"
# start = 'http://www.lnb.gob.pa/gordito.php'


# Determinar la fecha actual
hoy = date.today()
ahora = datetime.now()
ahora = ahora.strftime('%H:%M:%S %p')
dataframe = ''
# hoy = datetime.date(int(hoy.year),int(hoy.month),int(hoy.day))

# Determinar si hoy es miércoles o domingo
dia_sorteo = hoy.isoweekday()

fecha_ini = date(int(hoy.year), int(hoy.month), 1)
month_days = monthrange(int(hoy.year), int(hoy.month))[1] # Calcula el número de días de un mes
fecha_end = date(int(hoy.year), int(hoy.month), month_days)
count = 0
fechas_sorteo_semanal = []

for d_ord in range(fecha_ini.toordinal(), fecha_end.toordinal()):
    d = date.fromordinal(d_ord)
    if (d.isoweekday() == 3 or d.isoweekday() == 5):
        fechas_sorteo_semanal.append(d)
        count += 1

validar_fecha_semanal = hoy in fechas_sorteo_semanal

if (validar_fecha_semanal == True and ahora >= "01:45:00 PM" and ahora >= "02:15:00 PM"):
    if (dia_sorteo == 3):
        dataframe = 'http://www.lnb.gob.pa/miertab.php'
        print("miercoles")
    if (dia_sorteo == 5):
        dataframe = 'http://www.lnb.gob.pa/domleft.php'
        print("domingo")

# Validar si hoy es el último viernes del mes
month_days = monthrange(int(hoy.year), int(hoy.month))[1] # Calcula el número de días de un mes
count_m = 0
fechas_sorteo_month = []

for d_ord in range(fecha_ini.toordinal(), fecha_end.toordinal()):
    d = date.fromordinal(d_ord)
    if (d.isoweekday() == 5):
        fechas_sorteo_month.append(d)
        count_m += 1

last_friday = fechas_sorteo_month[len(fechas_sorteo_month)-1]

# validar_fecha_gordito = hoy in fechas_sorteo_month

if (hoy == last_friday  and ahora >= "11:15:00 AM" and ahora >= "02:15:00 PM"):
    if (dia_sorteo == 5):
        dataframe = 'http://www.lnb.gob.pa/gordito.php'
        print("gordito")

# if (validar_fecha_semanal == False and hoy != last_friday):
#     dataframe = ''

url = dataframe


# Extraer info

datasorteo = ''
if (url != ''):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find_all('strong')

    if (dia_sorteo == 3 or dia_sorteo == 7):
        # No de sorteo
        sorteo_num = data[2].text.replace(":","")
        sorteo = sorteo_num.strip()
        # print(sorteo)

        # Primer Premio
        premio1 = data[4].text
        # print(premio1)

        # Provincia donde jugó el Primer Premio
        premio1_provincia = data[5].text

        # Letras del Primer Premio
        letras = data[7].text

        # Serie del Primer Premio
        serie = data[9].text

        # Folio del Primer Premio
        folio = data[11].text

        # Segundo Premio
        premio2 = data[13].text

        # Provincia donde jugó el Segundo Premio
        premio2_provincia = data[14].text

        # Tercer Premio
        premio3 = data[16].text

        # Provincia donde jugó el Tercer Premio
        premio3_provincia = data[17].text

        if (dia_sorteo == 3):
            tipo = 'Miércoles'
        else:
            tipo = 'Domingo'

        datasorteo = {
        'fecha': hoy,
        'sorteo':sorteo,
        'tipo': tipo,
        'primer': premio1,
        'provincia1': premio1_provincia,
        'letras': letras,
        'serie': serie,
        'folio': folio,
        'segundo': premio2,
        'provincia2': premio2_provincia,
        'tercer': premio3,
        'provincia3': premio3_provincia,
        'ahora': str(hoy)
        }
    
    if (dia_sorteo == 5):
        # No de sorteo
        sorteo_num = data[2].text.replace(":","")
        sorteo = sorteo_num.strip()
        # print(sorteo)

        # Primer Premio
        premio1 = data[4].text.replace("\n","")
        # print(premio1)

        # Provincia donde jugó el Primer Premio
        premio1_provincia = data[5].text

        # Letras del Primer Premio
        letras = data[7].text

        # Serie del Primer Premio
        serie = data[9].text

        # Folio del Primer Premio
        folio = data[11].text

        # Segundo Premio
        premio2 = data[13].text

        # Provincia donde jugó el Segundo Premio
        # premio2_provincia = data[14].text

        # Tercer Premio
        # premio3 = data[16].text

        # Provincia donde jugó el Tercer Premio
        # premio3_provincia = data[17].text

        datasorteo = {
        'fecha': str(hoy),
        'sorteo':sorteo,
        'tipo':'Gordito',
        'primer': premio1,
        # 'provincia1': '',
        'letras': letras,
        'serie': serie,
        'folio': folio,
        # 'segundo': '',
        # 'provincia2': '',
        # 'tercer': '',
        # 'provincia3': '',
        'ahora': str("hoy")
        }

# Guardar info
if (datasorteo != ''):
    ref = db.reference('/Sorteos')
    ref.push(datasorteo)




    # # hoy = datetime.now()
    # current_time = hoy.strftime("%H:%M:%S")
    # current_date = hoy.strftime("%Y-%m-%d")

    # # Trigger scraper function everyday on 12 AM
    # if current_time == "02:00:00" and current_date == '2022-02-11': 
    #     spider()


