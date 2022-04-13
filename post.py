import requests
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
r = requests.post('https://notiloteria-api.herokuapp.com/api/sorteo/',json = pload)
print(r.status_code)
print(r.json())
