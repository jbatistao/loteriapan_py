import cv2
import numpy as np
import glob
from PIL import Image, ImageDraw, ImageFont

img_array = []
for filename in glob.glob('./source-images/video/*.jpg'):
    img = cv2.imread(filename)
    print(img)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

# https://www.youtube.com/watch?v=5_4vvSSFoY8
# https://www.youtube.com/watch?v=y4v6K3-s3mE
# https://www.youtube.com/watch?v=1alk6t8EIy0
# https://www.youtube.com/watch?v=CLNr_ClJr2o
# https://www.youtube.com/watch?v=2h8e0tXHfk0
# https://www.youtube.com/watch?v=NzLqRYVYFME
# https://www.stackbuilders.com/blog/python-video-generation/
# https://sonsuzdesign.blog/2021/04/06/rendering-responsive-text-on-video-using-python/
# https://www.geeksforgeeks.org/python-opencv-write-text-on-video/
# https://www.tutorialexample.com/python-moviepy-convert-images-png-jpg-to-video-python-moviepy-tutorial/
# https://zulko.github.io/moviepy/examples/moving_letters.html