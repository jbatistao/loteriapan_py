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

img = Image.open("bg.png")

font_h1 = ImageFont.truetype('./fonts/Roboto-Medium.ttf',70)
font_h2 = ImageFont.truetype('./fonts/Roboto-Medium.ttf',40)

color_a = (0,0,0)
i = 70
draw = ImageDraw.Draw(img)
draw.text((265, 110+i), "Sorteo Dominical",fill=color_a,font=font_h1)
draw.text((250, 180+i), "Domingo 23 de Febrero de 2022",fill=color_a,font=font_h2)

draw.text((400, 280+i), "Primer Premio",fill=color_a,font=font_h2)
draw.text((450, 320+i), "0000",fill=color_a,font=font_h1)

draw.text((200, 420+i), "Letras",fill=color_a,font=font_h2)
draw.text((480, 420+i), "Serie",fill=color_a,font=font_h2)
draw.text((770, 420+i), "Folio",fill=color_a,font=font_h2)

draw.text((170, 460+i), "AAAA",fill=color_a,font=font_h1)
draw.text((490, 460+i), "10",fill=color_a,font=font_h1)
draw.text((790, 460+i), "1",fill=color_a,font=font_h1)

draw.text((390, 560+i), "Segundo Premio",fill=color_a,font=font_h2)
draw.text((450, 600+i), "0000",fill=color_a,font=font_h1)

draw.text((420, 700+i), "Tercer Premio",fill=color_a,font=font_h2)
draw.text((450, 740+i), "0000",fill=color_a,font=font_h1)


img.save("./saved-images/demotext.png")