from PIL import Image,ImageDraw,ImageFont

# def add_text(im, text, topleft, size, colour):

#     font = ImageFont.truetype('./fonts/Lobster-Regular.ttf',70)
#     draw = ImageDraw.Draw(im)
#     draw.text(topleft,text,font=font,fill=colour)
#     return im

# if __name__ == "__main__":
#     with Image.open("bg.png") as im:
#         im = add_text(im,"Hello Wolrd", (100,100), 60, (0,0,0))
#         im.save("./saved-images/demotext.png")

img = Image.open("./source-images/temp_ig.png")

font_base = './fonts/Roboto-Medium.ttf'

font_h1 = ImageFont.truetype(font_base,70)
font_h2 = ImageFont.truetype(font_base,40)
font_h3 = ImageFont.truetype(font_base,50)

color_a = (255,255,255)
x = 0
y = 45
tipo_sorteo = 'Dominicial'
fecha_sorteo = '26 de Febrero de 2022'
primer_premio = '0000'
letras = 'AAAA'
serie = 12
folio = 1
segundo_premio = '0000'
tercer_premio = '0000'
draw = ImageDraw.Draw(img)
draw.text((460+x, 0+y), "Sorteo",fill=color_a,font=font_h3)
draw.text((380+x, 60+y), tipo_sorteo,fill=color_a,font=font_h1)
draw.text((350+x, 150+y), fecha_sorteo,fill=color_a,font=font_h2)

draw.text((150+x, 280+y), "Primer Premio",fill=color_a,font=font_h2)
draw.text((700+x, 265+y), primer_premio,fill=color_a,font=font_h1)

draw.text((200+x, 400+y), "Letras",fill=color_a,font=font_h2)
draw.text((490+x, 400+y), "Serie",fill=color_a,font=font_h2)
draw.text((770+x, 400+y), "Folio",fill=color_a,font=font_h2)

draw.text((170+x, 450+y), letras,fill=color_a,font=font_h1)
draw.text((500+x, 450+y), str(serie),fill=color_a,font=font_h1)
draw.text((790+x, 450+y), str(folio),fill=color_a,font=font_h1)

draw.text((150+x, 620+y), "Segundo Premio",fill=color_a,font=font_h2)
draw.text((700+x, 600+y), segundo_premio,fill=color_a,font=font_h1)

draw.text((150+x, 790+y), "Tercer Premio",fill=color_a,font=font_h2)
draw.text((700+x, 770+y), tercer_premio,fill=color_a,font=font_h1)

img.save("./saved-images/post.png")
# Convertir PNG a JPG
img2 = Image.open("./saved-images/post.png")
img_rgb = img2.convert('RGB') 
img_rgb.save("./saved-images/post.jpg")