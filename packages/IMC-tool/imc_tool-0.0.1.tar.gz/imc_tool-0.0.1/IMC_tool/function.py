from readimc import MCDFile, TXTFile
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
from PIL import Image
import skimage as ski
import os
import cv2
import numpy as np


# MinMax normalisation (values between O and 1)
def normalize(img):
  img=(img-np.min(img))/(np.max(img)-np.min(img))
  return img

# MinMax normalisation (values between O and 255)
def normalize_255(img):
  img=((img-np.min(img))/(np.max(img)-np.min(img)))*255
  return img

# Image preprocessing with arcsinb transformation
def arcsinh_std_thresh(img,thresh,cofactor,kernel):
  img_sin=np.arcsinh(img*cofactor)
  img_med=cv2.medianBlur(img_sin,5)
  img_std=(img_med-np.mean(img_med))/np.std(img_med)
  img_thresh=np.where(img_std<thresh,0,img_sin)
  return img_thresh
    
#Convert image from mcd format to png
# A list of images and markers not interesting can be add as parameters
def convert_mcd_png(path_mcd,roi_exclude=[],marker_exclude=[],path="./images/raw_images"):
    if os.path.isdir(path)==False:
        os.mkdir(path)
    for file in os.listdir(path_mcd):
        print("   ** "+file+" **")
        with MCDFile(path_mcd+"/"+file) as f:
            slide = f.slides[0]
            panorama = slide.panoramas[0]
            for acq in range(len(slide.acquisitions)):
                acquisition = slide.acquisitions[acq]
                roi=acquisition.description
                if roi not in roi_exclude:
                    print("     ROI: "+roi)
                    if os.path.isdir(path+"/"+acquisition.description)==False:
                         os.mkdir(path+"/"+acquisition.description)
                    try:
                        img = f.read_acquisition(acquisition)
                        list_target=acquisition.channel_labels
                        dico_target={v:i for i,v in enumerate(list_target)}
                        for i in range(len(list_target)):
                            if list_target[i] not in marker_exclude:
                                img_marker=img[dico_target[list_target[i]],:,:]
                                cv2.imwrite(path+"/"+acquisition.description+"/"+list_target[i]+".png",img_marker)
                               
                    except:
                        print("     Erreure: "+roi)
                
#Function to visualize png images
# Image preprocessing uses arcsinh transformation 
def visualize_roi(cofactor=1000,thresh=2,kernel=5,path_raw="./images/raw_images",path="./images/arcsinh_images"):
    if os.path.isdir(path)==False:
        os.mkdir(path)
    for roi in os.listdir(path_raw):
        print("     ROI: "+roi)
        if os.path.isdir(path+"/"+roi)==False:
            os.mkdir(path+"/"+roi)
        for marker in os.listdir(path_raw+"/"+roi):
            img=plt.imread(path_raw+"/"+roi+"/"+marker)
            if marker!="DNA.png":
             img=arcsinh_std_thresh(img,thresh,cofactor,kernel)
            cv2.imwrite(path+"/"+roi+"/"+marker,normalize_255(img))

#Function to visualize png images
# The images are classified by markers
def visualize_marker(cofactor=1000,thresh=2,kernel=5,path_raw="./raw_images"):
    path="./images/marker_arcsinh"
    if os.path.isdir(path)==False:
        os.mkdir(path)
    for roi in os.listdir(path_raw):
            print("    ROI: "+roi)
            for marker in os.listdir(path_raw+"/"+roi):
                if os.path.isdir(path+"/"+marker[:-4])==False:
                    os.mkdir(path+"/"+marker[:-4])
                img=plt.imread(path_raw+"/"+roi+"/"+marker)
                #img=arcsinh_std_thresh(img,thresh,cofactor,kernel)
                img=np.arcsinh(img*100)
                cv2.imwrite(path+"/"+marker[:-4]+"/"+roi+".png",normalize_255(img))

def classified_image_by_marker(path_img="./images/arcsinh_img",path="./images/marker_arcsinh/"):
    if os.path.isdir(path)==False:
        os.mkdir(path)
    for roi in os.listdir(path_img):
        print("   ROI: "+roi)
        for marker in os.listdir(path_img+roi):
            if os.path.isdir(path+marker[:-4])==False:
                os.mkdir(path+marker[:-4])
            cv2.imwrite(path+marker[:-4]+"/"+roi+".png",normalize_255((plt.imread(path_img+roi+"/"+marker))))

def combine_marker(list_marker,path_raw):
    path="_".join(list_marker)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2
 
    color={}
    color_txt={}
    dico_pos={}
    colors=[0,1,2]
    pos=[20,60,100]
    colors_txt=[(150,0,0),(0,150,0),(0,0,150)]
    name=""
    for m in range(len(list_marker)):
        color[list_marker[m]]=colors[m]
        color_txt[list_marker[m]]=colors_txt[m]
        dico_pos[list_marker[m]]=pos[m]
        name+=list_marker[m]
    if os.path.isdir(path)==False:
        os.mkdir(path)
    for roi in os.listdir(path_raw):
        print("    ROI: "+roi)
        n=0
        for marker in list_marker:
            img_marker=plt.imread(path_raw+"/"+roi+"/"+marker+".png")
            if n==0:
                img=np.zeros((img_marker.shape[0],img_marker.shape[1],3))
                n+=1
            img[:,:,color[marker]]=normalize_255(arcsinh_std_thresh(img_marker,2,10000,3))
            #img[:,:,color[marker]]=normalize_255(np.arcsinh(img_marker*1000))
    
        for marker in list_marker:
            img = cv2.putText(img, marker,(20,img_marker.shape[0]-dico_pos[marker]), font, 
                fontScale,color_txt[marker], thickness, cv2.LINE_AA)
    
        cv2.imwrite(path+"/"+roi+".png",normalize_255(img))