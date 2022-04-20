import requests
import os
from dotenv import load_dotenv

dotenvvals = load_dotenv()

key = os.getenv('API_KEY')

pload = {
		"fecha_sorteo": "2022-04-11",
	    "fecha_sort": "20220411",
	    "tipo": "gordito",
		"primer_premio": "9999",
		"segundo_premio": "9999",
		"tercer_premio": "8888",
		"letras": "AAAB",
		"serie": 10,
		"folio": 0
	}

headers_content = { "Authorization" : key }

r = requests.post('https://notiloteria-api.herokuapp.com/api/sorteo/',json = pload)
print(r.status_code)
print(r.json())
