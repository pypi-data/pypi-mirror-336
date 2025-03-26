from IMC_tool import function

#path_mcd,path_png,roi_exclude,marker_exclude=read_parameters_convert()
path_mcd=input("Saisir le chemin d'acces au fichier mcd: ")
roi_exclude=input("Saisir les noms de ROI que vous souhaitez exclure (séparer par une virgule): ")
marker_exclude=input("Saisir les noms de marqueurs que vous souhaitez exclure (séparer par une virgule): ")
marker_exclude=marker_exclude.split(",")
roi_exclude=roi_exclude.split(",")

function.convert_mcd_png(path_mcd,roi_exclude,marker_exclude)