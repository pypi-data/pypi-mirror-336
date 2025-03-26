from IMC_tool import function
#import function
import os

#path_mcd,path_png,roi_exclude,marker_exclude=read_parameters_convert()
path_mcd=input("Enter the path of the mcd file: ")
roi_exclude=input("Enter the ROI names you wish to exclude (separate with a comma): ")
marker_exclude=input("Enter the marker names you want to exclude (separate with a comma): ")
cofactor=input("Enter the cofactor applied in the Arcsinh transformation: ")
thresh=input("Enter threshold: ")
kernel=input("Enter kernel size: ")

marker_exclude=marker_exclude.split(",")
roi_exclude=roi_exclude.split(",")

if os.path.isdir("./images")==False:
    os.mkdir("./images")

print("*"*50)
print("Converting mcd files to png")
function.convert_mcd_png(path_mcd,roi_exclude,marker_exclude)

print("*"*50)
print("Image Pre-processing classified by roi ")
function.visualize_roi(int(cofactor),int(thresh),int(kernel))


print("*"*50)
print("Image Pre-processing classified by marker ")
function.classified_image_by_marker()