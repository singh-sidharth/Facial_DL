#Commented expressions are used to return the resized images to the caller
import os
import cv2

def init():
    process_images("Original_Images",r".\Processed_Images",(100,100))

def process_images(folder,newpath,size):
    #images=[]

    #Create a folder to hold the processed images
    if not os.path.exists(newpath):
            os.makedirs(newpath)

    for filename in os.listdir(folder):
        #Read images
        image = cv2.imread(os.path.join(folder,filename), cv2.IMREAD_GRAYSCALE)
        if image is not None:
            img=cv2.resize(image,size)
            cv2.imwrite(os.path.join(newpath,filename), img)
            #images.append(img)
    #return images

if __name__ == "__main__":
    init()
