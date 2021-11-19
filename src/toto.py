#!/usr/bin/python
#-*- coding:utf8 -*-
from wand.image import Image
import os, sys 
from datetime import datetime
import re , os, glob

def resize_image(nomFichier, rep_dest=None, width=200, height=160):
	"""
	# Converting first page into JPG
	"""

	if os.path.isfile(nomFichier) :
		# on isole le nom du fichier seul
		fic_basename = os.path.basename(nomFichier)
		#----------------------     
		# Resizing this image
		#---------------------
		with Image(filename=nomFichier) as img:
			img.resize(width, height)

			if rep_dest and os.path.isdir(rep_dest) :
				fic_dest = os.path.splitext(fic_basename)[0] + "_thunbnail.jpg"
				#on sauve la  photo
				photo = os.path.join(rep_dest, fic_dest)
				img.save(filename=photo)
			else :
				img.save(filename= os.path.splitext(fic_basename)[0] + "_thunbnail.jpg")

	return False


# programme principale 
def main(rep_in):
	"""
	rep_in 
	"""
	files_a_traiter = []
	print(rep_in)
	# filtrez les fichier a traiter
	if os.path.isdir(rep_in) :
		filenames  = os.listdir(rep_in) 
		for filename in filenames:
			#print("filename = %s%s " % (rep_in, filename))
			fic_basename = os.path.basename(filename)
			
			types = ('.jpg', '.jpeg') # the tuple of file types
			extension = os.path.splitext(fic_basename)[1]
			print extension
			
			if extension in types:
				files_a_traiter.extend(glob.glob(os.path.join(rep_in, filename)))
			
		print(files_a_traiter)

	#traiter les fichier
	for image in files_a_traiter:
		#
		resize_image(image)





if __name__ == '__main__':
   #
   BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   #
   main(BASE_DIR)
