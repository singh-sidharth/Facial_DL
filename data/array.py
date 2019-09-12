import numpy as np
from PIL import Image
import glob

path="False_Images/*.jpg"
arr=[]

for image in glob.glob(path):
    img = Image.open(image)
    pixel = np.array(img)
    arr.append(pixel)

arr=np.array(arr)
print(arr)
#To see the image uncomment below code
#pili = Image.fromarray(arr[1])
#pili.save('testrgba.png')