import requests
import os
from dotenv import load_dotenv

dotenvvals = load_dotenv()

key = os.getenv('API_KEY')

pload = {
		"fecha_sorteo": '18 de Abril de 2022',
	    "fecha_sort": '20220418',
	    "tipo": 'Extraordinario',
		"primer_premio": '24001',
		"segundo_premio": "9999",
		"tercer_premio": "8888",
		"letras": "AAAB",
		"serie": 10,
		"folio": 0
	}
# pload = {
# 		"fecha_sorteo": '18 de Abril de 2022',
# 	    "fecha_sort": '20220418',
# 	    "tipo": 'Extraordinario',
# 		"primer_premio": '24004',
# 		"segundo_premio": '41828',
# 		"tercer_premio": '16739',
# 		"letras": 'AABC',
# 		"serie": 1,
# 		"folio": 4
# 	}

headers_content = { "Authorization" : key }

r = requests.post('https://notiloteria-api.herokuapp.com/api/sorteo/',json = pload)
print(r)
print(r.json())
