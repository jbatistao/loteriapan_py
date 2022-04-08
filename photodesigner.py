from PIL import Image,ImageDraw,ImageFont
from datetime import *
import requests
from io import BytesIO

tipo_sorteo = 'Miercolito'
fecha_sort = '20220401'
fecha_sorteo = '9 de abril de 2022'
primer_premio = '0000'
segundo_premio = '0000'
tercer_premio = '0000'
letras = 'AAAA'
serie = 0
folio = 0

urls3img = 'https://infoloteria.s3.amazonaws.com/imgtemp_bot.jpg'                             

response = requests.get(urls3img)

img = Image.open(BytesIO(response.content))

# img = Image.open("./source-images/temp_bot.jpg")

font_base = './fonts/Roboto-Medium.ttf'

font_h1 = ImageFont.truetype(font_base,90)
font_h2 = ImageFont.truetype(font_base,40)
font_h3 = ImageFont.truetype(font_base,50)

color_a = (0,0,0)
x = 0
y = 45
draw = ImageDraw.Draw(img)
draw.text((40+x, 240+y), "Sorteo "+tipo_sorteo,fill=color_a,font=font_h3)
# draw.text((380+x, 60+y), tipo_sorteo,fill=color_a,font=font_h1)
draw.text((40+x, 300+y), fecha_sorteo,fill=color_a,font=font_h2)

draw.text((90+x, 465+y), primer_premio,fill=color_a,font=font_h1)
draw.text((440+x, 465+y), segundo_premio,fill=color_a,font=font_h1)
draw.text((780+x, 465+y), tercer_premio,fill=color_a,font=font_h1)

draw.text((80+x, 730+y), letras,fill=color_a,font=font_h1)
if serie >= 10:
    draw.text((485+x, 730+y), str(serie),fill=color_a,font=font_h1)
else:
    draw.text((520+x, 730+y), str(serie),fill=color_a,font=font_h1)

if folio >= 10:
    draw.text((835+x, 730+y), str(folio),fill=color_a,font=font_h1)
else:
    draw.text((860+x, 730+y), str(folio),fill=color_a,font=font_h1)

img_name = 'post'+fecha_sort+'.jpg'
img_fullroute = 'saved-images/'+img_name

img.save('./saved-images/'+img_name)
print(datetime.now(),' - Imagen guardada')