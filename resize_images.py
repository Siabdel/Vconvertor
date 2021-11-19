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
		with Image(filename=photo) as img:
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
	# Converting first page into JPG
	for filename in os.listdir( rep_in):
		fic_basename = os.basename(filename)

		types = ('*.jpg', '*.jpeg') # the tuple of file types
		
		for os.path.splitext(fic_basename)[1] in types:
			files_a_traiter.append(tag)(glob.glob(files))
			
	print files_a_traiter





if __name__ == '__main__':
   #
   local = os.path.dirname()
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

   main(BASE_DIR)



