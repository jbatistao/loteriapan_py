from email import message
import facebook
import os

from dotenv import load_dotenv

dotenvvals = load_dotenv()

fb_token = os.getenv('FB_TOKEN')



# InfoLot_FB = "102607489042095"
# InfoLot_IGBA = "17841452380183145"
# profilePage_IG = "52345162006"
 
def main():
    token = fb_token
    # token = 'EAAOUA1lyRtUBAK0Ih5Yix1uuaIT9xTqcGkjKZA2kbwq0FCtxiNwSQZBFUmTUrHi1fOKEJurZAZCobZBE7LPZCHG1hks53933XkIObCxDtj9eBYMJYZByOsDhUOh2eS49GMLittgeHZAO0Hoo81UiLeaGXhnyrJMUWozPYshc0wWV0NPjakusKxXJ'
    graph = facebook.GraphAPI(token)

    
    # Obtener el id del usuario
    # Resultado: {'name': 'Infoloteria', 'id': '102607489042095'}
    # fb_rx = graph.get_object('me')
    # print(fb_rx)

    # Publicar en una página de FB con un link
    # Resultado: {'id': '102607489042095_103103765659134'}
    # fb_rx = graph.put_object('102607489042095','feed',message='Esta es una prueba 222',link='http://www.facebook.com')
    # print(fb_rx)

    # Publicar en una página de FB con una foto
    # Resultado: {'id': '103119062324271', 'post_id': '102607489042095_103119062324271'}
    fb_rx = graph.put_object('102607489042095','photos',url='https://cdn.icon-icons.com/icons2/1948/PNG/512/free-30-instagram-stories-icons26_122574.png',caption='es una prueba con foto y 😀')
    print(fb_rx)
    


    # Publicar en una página de IG - Con texto y Emoji
    # Resultado: {'id': '102607489042095_103103765659134'}
    # fb_rx_a = graph.put_object('17841452380183145','media',image_url='https://cdn.icon-icons.com/icons2/1948/PNG/512/free-30-instagram-stories-icons26_122574.png',caption='es una prueba con foto y 😀')
    # fb_rx_a = graph.put_object('17841452380183145','media',image_url='https://loteriapan.herokuapp.com/saved-images/post.png',caption='es una prueba con foto y 😀')
    # print(fb_rx_a)

    # fb_rx_b = graph.put_object('17841452380183145','media_publish',creation_id=fb_rx_a['id'],caption='es una prueba con foto y 😀')
    # print(fb_rx_b)
 
if __name__ == '__main__':
    main()

print('Success!')



# <iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fpermalink.php%3Fstory_fbid%3D102900885679422%26id%3D102607489042095&show_text=true&width=500" width="500" height="590" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>