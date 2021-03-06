# -*- coding: utf-8 -*-
import re , os, glob
import datetime
from datetime import date, time
from codecs import open
import shutil  
#from wand.image import Image
from mymedia.models import Article, Photo
# Debugging
import logging
log = logging.getLogger(__name__ + "trace")


def copy_files():
    """
    """
    import os
    from codecs import open
    
    DstDir = "/home/aziz/dev/django/ebook/static/pdf/"
    SrcDir = "/home/aziz/Documents/ebook/"
    fd = open("liste_ebook.lst", "r")
    listfic = fd.read().splitlines()
    listfic.sort()
    
    for path, dirs, files in os.walk(SrcDir):
        files.sort()
        for filename in  files :
            source = os.path.join(path, filename)
            cible = os.path.join(DstDir, filename)
            shutil.copy(source, cible)
            #break;
      
    """
    assert not os.path.isabs(scrfile)
    dstdir =  os.path.join(dstroot, os.path.dirname(scrfile))
    os.makedirs(dstdir) # create all directories, raise an error if it already exists    
    """

def convertPdf2Image(nomFichier, rep_dest=None):
    #pass
    from wand.image import Image

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
                     # on traite le pdf est on sauve la  photo
                    photo_pdf = os.path.join(rep_dest, fic_dest)
                    img.save(filename=photo_pdf)
            else :
                    img.save(filename= os.path.splitext(fic_basename)[0] + "_thunbnail.jpg")
    else :
        return False

#-------------------------------
# recup_image
#-------------------------------

def recup_image(repertoire, rep_dest=None):
    """
    cette fonction recupere les image a partir des fichier pdf
    pour en sortir une image en jpeg grace a la librairie
    Wand
    http://garmoncheg.blogspot.fr/2013/07/python-converting-pdf-to-image.html
    pip install wand
    from wand.image import Image
    """
    if os.path.isdir(repertoire)   :
        for path, dirs, files in os.walk(repertoire):
           ## je prend que les fichier a extension .pdf
           files = [elem for elem in files if os.path.splitext(elem)[1] == '.pdf']

           for filename in  files :
               #print os.path.join(path, filename)
               nom_complet = os.path.join(path, filename)
               print nom_complet
               convertPdf2Image(nom_complet, rep_dest)
               #break
#-------------------------------save
# saveList_infic
#-------------------------------
        
def saveList_infic(repertoire):
    """
    lister les fichiers d'un reperoire est les enregistre en liste fichiers
    """
    fout = open('liste_ebook4.lst', 'w', 'utf-8')
       
    for path, dirs, files in os.walk(repertoire):
        files.sort()
        for filename in  files :
            #print os.path.join(path, filename)
            nom_complet = os.path.join(path, filename) + "\n"
            #str.encode('latin1').upper()
            #re.search([a-zA-Z0-9_.\-\(\)\[\]\' &+], nom_complet)
            #nom_complet = re.sub("[\W]", '', nom_complet)
            if filename.split(".")[-1].lower() in ["pdf", "ppt", "doc", "docs", "chm"] :
                nom_fichierMaj = filename.decode('utf-8').upper() + "\n"
                print nom_complet
                fout.write(nom_complet)
                        
    fout.close()
    return True
        
#-------------------------------
#
#-------------------------------
        
def save_indb():
    """
    """
    from mymedia.models import Article, Categorie, Auteur, Support
    import datetime,  shutil, os
    
    
    cat = Categorie.objects.get(nom=u"Informatique")
    aut = Auteur.objects.get(nom=u"Inconnu")
     
    #1/ charger la  liste des fichier pdf ebook
    listfic = []
    fd = open("liste_ebook4.lst", "r")
    listfic = fd.readlines()
    listfic.sort()
    
    #2/ charger un objet Livre( titre = xxx,   date_parution=xxx, description = xxx, categorie=cat, auteur=aut)
    for titre in listfic :
        #
        titre = titre.strip()
        if os.path.isfile(titre)  :
            print titre
            filename = os.path.basename(titre)
            
            art = Article()
            art.titre       = filename
            art.auteur      = aut
            art.description = ".".join(filename.split('.')[:-1])    
            art.categorie   = cat
            art.date_parution = datetime.datetime.now()
            art.url        = os.path.dirname(titre)
            art.categorie   = cat
            
    
        
            # 3/ sauve object livre en base 
            if filename.split(".")[-1].lower() in ["pdf", "ppt", "doc", "docx", "chm"] :
                nom_supp = "fichier " + filename.split(".")[-1].lower()
                try :
                    sup = Support.objects.get(nom=nom_supp)
                except: 
                    sup = Support.objects.get(pk=7)
                    
                art.support     = sup
                art.save()
            # 4/ copy file de la source to startic
            source = titre
            cible = os.path.join("/home/abdel/dev/django/ebook/static/pdf/", filename)
            shutil.copy(source, cible)
            #break
    # cloture de fichier
    fd.close()
    
 
def saveImage_indb(repertoire):
    # declaration
    from mymedia.models import Article, Photo
    
    if os.path.isdir(repertoire)   :
        for path, dirs, files in os.walk(repertoire):
           ## je prend que les fichier a extension .jpg
           files = [elem for elem in files if os.path.splitext(elem)[1] == '.jpg']

    # je prend les images et pas les etiquetes
    files = [elem for elem in files if elem.find('_thunbnail') > 0]
    
    for filename in  files :
        # on instancie un objet Image
        photo = Photo()
        
        #on charge l'objet du model Image
       
        
        photo.titre           = os.path.splitext(filename)[0]
        photo.titre           = photo.titre.strip()
        photo.created         = date(2014,01, 28) #datetime.datetime.today() or datetime.datetime.now().isoformat() datetime.datetime.utcnow()
        photo.localisation    = "/static/img/" + filename
        photo.url             = "http://localhost:8000/mymedia/static/img/" + filename
        photo.path            = "/static/img/" + filename
        photo.oldpath         =  os.path.abspath(os.path.join(path, filename))
        
        photo.grand_format    = filename.split("_thunbnail")[0] + ".jpg"
        photo.thunbnail_name  = filename
        nom_complet =   os.path.join(repertoire, photo.grand_format)
        if os.path.isfile(nom_complet) :
            #print nom_complet
            #photo.size        = os.path.getsize(nom_complet)
            taille      = os.path.getsize(nom_complet)
            photo.size_field  = taille
        else :
            photo.size_filed = None
        photo.resolution      = (200,150)
        photo.type_field      = "image/jpeg"
        photo.width_field     = 200
        photo.height_field    = 150
        
        
        
        libelle = filename.split("_thunbnail")[0]
        try :
            #print libelle liv_coresp = Livre.objects.get(titre__contains = "CSS3.pdf" )
            liv_coresp = Article.objects.get(titre = libelle + ".pdf")
            #print liv_coresp
            photo.article = liv_coresp 
            #photo_id = liv_coresp.id
           
            # save elem en base
            photo.save()
            print "sauve ..." +  photo.titre
            
        except Exception as err:
            log.debug('pas save erreur. %s', err)
            print 'pas save erreur. %s' % (err)
            
"""

"""
    #-------------------------------
#
#-------------------------------
        
def saveArticle_indb(repertoire):
    """
    """
    from mymedia.models import Article, Categorie, Auteur, Support
    import datetime,  shutil, os
    depot_uniq = []
    file_erreur = []
    
    
    cat = Categorie.objects.get(nom=u"Informatique")
    aut = Auteur.objects.get(nom=u"Inconnu")
     
    #1/ charger la  liste des fichier pdf ebook
    
    if os.path.isdir(repertoire)   :
        for path, dirs, files in os.walk(repertoire):
            ## je prend que les fichier a extension pdf ...
            print path
            files = [elem for elem in files if os.path.splitext(elem)[-1].lower() in [".pdf", ".ppt", ".doc", ".docx", ".chm"] ]
            
    
            #2/ charger un objet Livre( titre = xxx,   date_parution=xxx, description = xxx, categorie=cat, auteur=aut)
            for fichier in files :
                #
                #titre = titre.strip()
                #print titre
                filename = os.path.basename(fichier)
                
                art = Article()
                art.titre       = filename
                art.auteur      = aut
                art.description = os.path.splitext(fichier)[-1]    
                art.categorie   = cat
                art.date_parution = datetime.datetime.now()
                art.url        = os.path.dirname(fichier)
                art.categorie   = cat
                
                # 3/ sauve object livre en base 
                if filename not in depot_uniq and filename.split(".")[-1].lower() in  ["pdf", "ppt", "doc", "docx", "chm"]:
                    nom_supp = "fichier " + filename.split(".")[-1].lower()
                    try :
                        sup = Support.objects.get(nom=nom_supp)
                    except: 
                        sup = Support.objects.get(pk=7)
                        
                    art.support     = sup
                    # sauvegarde en base
                    try :
                        art.save()
                        #ajout en depot
                        depot_uniq.append(filename)
                    except :
                        print filename
                        file_erreur.append(fichier)
                        pass
                # 4/ copy file de la source to startic
                #break
    # cloture de fichier
    fd = open("list_fichiers_insindb.lst", "w")
    for elem in depot_uniq :
        fd.write(elem + '\n')
    fd.close()
    
     # save fichier en erreur
    fd = open("file_erreur.lst", "w")
    for elem in file_erreur :
        fd.write(elem + '\n')
    fd.close()
#--------------------------------------------
# Recupere la liste de fichiers pdf sans img
#--------------------------------------------
def list_pdf_sans_img():
    pdf_sans_image = []
    list_piece_img = []
    list_piece_pdf = []
        
    fdout = open("list_pdf_sans_image.lst", "w")
        
 
    #recuperer la liste des fichier img
    for path, dirs, files in os.walk("static/img/") :
        for fichier in files :
            # on verifie l'extension du fichier est jpg
            if os.path.splitext(fichier)[-1].lower() ==  ".jpg" :
                print fichier
                list_piece_img.append(os.path.splitext(fichier)[0])
                
    #recuperer la liste des fichier pdf 
    for path, dirs, files in os.walk("static/pdf/") :
        for fichier in files :
            if os.path.splitext(fichier)[-1].lower() ==  ".pdf" :
                list_piece_pdf.append(os.path.splitext(fichier)[0])
                
    # liste des pdf qui non pas d'image
    for elem in list_piece_pdf :
        if elem not in list_piece_img :
            pdf_sans_image.append(elem)
            
    # save in file 
    for elem in pdf_sans_image :
        fdout.write(elem + ".pdf\n")
    # fermeture du fichier
    fdout.close()
    
    # sauver les liste des fichiers pdf et img
    fd_pdf = open("liste_pieces_pdf.lst", "w")
    fd_img = open("liste_pieces_img.lst", "w")
    
    
    # save in file 
    for elem in list_piece_pdf:
        fd_pdf.write(elem + ".pdf\n")
    # fermeture du fichier
    fd_pdf.close()
    
    # save in file 
    for elem in list_piece_img:
        fd_img.write(elem + ".jpg\n")
    # fermeture du fichier
    fd_img.close()
    
    
#-------------------------------
# recup_image
#-------------------------------

def recup_imagepdf_fromlist(fichier_list, rep_dest="tmp/"):
    """
    cette fonction recupere les image a partir des fichier pdf
    pour en sortir une image en jpeg grace a la librairie
    Wand
    http://garmoncheg.blogspot.fr/2013/07/python-converting-pdf-to-image.html
    pip install wand
    from wand.image import Image
    """
    fd_pdf =  open(fichier_list, "r", 'utf-8')
    
    liste_pdf = fd_pdf.readlines()
    
    for fichier in liste_pdf :
        fichier = fichier.strip("\n")
        
        nom_complet = os.path.join("/home/aziz/dev/django/ebook/static/pdf/", fichier)
        #
        print nom_complet
        if os.path.isfile(nom_complet):
            #print os.path.join(path, filename)
            #print nom_complet
            try :
                convertPdf2Image(nom_complet, rep_dest)
            except Exception as err :
                pass
                

#-------------------------------save
# saveList_infic
#-------------------------------
        
def saveListVideo(repertoire):
    """
    lister les fichiers d'un reperoire est les enregistre en liste fichiers
    """
    fout = open('liste_video.lst', 'w', 'utf-8')
    
           
    for path, dirs, files in os.walk(repertoire):
        files.sort()
        for filename in  files :
            #print os.path.join(path, filename)
            nom_complet = os.path.join(path, filename) + "\n"
            #str.encode('latin1').upper()
            #re.search([a-zA-Z0-9_.\-\(\)\[\]\' &+], nom_complet)
            #nom_complet = re.sub("[\W]", '', nom_complet)
            if filename.split(".")[-1].lower() in ["m2ts"] :
                nom_fichierMaj = filename.decode('utf-8').upper() + "\n"
                print nom_complet
                fout.write(filename.decode("utf-8") + "\n" )  
                
                        
    fout.close()
    return True
#-------------------------------------------
# renommer les fichiers dans un repertoire
#-------------------------
def renameFiles(repertoire):
    """
    lister les fichiers d'un reperoire  
    """
    fout = open('liste_ebook4.lst', 'w', 'utf-8')
       
    for path, dirs, files in os.walk(repertoire):
        files.sort()
        for filename in  files :
            #print os.path.join(path, filename)
            nom_complet = os.path.join(path, filename)
	    new_name = nom_complet + '_' + str(time.time())

            #str.encode('latin1').upper()
            #re.search([a-zA-Z0-9_.\-\(\)\[\]\' &+], nom_complet)
            #nom_complet = re.sub("[\W]", '', nom_complet)
            if filename.split(".")[-1].lower() in ["jpeg", "png", "pdf", "ppt", "doc", "docs", "chm"] :
                #nom_fichierMaj = filename.decode('utf-8').upper() + "\n"
                print nom_complet

                os.path.os.rename(nom_complet, new_name)
		fout.write(new_name + '\n')
                        
    fout.close()
    return True
