from IMC_tool import function
import sys
import function


cofactor=input("Saisir le cofacteur appliquer dans la transformation Arcsinh: ")
thresh=input("Saisir le seuil: ")
kernel=input("Saisir la taille du kernel: ")
path_raw=input("Saisir le chemin d'acces du dossier contenant les images brutes: ")


function.visualize_marker(int(cofactor),int(thresh),int(kernel),path_raw)
