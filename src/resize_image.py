#!/usr/bin/python
#-*- coding:utf8 -*-
from wand.image import Image


def resize_image(nomFichier, rep_dest=None, width=200, height=160):
    #pass
    

    # Converting first page into JPG
    if os.path.isfile(nomFichier) :
        # on isole le nom du fichier seul
        fic_basename = os.path.basename(nomFichier)
        photo_pdf = os.path.splitext(fic_basename)[0] + ".jpg"
        # on traite le pdf est on sauve la  photo
        with Image(filename=nomFichier + "[0]") as img:
            if rep_dest and os.path.isdir(rep_dest) :
                photo_pdf = os.path.join(rep_dest, photo_pdf)
                img.save(filename=photo_pdf)
                
            else :    
                img.save(filename=photo_pdf)
        #----------------------     
        # Resizing this image
        #---------------------
        with Image(filename=photo_pdf) as img:
            img.resize(200, 150)
            if rep_dest and os.path.isdir(rep_dest) :
                    fic_dest = os.path.splitext(fic_basename)[0] + "_thunbnail.jpg"
                    #on sauve la  photo
                    photo_pdf = os.path.join(rep_dest, fic_dest)
                    img.save(filename=photo_pdf)
            else :
                    img.save(filename= os.path.splitext(fic_basename)[0] + "_thunbnail.jpg")
    else :
        return False

