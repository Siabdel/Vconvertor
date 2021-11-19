# -*- coding: utf8 -*-
# module local 
from clss_convertor import ClssConvertor
from clss_helpers import *
from commun_helpers import subprocessLaunchWithoutConsole, searchConfigUserFromFileXml, createElemntXml
from commun_helpers import creerRepertoire, deleteConfigUserFromFileXml
# module general
import threading
import tkinter
import Pmw

from tkinter import messagebox
from tkinter.filedialog import askdirectory, askopenfile, askopenfilenames, askopenfiles
import fileinput
import os, sys, stat, string
#import _winreg
from tkinter.scrolledtext import *
from time import (strftime, mktime)
import time
from datetime import datetime
import re
#sys.path.append("C:\Python26\Lib\site-packages")
#sys.path.append("C:\Python26\Lib\site-packages\win32\lib")
#import win32api
#import win32com
from xml.dom import minidom
import fileinput
import decimal
from  traceback  import print_exc
from logging import debug
import glob
import converter
from converter import *
import logging
import subprocess  
import signal
import json
from string import *
import tempfile
import shutil
import logging




mswindows = (sys.platform == "win32")
logger = logging.getLogger(__name__)

class ClssStartConvertor(ClssConvertor) :
	"""
	StartConvertor
	"""
	
	def __init__(self, parent) :
		self.parent = parent
		self.tab_entry_connexion = {}
		self.group_process = None
		self.compteur_lig = 0
		self.src_filenames = []
		self.button_cmd = None
		#---------------------------------------------
		# 1- initialisation de la classe mere
		#---------------------------------------------
		ClssConvertor.__init__(self)

		#---------------------------------------------
		# 2- charge l'environnment 
		#---------------------------------------------
		self.chargeEnvironnement()
		
		#---------------------------------------------
		# 3- lancement de l'interfae
		#---------------------------------------------
		self.interfaceStart()
		
		
	
	def interfaceStart(self) :
		#
		self.options = {}
		initialdir  = os.getcwd() + "/config/param.xml"
		self.options['initialdir'] = initialdir
		self.options['title'] = 'Localisation du fichier param.xml'
		self.options['defaultextension'] = '*.xml' 
		
		
		pframe = tkinter.Frame(self.parent, bd =1,  bg ='#D0E3FF', width= 400, height=180);
		pframe.pack(fill = 'both', expand = 1)
		
		# multi frames
		self.notebook1 = Pmw.NoteBook(pframe, 
						createcommand = None,
						lowercommand = 	None,
						raisecommand = 	None,
						hull_width 	= 450,
						hull_height 	= 340,
						)	
		
		# Pack the notebook last so that the buttonbox does not disappear
		# when the window is made smaller.
		self.notebook1.pack(fill = 'both', expand = 1, padx = 5, pady = 5 )
		
		self.page1 = self.notebook1.add('Muti Lignes conversion')
		self.page2 = self.notebook1.add('Free conversion')
		self.page3 = self.notebook1.add('Extraction audio') 
		 
		self.page1.focus()
		# le groupe
		self.group_options = Pmw.Group(self.parent, tag_text='Atlass Convertor')
		self.group_options.pack(side='top',  expand = 1, padx = 2, pady = 2)
		
		# Commandes 
		self.img_convert 	= PhotoImage(file = "images/convert.gif" ) 
		self.img_play 		= PhotoImage(file = "images/play.gif" , height=50)
		self.img_param 		= PhotoImage(file = "images/param.gif" ) 
		self.img_ajouter	= PhotoImage(file = "images/ajouter.gif" , height=50)
		self.img_reload		= PhotoImage(file = "images/reload.gif" , height=50)
		self.img_quitter	= PhotoImage(file = "images/quitter_2.gif" , height=50)
		
		
		self.tipinfo1 = Pmw.Balloon(self.group_options.interior())
		
		self.buttonBoxAdmin = Pmw.ButtonBox(self.page1)
		bt1 = self.buttonBoxAdmin.add('Ajouter',cursor='hand2',width=100, height=40, command = self.ajouterVideo,
					      image=self.img_ajouter)
		bt2 = self.buttonBoxAdmin.add('Clear',  cursor='hand2',width=100, height=40, command = self.parametrages,
					      image=self.img_reload)
		bt3 = self.buttonBoxAdmin.add('Lancer Convertor',cursor='hand2',width=100, height=40,
					      command = self.runApplicationConvertor, image=self.img_convert)
		bt4 = self.buttonBoxAdmin.add('Parametrage',  	cursor='hand2',width=100, height=40,
					      command = self.parametrages, image=self.img_param)
		bt5 = self.buttonBoxAdmin.add('Rotate',  cursor='hand2',width=9, height=2,
					      command = self.rotate, text="Rotation 90")
		bt6 = self.buttonBoxAdmin.add('Free M2TS convert',  cursor='hand2',width=9, height=2,
					      command = self.converM2tsToAvi, text="Free M2TS convert")
		bt7 = self.buttonBoxAdmin.add('Assembler des videos',  cursor='hand2',width=9, height=2,
					      command = self.concat_videos, text="Assembler des video")
		
		bt8 = self.buttonBoxAdmin.add('Assembler des morceaux audio',  cursor='hand2',width=20, height=2,
					      command = self.concat_fichiers_audio, text="Assembler des morceaux audio")
		
		
		
		self.buttonBoxAdmin2 = Pmw.ButtonBox(self.page3)
		
		
		self.buttonBoxAdmin.pack(padx=3, pady=3)
		self.buttonBoxAdmin2.pack(padx=3, pady=3)
		
		self.tipinfo1.bind(bt1, 'Lancer Convertor')
		self.tipinfo1.bind(bt2, 'Parametrage du lanceur')
		#
		#-----------------------------
		# choix du type de traitement
		#-----------------------------
		"""
		self.variable1 = IntVar()
		self.variable2 = IntVar()
		checkbox1 = Checkbutton(pframe_page1, variable=self.variable1, text='Audio',
				       command=self.verifieEtat)
		self.etat = Label(pframe_page1)

		checkbox2 = Checkbutton(pframe_page1, variable=self.variable2, text='Video',
				       command=self.verifieEtat)
		checkbox1.grid(row=1, column=1)
		checkbox2.grid(row=1, column=2)
		"""
		#-----------------------------
		#Page 1 conversion parametre 
		#-----------------------------
		pframe_page1 = tkinter.Frame(self.page1, bd =1,  bg ='#D0E3FF', width= 400, height=18);
		pframe_page1.pack(fill = 'both', expand = 1)
		
		## choix de type de Format.
		libelles = ["Audio", "Video", "Image"]
		valSegments = ["A", "V", "I"]
		
		self.groupe_type = Pmw.Group(pframe_page1, tag_text='type de codage')
		self.groupe_type.pack(side='top',  expand = 1, padx = 2, pady = 2)
		
		self.optionsSauve = StringVar()
		self.optionsSauve.set(valSegments[0])
		

		ind = 0
		self.bout_type = []
		for n in [0,1,2]:
			self.bout_type.append(Radiobutton(self.groupe_type.interior(), text = libelles[n],
							   width=12, variable = self.optionsSauve,
							   value = valSegments[n], command = self.monchoix))
			self.bout_type[n].grid(row=3, column= n)
		#-------------------------
		#- Recape des choix
		#-------------------------
		pframe_info = tkinter.Frame(self.page1, bd =1,  bg ='#fff', width= 1400, height=18);
		pframe_info.pack(fill = 'both', expand = YES)
		
		self.group_info = Pmw.Group(pframe_info, tag_text='parametrage du codage choisi')
		self.group_info.config(background='#fff')
		self.group_info.pack(side=TOP, expand = 1, padx = 2, pady = 2)

		# label audio
		self.label_audio = Label(self.group_info.interior())
		Label(self.group_info.interior(),  fg='#00f', text="Format audio :").grid(row=1, column=0)
		self.label_audio.grid(row=1, column=1)
		
		# label video codec
		self.label_format_video = Label(self.group_info.interior())
		Label(self.group_info.interior(), fg='#00f', text="Format Video :").grid(row=1, column=2)
		self.label_format_video.grid(row=1, column=3)

		# label definitions
		self.label_definition = Label(self.group_info.interior())
		Label(self.group_info.interior(),  fg='#00f', text="Definition :").grid(row=1, column=4)
		self.label_definition.grid(row=1, column=5)
		
		# label video format
		self.label_codec_video = Label(self.group_info.interior())
		Label(self.group_info.interior(),  fg='#00f', text="Codec Video :").grid(row=1, column=6)
		self.label_codec_video.grid(row=1, column=7)
		
		
		#-------------------------
		# liste des codecs audio
		#-------------------------
		pframe_codec = tkinter.Frame(self.page1, bd =1,  bg ='#D0E3FF', width= 400, height=180);
		pframe_codec.pack(fill = 'both', expand = 1)
		
		#----------------------------------------
		# liste du format video/audi emballage
		# Ogg : container format, mostly used with Vorbis and Theora.
		# Avi : container format, often used vith DivX video.
		# mkv : Matroska format, often used with H.264 video.
		# WebM : is Google's variant of Matroska containing only
		# VP8 : for video and Vorbis for audio content.
		# flv : Flash Video container format.
		# Mov : container format, used mostly with H.264 video content, often for mobile platforms.
		# Mp4 : container format, the default Format for H.264  video content.
		# MPEG(TS) :  container, used mainly for MPEG 1/2 video codecs
		# Mp3 : container, used audio-only mp3 files
		

		#----------------------------------------
		self.group_format_video = Pmw.Group(pframe_codec, tag_text='Format video de sortie ')
		self.group_format_video.pack(side=LEFT,  expand = NO, padx = 2, pady = 2)
		
		format_list = ['ogg', ' avi', ' mkv', ' webm', 'flv', 'mov', 'mp4', 'mpeg']
		self.scrol_format = ScrooledList(format_list, self.group_format_video.interior(), self.label_format_video)
		self.scrol_format.configure(height=2, width=12)
		self.scrol_format.grid(row=1, column=1)
		
		
		#-------------------------
		# liste des codecs video
		#-------------------------
		self.group_sources_video = Pmw.Group(pframe_codec, tag_text='Codec video')
		self.group_sources_video.pack(side=LEFT,  expand = NO, padx = 2, pady = 2)
		
		options_video = ['mpeg2', 'mpeg4', 'h264']
		self.scrol_video = ScrooledList(options_video,  self.group_sources_video.interior(), self.label_codec_video)
		self.scrol_video.listbox.configure(height=2, width=12)
		
		self.group_definitions = Pmw.Group(pframe_codec, tag_text='Definitions')
		self.group_definitions.pack(side=LEFT,  expand = NO, padx = 2, pady = 2)
		definitions  = ["720x400", "1280x720", "960x540", "1024x768", "1024x576", "1280x720", "1440x1080","1440x1980", "1600x1200", "1920x1080"]
		ind = 0
		
		valSegments = ["720x400", "960x540", "1024x768", "1024x576", "1280x720","1440x1080","1440x1980", "1600x1200", "1920x1080"]
		definitions_video = {"sqcif" :  "128x96","qcif" :  "176x144", 
		'cif' :    "352x288", "4cif":    "704x576", "16cif":    "1408x1152",
		"qqvga":    "160x120","qvga":    "320x240","vga":    "640x480",
		"svga":    "800x600","xga":    "1024x768","uxga":    "1600x1200",
		"qxga":    "2048x1536","sxga":    "1280x1024","qsxga":    "2560x2048",
		"hsxga":    "5120x4096","wvga":    "852x480","wxga":    "1366x768",
		"wsxga":    "1600x1024","wuxga":    "1920x1200","woxga":    "2560x1600",
		"wqsxga":    "3200x2048","wquxga":    "3840x2400","whsxga":    "6400x4096",
		"whuxga":    "7680x4800","cga":    "320x200","ega":    "640x350",
		"hd480":    "852x480","hd720":    "1280x720","hd1080":    "1920x1080"
		}

		
		
		self.scrol_def = ScrooledList(definitions,  self.group_definitions.interior(), self.label_definition)
		self.scrol_def.listbox.configure(height=2, width=12)
		
		# ratio du format
		ratio = ["4:3", "16:9"]
		#-------------------------
		# format audio
		#-------------------------
		
		self.group_sources_audio = Pmw.Group(pframe_codec, tag_text='Format audio')
		self.group_sources_audio.pack(side=LEFT,  expand = NO, padx = 2, pady = 2)
		
		#options_image  = ['JPG,BMP,PNG,TIF,ICO,GIF,TGA']
		#options = map(lambda ind : 'element_' + str(ind), range(20))
		options_audio  = ['FLAC', 'APE',  'OGG', 'AAC', 'MP3', 'WAV', 'AMR' ]
		self.scrol_audio = ScrooledList(options_audio, self.group_sources_audio.interior(),
					   self.label_audio)
		self.scrol_audio.grid(row=1, column=0)
		
		canaux = ["canal 1", "canal 2", "canal 3"]
		valSegments = ["1", "2", "3"]
		self.canaux_son = StringVar()
		self.canaux_son.set(canaux[0])
		self.bout_type = []
		
		
		for n in range(len(canaux)):
			self.bout_type.append(Radiobutton(self.group_sources_audio.interior(), text = canaux[n],
							   width=12, variable = self.canaux_son,
							   value = valSegments[n], command = self.monchoix))
			self.bout_type[n].grid(row=n, column=1)

		#-------------------------
		#- page 2  
		#-------------------------
		self.affPage2()
		
		#-------------------------
		#- page 3
		#-------------------------
		self.affPage3()
		#-------------------------
		#- Info Suivi 
		#-------------------------
		self.group_info = Pmw.Group(pframe, tag_text='Sources')
		self.group_info.pack(side=TOP,  expand = YES, padx = 2, pady = 2)
		self.suivis 	= Listbox(self.group_info.interior())
		ascenseur 	= Scrollbar(self.group_info.interior())

		ascenseur.config(command = self.suivis.yview)
		self.suivis.config(yscrollcommand = ascenseur.set)
		self.suivis.config(background='black', foreground='green')
		self.suivis.config(height = 5, width = 100)
		self.suivis.insert(0 , '------------ videos a convertir --------------')
		self.suivis.insert(self.suivant(), '----------------------------------------------')
		self.suivis.pack()
	
	
		self.buttonBoxMain = Pmw.ButtonBox(pframe)
		
		self.buttonBoxMain.add('Ok',  	  cursor='hand2',width=12, height=3,  command = None )
		self.buttonBoxMain.add('Quitter', cursor='hand2',width=12, height=3,  command = self.parent.quit )
		self.buttonBoxMain.pack()
		
		
		
	def affPage2(self):
		#-------------------------
		# liste des codecs audio
		#-------------------------
		p2frame = tkinter.Frame(self.page2, bd =1,  bg ='#D0E3FF', width= 400, height=180);
		p2frame.pack(fill = 'both', expand = 1)
		
		#----------------------------------------
		# liste du format video/audi emballage
		# Ogg : container format, mostly used with Vorbis and Theora.
		# Avi : container format, often used vith DivX video.
		# mkv : Matroska format, often used with H.264 video.
		# WebM : is Google's variant of Matroska containing only
		# VP8 : for video and Vorbis for audio content.
		# flv : Flash Video container format.
		# Mov : container format, used mostly with H.264 video content, often for mobile platforms.
		# Mp4 : container format, the default Format for H.264  video content.
		# MPEG(TS) :  container, used mainly for MPEG 1/2 video codecs
		# Mp3 : container, used audio-only mp3 files
		

		#----------------------------------------
		self.groupe_page2	= Pmw.Group(p2frame, tag_text='Format video de sortie ')
		self.groupe_page2.pack(side=LEFT,  expand = NO, padx = 2, pady = 2)
		"""
		effects avec ffmpeg
		2 videos of 4 seconds each. Need to join it with fade between them.videos are 25 fps.
		1) Add fade out (light to dark) at the end of the 1st and fade in (dark to light) at the beggining of the 2nd:
		
		ffmpeg -i 1.mp4 -y -vf fade=out:76:24 1f.mp4
		
		ffmpeg -i 2.mp4 -y -vf fade=in:0:25 2f.mp4
		76:24 mean the fade out will start frame 76 and will finish 24 frames later = 1s fade out.
		
		0:25 mean the fade in will start frame 0 and will finish 25 frames later.
		
		2) Merge the 2 videos Convert all to TS
		
		ffmpeg -i 1f.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts 1f.ts
		
		ffmpeg -i 2f.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts 2f.ts
		Merge

		ffmpeg -i "concat:1f.ts|2f.ts" -bsf:a aac_adtstoasc -c copy output.mp4
		"""

		self.list_cmd_ffmpeg_video_complet= {
		#convertir au foramt Full DH' If you want to convert the recorded files at full HD resolution
		"Convertir la video en Full HD ": "ffmpeg -i %s inputfile.m2ts -deinterlace -sameq %s outputfile.avi",
		
		#Extraire le son de la video
		"""
		-i “input file”
		-vn “skip the video part”
		-ac “audio channels”
		-ar “audio rate”
		-ab “audio bit-rate“ 320 kbit
		-f “file format to use”
		"""

		"Extraire le son de la video":"ffmpeg -i 'whatever.format' -vn -ac 2 -ar 44100 -ab 320k -f mp3 output.mp3",
		# Convertir une video ts (transport streaming)
		"Convertir une video ts (transport streaming)" : "ffmpeg -i 000.ts -vcodec copy -acodec copy -absf aac_adtstoasc toto.mp4",
		#Separer la video du son -vn : desactive l’enregistrement video -f : force le format de sortie (facultatif: par defaut FFMPEG choisit le format specifie parl’extension
		'Extraire le son d\'une video' : "ffmpeg -i fichier_video.avi -vn -f mp3v fichier_son.mp3",
		#Separer la video du son -an : desactive l’enregistrement audio
		'Recuperer uniquement le flux video' :"ffmpeg -i fichier_video.avi -an -f avi fichier_sans_son.mp4",

		# generer du gif animes
		'generer de la même maniere des gif animes' : "ffmpeg -i test.avi out.gif",
		# Fusionner du son et de la video
		'fusionner un fichier audio et un fichier video pour creer une video avec une piste sonore' :
			"ffmpeg -i son.wav -i video.yuv out.mpg",
		
		# creation de video a partir de plusieurs images
		'Creation de videos g partir d\'un ensemble d\'images': "ffmpeg -r 24 -b 1800 -i %02d.bmp out.mpg",
		"For extracting images from a video" : "ffmpeg -i foo.avi -r 1 -s WxH -f image2 foo-%03d.jpeg",

		# *** Effectuer un screencast
		#Un screencast consiste en une capture video de votre ecran et FFMPEG fait ca tres facilement :
		#-b : permet de regler le taux d’echantillonnage de la video (cela influe sur la qualite video)
		#-f : l’argument x11grab permet de specifier qu’il faut capturer « l’ecran »
		#-s : la taille (ici votre resolution)
		#-r : le nombre d’images par seconde (25 fps par defaut)
		#-i : ici le numero de votre ecran de votre serveur X11 (variable d’environnement DISPLAY)
		# Pour connaître le numero de votre ecran $ env | grep DISPLAY
		"Faire une capture video de votre ecran et FFMPEG" : "ffmpeg -b 1000k -f x11grab -s 1024x768 -r 30 -i :0.0 capture.mpg",

		# Euro format: (PAL)

		"Creation DVD en pal a partir d'un fichier m2ts freeBox" 	: " ffmpeg -i inputfile.m2ts -deinterlace -target pal-dvd outputfile.avi",
		"Creation XVID (Computer Format @ Max Resoution / same as source)" : "ffmpeg -i inputfile.m2ts -threads 0 -deinterlace -f avi -r 25 -vcodec libxvid -vtag XVID  -aspect 16:9 -maxrate 1800k -b 1500k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis -aic -cmp 2 -subcmp 2 -g 300 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 outputfile.avi ",
		"Creation XVID (Computer Format @ Reasonable Web Resolution) " : "ffmpeg -i inputfile.m2ts -threads 0 -deinterlace -f avi -r 25 -vcodec libxvid -vtag XVID -s 480x360 -aspect 16:9 -maxrate 1000k -b 700k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis -aic -cmp 2 -subcmp 2 -g 300 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 outputfile.avi",

		#Extraction  images d une video:
		
		"You can put many streams of the same type in the output" :"ffmpeg -i test1.avi -i test2.avi -vcodec copy -acodec copy -vcodec copy -acodec copy test12.avi -newvideo -newaudio",
		#Extraire une image d’une video
		#Il s’agit d’extraire une image de la video et d’en faire une miniature pour donner un apercu de la video.
		#-vcodec : specifie le codec de sortie (ici mjpeg pour obtenir une image au format jpg)
		#-vframes : nombre d’images g capturer
		#-ss : position de l’image dans le temps
		"Extraire une image d’une video" : "ffmpeg -i %s -vcodec mjpeg -vframes 1 -an -s 200x200 -ss 30 %s" ,
		"Extraire des images a partir d'une video" : "ffmpeg -i foo.avi -r 1 -s WxH -f image2.jpeg",
		"Creation video a partir de plusieurs images" : "ffmpeg -f image2 -i toto.jpeg -r 12 -s WxH foo.avi",
		#
		"Convertir fichier avi en un fichier mkv (le format Matroska)": "ffmpeg -i entree.avi -threads 4 -f matroska -vcodec libvpx -vb 1350000 -rc_lookahead 16 -keyint_min 0 -g 360 -skip_threshold 0 -level 116 -qmin 15 -qmax 30 -acodec libvorbis -ab 128k -ar 44100 -ac 2 sortie.mkv ",
		# Rotation de la video de 90 degre
		"Rotation de la video de 90 degre": "ffmpeg -i e:/python/convertor/test1.ogg -vf rotate=90 e:/python/convertor/output.ogg",
		# decouper un bout de video 
		#"decouper un bout de video": "ffmpeg -ss 00:00:30.00 -t 00:00:25:00 -i video.flv video-new.avi" #ne marche pas bien
		#devrait te couper un bout de 25seconde apres 30s du debut., #
		"decouper un bout de video": "avconv -i video_source.m2ts -vcodec copy -acodec copy -ss 00:00:30  -t 00:00:25 video_elvis.mp4",
		# decoupage audio
		#ffmpeg -i input.wmv -ss 00:00:30.0 -c copy -t 00:00:10.0 output.wmv
		#ffmpeg -i input.wmv -ss 30 -c copy -t 10 output.wmv
		# decoupage video
		#ffmpeg -i movie.mp4 -ss 00:03:56 -c copy -t 00:00:29 output.mp4


		}
		#Encoder une video pour l'iPhone ou l'iPod Touch
		#ffmpeg -i source_video.avi input -acodec aac -ab 128kb -vcodec mpeg4 -b 1200kb -mbd 2 -flags +4mv+trell -aic 2 -cmp 2 -subcmp 2 -s 320x180 -title X final_video.mp4
		#ffmpeg -i source_video.avi input -acodec aac -ab 128kb -vcodec mpeg4 -b 1200kb -mbd 2 -flags +4mv+trell -aic 2 -cmp 2 -subcmp 2 -s 320x180 -title X final_video.mp4
		

		#ffcommand = eval ('ffcommand_in % (fichier_in, format_audio, fichier_out)')
		self.list_cmd_ffmpeg_video = {
			#convertir au foramt Full DH' If you want to convert the recorded files at full HD resolution
			#"Convertir mes video freeBox m2ts"	: "ffmpeg -i %s  -acodec libmp3lame -ac 1 -aq 10 -ar 11025 -vcodec libx264 -r 15 -s '1440x1080' -aspect 16:9 -f %s -y -vlang fr -alang fr '%s'",
			"Convertir la video en Full HD "	: "ffmpeg -i %s  -deinterlace -sameq  %s",
			"Convertir mes video freeBox m2ts"	: 'ffmpeg -i %s  -acodec libmp3lame -ac 1 -aq 10 -ar 11025 -vcodec libx264 -r 15 -s 1440x1080 -aspect 16:9  -y -vlang fr -alang fr "%s"',
			"Encoder une video pour l'iPhone ou l'iPod Touch" : "ffmpeg -i %s -acodec aac -ab 128kb -vcodec mpeg4 -b 1200kb -mbd 2 -flags +4mv+trell -cmp 2 -subcmp 2 -s 320x180  %s",
			# ffmpeg -i 000.ts  -vcodec libx264 -f mp3 toto.mkv
			"Convertir les fichiers ts du recepeteur SAMSAT TITAN  en mpeg4"  : "ffmpeg -i %s   %s",
			# ffmpeg -i 000.ts  -vcodec libx264 -f mp3 toto.mkv
			"Convertir les fichiers ts du recepeteur SAMSAT TITAN en bonne qualite codage h264"  : "ffmpeg -i %s -vcodec libx264  %s",
			"Convertir les fichiers ts du recepeteur SAMSAT TITAN en HD (1440x1080) qualite codage h264"  : "ffmpeg -i %s -vcodec libx264 s-1440x1080 %s",
			# Pivoter la video de 90 degre a droite
			#"Pivoter la video" : "avconv -i %s -vf 'transpose=1' -codec:v libx264 -preset slow -crf 25 -codec:a copy %s",
			"Pivoter la video" : "ffmpeg -i %s -vf 'transpose=1' -vcodec  libx264 -s 480x852 -acodec copy %s",
			
			#ffmpeg -y -i concat:"source1.ts|source2.ts" -absf aac_adtstoasc -c copy -f mov "destination.mp4"
			# en details
			#ffmpeg -i input1.avi -qscale:v 1 intermediate1.mpg
			#ffmpeg -i input2.avi -qscale:v 1 intermediate2.mpg
			#ffmpeg -i concat:"intermediate1.mpg|intermediate2.mpg" -c copy intermediate_all.mpg
			#ffmpeg -i intermediate_all.mpg -qscale:v 2 output.avi
			# or
			# cat 1.mpeg 2.mpeg 3.mpeg | avconv -f mpeg -i - -vcodec mpeg4 -strict experimental output.mp4
			#ffmpeg -i intermediate_all.mpg -qscale:v 2 output.avi
			# ==> fonctionne avconv -i "concat:001.mp4|002.mp4|003.mp4" -c copy full.mp4
			# a partir d'une liste de fichiers infic.txt==> avconv  -f h264 concat -i infic.txt   -c copy -bsf:a aac_adtstoasc  test_all.mkv
			# ok fusionner plusieurs mp3 ==>  avconv -i "concat:YebadOuNavdou.mp3|TafatDdunitIw.mp3" -c copy out.mp3
			
			"Assembler des videos en un seul fichier video" : "ffmpeg -y -i concat:%s|%s -absf aac_adtstoasc -c copy   %s",
			"Mariage traitement 2016 fichier video" : "ffmpeg -i %s -acodec libmp3lame  -s 1920x1080   -y %s"

		}
		
		self.scrol_format_ffmpeg = ScrooledList(self.list_cmd_ffmpeg_video.keys(), self.groupe_page2.interior(),
							self.afficheInfos, 10, 200, self.afficheCmdVideo)
		#self.scrol_format_ffmpeg.configure(width=200)
		self.scrol_format_ffmpeg.grid(row=0, column=0, columnspan=25)
		
		#------------------------------
		# choix du format video , ...
		format_list = ['ogg', ' avi', ' mkv', ' webm', 'flv', 'mov', 'mp4', 'mpeg']

		self.var_video = StringVar()
		self.var_video.set( format_list [1])
		self.bout_video = []
		
		
		for n in range(len(format_list)):
			self.bout_video.append(Radiobutton(self.groupe_page2.interior(), text = format_list [n],
							   width=3, variable = self.var_video,
							   value = format_list[n], command = self.monchoix))
			self.bout_video[n].grid(row=1, column=n)

		
		return True
	
	def affPage3(self) :
		"""
		Extraction audio des fichiers video avi et mpeg
		"""
		
		#-----------------------------
		# frame  
		#-----------------------------
		pframe_page3 = tkinter.Frame(self.page3, bd =1,  bg ='#D0E3FF', width= 400, height=18);
		pframe_page3.pack(fill = 'both', expand = 1)
		#
		self.groupe_page3	= Pmw.Group(pframe_page3, tag_text='transcodage audio')
		self.groupe_page3.pack(side=LEFT,  expand = NO, padx = 2, pady = 2)
		
		
		
		
		#Extraire le son de la video
		"""
		-i “input file”
		-vn “skip the video part”
		-ac “audio channels”
		-ar “audio rate”
		-ab “audio bit-rate“ 320 kbit
		-f “file format to use”
		#Separer la video du son -vn : desactive l’enregistrement video -f : force le format de sortie (facultatif: par defaut FFMPEG choisit le format specifie parl’extension
		# encoder un DVD		
		mencoder dvd://2 -ovc lavc -lavcopts vcodec=mpeg4:vhq:vbitrate="1200" -vf scale -zoom -xy 640 -oac mp3lame -lameopts br=128 -o /nas/videos/my-movies/example/track2.avi
		# extraire des photo de la video (-r frequence freme -f 		
		#ffmpeg -i Dvd\ Mehdi\&Oifa.mkv -r 25 -f image2 test_%4d.jpeg
		# extraire une photo -vframe 
		==> ffmpeg -i "fichier.avi" -vcodec mjpeg -vframes 1 -an -f rawvideo -s 640x360 -ss 20 "image.jpg"
                # extraire un echantillon de photo
 		ffmpeg -i film.mkv -ss 00:01:40  -t 00:15:00 -r 1/60 out/test_%4d.png
		#
 		ffmpeg -i Mariage2015.mkv -ss 00:01:40  -t 00:15:00 -r 1/10 out/test_%4d.png
		ffmpeg -i Mariage2015.mkv -ss 01:00:00  -t 00:30:00 -r 1/10 out/test_%4d.png



		"""
		self.list_cmd_ffmpeg_audio = {
			"Extraire le son en qualte superieur"	: "ffmpeg -i %s -vn -ac 2 -ar 44100 -ab 320k -f %s -y '%s' ",
			# wav to mp3
			'convertir un fichier wav en mp3 g 22050 Hz' : "ffmpeg -i %s -ar 22050 -f %s %s -y ",
		
		}
		
		self.scrol_lignes_etraction = ScrooledList(self.list_cmd_ffmpeg_audio.keys(), self.groupe_page3.interior(),
							   self.afficheInfos, 10, 200, self.afficheCmdAudio)
		#self.scrol_format_ffmpeg.configure(width=200)
		self.scrol_lignes_etraction.grid(row=0, column=0, columnspan=25)
		
		#------------------------------
		# choix du format audio mp3, FLAC, ACC, ...
		format_list = ['FLAC', ' ACC', 'APE', 'OGG', 'MP3', 'WAV']

		self.var_son = StringVar()
		self.var_son.set( format_list [0])
		self.bout_wave = []
		
		
		for n in range(len(format_list)):
			self.bout_wave.append(Radiobutton(self.groupe_page3.interior(), text = format_list [n],
							   width=3, variable = self.var_son,
							   value = format_list[n], command = self.monchoix))
			self.bout_wave[n].grid(row=1, column=n)

		
		#==================================
		#Les different choix
		#-----------------------------
		libelles = ["Oui", "Non"]
		valNomages = ["O", "N"]
		
		self.optionsTest = StringVar()
		self.optionsTest.set(valNomages[1])
		
		n = 0
		choix_nomage = []
		for n in range(len(libelles)):
			bt_test = Radiobutton(self.groupe_page3.interior(), text = libelles[n],
							   width=12,
							   variable = self.optionsTest,
							   value = valNomages[n],
							   command = self.monchoix)
			bt_test.grid(row=3, column=n+1)
		
		
	def afficheCmdVideo(self, key_command) :
		#
		#destruction des boutton de command
		if isinstance(self.button_cmd, Pmw.ButtonBox) :
			self.button_cmd.destroy()
			
		# contruire la commande 
		ffcommand = list(self.list_cmd_ffmpeg_video.values())[key_command]
	
		# Commandes 
		self.img_play 		= PhotoImage(file = "images/GArrow.gif" , height=30, width=30)
		self.img_ajouter	= PhotoImage(file = "images/openfolder.gif" , height=30, width=30)
		
		self.button_cmd = Pmw.ButtonBox(self.page2)
		bt1 = self.button_cmd.add('Ajouter',cursor='hand2',width=60, height=40, command = self.ajouterVideo,     image=self.img_ajouter)
		#command = lambda b='apply':  self.buttonPress(b))
		bt1 = self.button_cmd.add('Lancer',cursor='hand2',width=8, height=2, command= lambda p=ffcommand : self.lanceFFmpegVideo(p))
		self.button_cmd.pack()
	
		return True
	#----------------------
	#-
	#----------------------
	def afficheCmdAudio(self, key_command) :
		#
		#destruction des boutton de command
		if isinstance(self.button_cmd, Pmw.ButtonBox) :
			self.button_cmd.destroy()
			
		# contruire la commande 
		ffcommand = list(self.list_cmd_ffmpeg_audio.values())[key_command]
		print(key_command)
		print(ffcommand)
		print( list(self.list_cmd_ffmpeg_audio.values())[0])
		
		# Commandes 
		self.img_play 		= PhotoImage(file = "images/GArrow.gif" , height=30, width=30)
		self.img_ajouter	= PhotoImage(file = "images/openfolder.gif" , height=30, width=30)
		
		self.button_cmd = Pmw.ButtonBox(self.page3)
		bt1 = self.button_cmd.add('Ajouter',cursor='hand2',width=60, height=40, command = self.ajouterVideo,     image=self.img_ajouter)
		#command = lambda b='apply':  self.buttonPress(b))
		bt1 = self.button_cmd.add('Lancer',cursor='hand2',width=8, height=2, command= lambda p=ffcommand : self.lanceFFmpegAudio(p))
		self.button_cmd.pack()
	
		return True
	#------------------------------------------
	#- lance la commande ffmpeg pour la video
	#-----------------------------------------
	def lanceFFmpegVideo(self, ffcommand_in):
		"""
		"""
		# Recuperer les fichiers
		 
		for fichier in self.src_filenames :
			# Recuperer les fichiers
			fichier_in 	= fichier.decode("utf8", 'ignore')
			fichier_in 	= json.dumps(fichier_in, ensure_ascii=False)  # escape les quotes 
			#lancer le process de la commande
			
			
			# le format audio
			format_video 	= self.var_video.get().strip().lower()
			fichier_out 	= os.path.splitext(os.path.basename(fichier_in))[0] + "." + format_video.lower()
			fichier_out 	= fichier_out.replace("(", "_")
			fichier_out 	= "tmp/" + fichier_out.replace(")", "_")
			
			if fichier_in and  format_video and fichier_out :
				#
				#ffcommand = eval ('ffcommand_in % (fichier_in, format_video, fichier_out)')
				ffcommand = eval ('ffcommand_in % (fichier_in,   fichier_out)')
				returncode, data, erreur = subprocessLaunchWithoutConsole(ffcommand)
				#destruction des boutton de command
				self.button_cmd.forget()
				


	#------------------------------------------
	#- lance la commande ffmpeg pour l'Audio
	#-----------------------------------------
	def lanceFFmpegAudio(self, ffcommand_in):
		"""
		"""
		
		# Recuperer les fichiers
		for fichier in self.src_filenames :
			fichier_in 	= fichier.decode("utf8", 'ignore')
			
			fichier_in 	= json.dumps(fichier_in, ensure_ascii=False)  # escape les quotes 
			
			# le format audio
			format_audio = self.var_son.get().strip().lower()
			fichier_out 	= os.path.splitext(os.path.basename(fichier_in))[0] + "." + format_audio.lower() 
			
			# "Extraire le son de la video" 		: "ffmpeg -i %s -vn -ac 2 -ar 44100 -ab 320k -f %s %s ",
			#lancer le process de la commande
			if fichier_in and  format_audio and fichier_out :
				#-------------------------
				# lancement de la commande
				#-------------------------
				ffcommand = eval ('ffcommand_in % (fichier_in, format_audio, fichier_out)')
				try :
					returncode, data, erreur = subprocessLaunchWithoutConsole(ffcommand)
					#destruction des boutton de command
					self.button_cmd.forget()
				except Exception as err:
					pass
			
			print(ffcommand)

		#retour
		return False
		
		
		
	def verifieEtat(self):
		self.etat['text'] = self.variable1.get()
	
	def monchoix(self):
		#
		
		#print self.var_son.get()
		print (self.optionsTest.get())
		#print self.optionsSauveNomage.get()
		pass
		
	def suivant(self) :
		self.compteur_lig +=1
		return self.compteur_lig

	def rotate(self) :
		#
		fichier = str(self.src_filenames)
		if mswindows :
			cc = Converter("c:/bin/ffmpeg.exe", "c:/bin/ffprobe.exe")
		else :
			cc = Converter("/usr/bin/ffmpeg", "/usr/bin/ffprobe")
		

		conv = cc.rotate()
		for timecode in conv :
			message =  "Rotatting (%f) ...\r" % timecode
			self.suivis.insert(self.suivant(), message)
			pass 
		"""
		command = "c:/bin/ffmpeg.exe -i e:/python/convertor/test1.ogg -vf rotate=90 e:/python/convertor/output.ogg"
		#command = "c:/bin/ffprobe.exe e:/python/convertor/test1.ogg"
		
		logger.debug('Spawning ffmpeg with command: ' + ' '.join(command))
		#
		timeout = 10
		if timeout:
			def on_SIGTERM(*_):
				signal.signal(signal.SIGTERM, signal.SIG_DFL)
				raise Exception('timed out while waiting for ffmpeg')
			signal.signal(signal.SIGTERM, on_SIGTERM)

		returncode, data, erreur = subprocessLaunchWithoutConsole(command)
	
		print "retour de popen ..." + str(data) + erreur
	
		"""
	#-----------------------------
	#- 
	#----------------------------
	def converM2tsToAvi(self):
		"""
		converti le format fichier de la freeBox .m2tsi au format avi (mpeg4)
		"""
		self.bprogress  = BarreProgression(None, 3)
		self.bprogress.start()
		
		fichiers_source = self.src_filenames
		#print "mes fichiers video saisi ...%s" % join(fichiers_source, "; ")
		
		if fichiers_source :
			for video in fichiers_source :
				self.bprogress.next_pas()
				threading.Thread(None, self.convert_M2TS_to_avi, None, [video]).start()
				time.sleep(2)
				#self.convert_M2TS_to_avi(video)
				#a.start()
				
		
		self.bprogress.arreter()				
		return True
	
	
	#-----------------------------
	#- 
	#----------------------------
	def convert_M2TS_to_avi(self, fichier_source=""):
		"""
		If you want to convert the recorded files at full HD resolution,
		use the following command:
		ffmpeg -i inputfile.m2ts -deinterlace -sameq outputfile.avi
		
		#video_in = unicode(u'%s' % self.src_filenames, 'utf-8')
		#video_in = u"%s" % self.src_filenames
		#video_in = self.src_filenames.decode("utf8", 'ignore')
		#
		#video_in = u"%s" % unicode(fichier_source)
		"""
				
		# fichier source
		repertoire 		= os.path.dirname(fichier_source)
		basename_video_source 	= os.path.basename(fichier_source)
		
		#fichier_source = re.escape(basename_video_source) # escape les cataere accentue
		#print "fichier avant %s" %  fichier_source
		fichier_source 		= os.path.join(repertoire, fichier_source )
		

		basename_video_source = json.dumps(basename_video_source, ensure_ascii=False)  # escape les quotes 
		
		
		# fichier dest out
		t_timestamp =  long(time.time()) # un compteur
		fic_out = re.findall("[a-zA-Z0-9]+", basename_video_source)
		fic_out = join(fic_out, "")
		
		video_out =   json.dumps(fic_out[:50] , ensure_ascii=False) + "_" + str(t_timestamp)  
		
		#print "le fichier basename_video_source =  %s " %  basename_video_source
		#print "le fichier en sortie =  %s " %  video_out
		#------------------------------
		# preparer la commande
		#-------------------------------
		
		if os.path.isfile (fichier_source) :
			# delete fichier de sortie
			if os.path.isfile(video_out) :
				#-----------------------------
				os.remove(video_out)
				
			if mswindows :
				commande = "c:/bin/ffmpeg.exe -i '%s'  -deinterlace -sameq '%s'" % (fichier_source, video_out)
			else :
				
				"""							
				==> format xvid full resolution ==>
				ffmpeg -i inputfile.m2ts -threads 0 -deinterlace -f avi -r 25 -vcodec libxvid -vtag XVID
				-aspect 16:9 -maxrate 1800k -b 1500k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis -aic -cmp 2 -subcmp 2 -g 300 -acodec
				libmp3lame -ar 48000 -ab 128k -ac 2 outputfile.avi 
				
				==> codage en mkv(h264) resoltion 1440x1080
				ffmpeg', '-i', 'monolitique.avi', '-acodec', 'libmp3lame', '-ac', '2', '-ar', '11025', '-vcodec', 'libx264', '-r', '15',
				'-s','1440x1080', '-aspect', '1440:1080', '-f', 'avi', '-y', u'/home/aziz/dev/python/convertor/outmonolitiqu_1393583076mkv
				-map 0:2 permet de choisir la piste g encoder.
				
				ffmpeg -i /home/aziz/dev/python/convertor/in/monolitique.avi -acodec libmp3lame -ac 2 -ar 11025 -vcodec libx264 -r 15 -s '1440x1080' -aspect 16:9 -f avi -y 	/home/aziz/dev/python/convertor/out/onolitiqueavi.avi 
				
				-map 0:2 permet de choisir la piste g encoder.
				-vn on extrait aucune piste video (on ne conserve que la piste audio)
				-sn on extrait aucune piste de sous-titre (on ne conserve que la piste audio)
				-aq 3 permet de choisir la qualite du son, plus la valeur est grande, meilleur est la qualite. Ce parametre va de 1 g 10.
				-ac 2 permet de specifier le nombre de canaux voulu (2 pour du stereo, 6 pour du 5.1, etc.), cette option n'est pas obligatoire.
				-f forcer le format audio
				- request_channels canal desire 
				
				- a 3 permet de choisir la qualite du son.
				– audiostream 2 permet de choisir la piste son g extraire. Pour avoir la bonne langue, choisissez la piste qui vous concerne.

				ffmpeg -i in/Lesmonolithes.avi -acodec libmp3lame -ac 1 -aq 10   -ar 11025 -vcodec libx264 -r 15 -s '1440x1080' -aspect 16:9 -f avi -y -f avi -vlang fr -alang fr out/toto.ogg

				"""
				fichier_source 	= json.dumps(fichier_source, ensure_ascii=False)  # escape les quotes # escape les cataere accentue
				
				fichier_out 	= json.dumps(fic_out, ensure_ascii=False) + ".avi"
				
				#
				
				options = self.getOptions()
				format_video = self.label_format_video['text'].lower()
				format_video = format_video.strip().lower()
				extension = format_video
				
				fichier_out =  u"%s/%s.%s" % (self.var_environnement['DIRDEST'],  fic_out, extension)
				
				
				codec_video = self.label_codec_video['text'].lower()
				codec_video =  codec_video.strip()
				
				format_audio = self.label_audio['text'].lower() 
				format_audio = format_audio.strip() 
		
				#  definition saisi
				definition_video = self.label_definition['text'].lower()
				t_definition_video = definition_video.split("x")
				d_width = t_definition_video[0]
				d_height =  t_definition_video[1]
				
				# 1/ command en codec mkv (h264) construit a partir de la saisie en utilisateur 
				#commande1 = self.getCommandeFFmpeg(fichier_source, format_video, format_audio, codec_video, d_width, d_height)
				canal = self.canaux_son.get()
				#lig_cmd = "ffmpeg -i %s -vcodec libx264 -ar 11025  -r 15 -s '1440x1080' -aspect 16:9  -acodec libmp3lame -ac 2 -aq 10 -request_channels %s -f %s -vlang fr -alang fr -slang fr -y %s"  % (fichier_source.decode("utf8", 'ignore'),  canal, format_video,   fichier_out.decode("utf8", 'ignore'))
				lig_cmd = "ffmpeg -i %s -vcodec libx264 -ar 11025  -r 15 -s '1440x1080' -aspect 16:9  -acodec libmp3lame -ac 2 -aq 10 -request_channels %s  -vlang fr -alang fr -slang fr -y %s"  % (fichier_source.decode("utf8", 'ignore'),  canal,  fichier_out.decode("utf8", 'ignore'))
				# 2/ commande traitement sans compression -sameq
				commande2 = "/usr/bin/ffmpeg -i %s -deinterlace -sameq %s" % (fichier_source.decode("utf8", 'ignore'),    fichier_out.decode("utf8", 'ignore'))
				

			returncode, data, erreur = subprocessLaunchWithoutConsole(lig_cmd)
			
		print("la commande =  %s " % lig_cmd)
		
		return True
		
	#--------------------------------------------------
	# recuprer les options saisi par l'user
	#--------------------------------------------------
	def getOptions(self):
		"""
		recuprer les options saisi par l'user
		"""
		format_video = self.label_format_video['text'].lower()
		format_video = format_video.strip() 
		
		codec_video = self.label_codec_video['text'].lower()
		codec_video =  codec_video.strip()
		
		format_audio = self.label_audio['text'].lower() 
		format_audio = format_audio.strip() 

		#  definition saisi
		definition_video = self.scrol_def.get()
		t_definition_video = definition_video.split("x")
		d_width = t_definition_video[0]
		d_height =  t_definition_video[1]
		
		options  = {
			'format': format_video,
			'audio': {
			    'codec': 	format_audio,
			    'samplerate': 11025,
			    'channels': 2
			},
			'video': {
			    'codec'	: codec_video,
			    'width'	: d_width,
			    'height'	: d_height,
			    'fps'	: 15,
			    'mode' 	: '16:9',
		}}
		"""
		# Only copy options that are expected and of correct type
		# (and do typecasting on them)
		for k, v in opts.items():
			if k in self.encoder_options:
				typ = self.encoder_options[k]
				try:
				   safe[k] = typ(v)
				except:
				   pass
		"""
		return options
		
	#--------------------------------------------------
	# format nom du fichier de sortie
	#--------------------------------------------------
	def formate_nomfichier(self, basename_video_source):
		# fichier dest out
		t_timestamp =  long(time.time()) # un compteur
		fic_out = re.findall("[a-zA-Z0-9]+", basename_video_source)
		fic_out = join(fic_out, "")
		
		video_out =   json.dumps(fic_out[:50] , ensure_ascii=False) + "_" + str(t_timestamp)
		fichier_out 	= json.dumps(fic_out, ensure_ascii=False) + ".avi"
		extension = u"avi"
		#
		fichier_out =  u"%s/%s.%s" % (self.var_environnement['DIRDEST'],  fic_out, extension)
		#
		return fichier_out
	#--------------------------------------------------
	#
	#--------------------------------------------------	
	def infoFormat(self, fichier) :
		mswindows = (sys.platform == "win32")
				
		if mswindows :
			cc = Converter("c:/bin/ffmpeg.exe", "c:/bin/ffprobe.exe")
		else :
			cc = converter.Converter("/usr/bin/ffmpeg", "/usr/bin/ffprobe")
			
		# recherche des proprite de la video ou du mp3
		#---------------------------------------------
		self.info = cc.probe(fichier)
		if self.info :
			msg = "Traitement du fichier : %s \n"  % fichier  	# fichier en traitement
			self.afficheInfos(msg, self.suivant())
			msg = "format : %s "  % 	self.info.format   	# for example 'ogg'
			self.afficheInfos(msg, self.suivant())
			self.info.format.duration = float(self.info.format.duration)
			if self.info.format.duration > 3600 :
				duree = self.info.format.duration / 3600
				msg ="duree : %f " % duree
				self.afficheInfos(msg, self.suivant())
			
			elif self.info.format.duration > 60 :
				duree = self.info.format.duration / 60
				reste = self.info.format.duration - abs(self.info.format.duration)
				reste = (reste % 60) / 100
				duree = duree + reste
				msg ="duree : %f " % duree
				self.afficheInfos(msg, self.suivant())	
				
			
			else :
				pass
			
			
			msg ="video codec : %s" % 	self.info.video.codec 	# 'theora'
			self.afficheInfos(msg, self.suivant())
			msg ="width : %sx%s" % 	(self.info.video.video_height, self.info.video.video_width)
			self.afficheInfos(msg, self.suivant())
			msg ="audio codec : %s" % 	self.info.audio.codec 	#  'vorbis'
			self.afficheInfos(msg, self.suivant())
		else :
			msg = "pas d\'info sur ce article %s" % fichier
			self.afficheInfos(msg , self.suivant())
	#-------------------
	#*** Parametrage
	#-------------------
	def parametrages(self) :
		#------------------------------
		#
		self.root_params = Tk();
		self.root_params.option_add('*background', BLEUAPP)
		self.root_params.option_add('*foreground', "#222")
		
		self.notebook = Pmw.NoteBook(self.root_params, 
						createcommand = None,
						lowercommand = 	None,
						raisecommand = 	None,
						hull_width 	= 450,
						hull_height 	= 540,
						)	
		
		# Pack the notebook last so that the buttonbox does not disappear
		# when the window is made smaller.
		self.notebook.pack(fill = 'both', expand = 1, padx = 5, pady = 5 )
		
		self.page1 = self.notebook.add('Parametres')
		self.page2 = self.notebook.add('Connexion')
		self.page3 = self.notebook.add('Suivi') 
		 
		self.page1.focus()
		
		# ajout dune Frame
		self.pframe1 = tkinter.Frame(self.page1, bd =1,  bg ='#FFFFFF', width=400, height=540);
		self.pframe1.pack(fill = 'both', expand = 1)
		
		self.pframe2 = tkinter.Frame(self.page2, bd =1,  bg ='#FFFFFF', width=400, height=540);
		self.pframe2.pack(fill = 'both', expand = 1)
		
		self.pframe3 = tkinter.Frame(self.page3, bd =1,  bg ='#FFFFFF', width=400, height=540);
		self.pframe3.pack(fill = 'both', expand = 1)
		
		#--------------------------------------
		#parametrages Variables environnement
		#---------------------------------------
		
		self.group_param1 = Pmw.Group(self.pframe1, tag_text=r'Parametrage Convertor')
		self.group_param1.pack(fill = 'both', expand = 0, padx = 6, pady = 6)
		self.group_param2 = Pmw.Group(self.pframe2, tag_text='Connexion')
		self.group_param2.pack(fill = 'both', expand = 0, padx = 6, pady = 6)
		
		
		# ---------------------------------------------
		# charger le tableau des variables environnement
		# ---------------------------------------------
		ind = 0
		username = self.username
		
		for cle in   self.var_environnement :  # apartir de du fichier xml
			#
			Label(self.group_param1.interior(), text= cle).grid(row=ind, column=0)
			self.tab_entry[cle]= Entry(self.group_param1.interior(), width=60, bg='white')
			#self.tab_entry[cle].config(bg="#FFFFCC")
			#self.tab_entry[cle].config(state = tkinter.DISABLED)
			
			# si n'est pas dans le tableau on le rajoute
			if self.var_environnement.has_key(cle) :
				self.tab_entry[cle].insert(0, self.var_environnement[cle])
			
			# username 
			if cle == 'USERNAME' :
				self.tab_entry[cle].delete(0, "end")
				self.tab_entry[cle].insert(0, str(os.getenv("USERNAME")))
				
			rubrique_claire = [ 'DIRSRC', 'HOMEAPP', 'DIRDEST', 'TRACE']
			if cle not in rubrique_claire :
				self.tab_entry[cle].config(state = "readonly")

			if cle == 'HOMEAPP' :
				#
				self.tab_entry['HOMEAPP'].bind('<KeyPress>', lambda event : self.update(event, 'HOMEAPP'))

			
			self.tab_entry[cle].grid(row=ind , column=1)
			#print type(self.tab_entry[cle])
			ind = ind +1
			## activation debugage
		
		
		#-----------------------------
		#Les different choix
		#-----------------------------
		## choix de type de Format.
		libelles = ["Nomage IDEM", "Nomage Auto"]
		valNomages = ["I", "A"]
		
		 
		self.optionsSauveNomage = StringVar()
		self.optionsSauveNomage.set(valNomages[1])
		
		group_choix = Pmw.Group(self.pframe1, tag_text='Nomage de fichier de sortie')
		group_choix.pack(fill = 'both', expand = 0, padx = 6, pady = 6)
		
		n = 0
		choix_nomage = []
		for n in range(2):
			choix_nomage.append(Radiobutton(group_choix.interior(), text = libelles[n],
							   width=12, variable = self.optionsSauveNomage,
							   value = valNomages[n], command = self.monchoix))
			choix_nomage[n].grid(row=0, column=n+3)
		
		
			
		# ---------------------------------------------
		# charger le tableau des variables environnement
		# ---------------------------------------------
		# Connexion

		self.canvas_bicolor_r = Canvas(self.group_param2.interior(), width=15, height=15, cursor='hand2')
		self.canvas_bicolor_r.create_oval(1, 1, 15, 15, outline="white", fill='#f00', width=1)
		self.canvas_bicolor_r.grid(row=0, column= 0)
		
		self.canvas_bicolor_v = Canvas(self.group_param2.interior(), width=15, height=15, cursor='hand2')
		self.canvas_bicolor_v.create_oval(1, 1, 15, 15, outline="white", fill='#000', width=1)
		self.canvas_bicolor_v.grid(row=0, column= 1, padx=22)

		#-------------------------
		#- Info Suivi 
		#-------------------------
		
		group_suivi = 	Pmw.Group(self.pframe3, tag_text='Traces suivi')
		group_suivi.pack(fill = 'both', expand = 0, padx = 6, pady = 6)
		self.suivis = 	Listbox(group_suivi.interior())
		ascenseur = 	Scrollbar(group_suivi.interior())

		ascenseur.config(command = self.suivis.yview)
		self.suivis.config(yscrollcommand = ascenseur.set)
		self.suivis.config(background='black', foreground='green')
		self.suivis.config(height = 20, width = 65)
		self.suivis.insert(1 , '------------ traces erreurs appli --------------')
		#lecture du fichier trace
		if(os.path.isfile("trace.log")) :
			fs = open("trace.log", "r")
			lignes_traces = fs.readlines()
			fs.close()
			ind = 0
			for ligne in lignes_traces :
				ind +=1
				ligne = ligne.strip()
				ligne = ligne.strip('\t')
				self.suivis.insert(ind , ligne)
				
		
		self.suivis.grid(row=0, column=0) 
		ascenseur.grid(row=0, column=2)
		#buttonBox = Pmw.ButtonBox(self.group_param3.interior())
		buttonBox = Pmw.ButtonBox(self.pframe3)
		buttonBox.add('Rafraichir', 		width=12, command=self.refreshSuivi,		cursor='hand2')
		buttonBox.add('Reset Log', 		width=12, command=self.resetFichierLog, 	cursor='hand2')
		
		buttonBox.pack()
		
		
		#buttonBox = Pmw.ButtonBox(self.group_param3.interior())
		buttonBox = Pmw.ButtonBox(self.root_params)
		
		#buttonBox.add('Defaut', 	width=12, command=self.getParametrageDefault,   	cursor='hand2')
		buttonBox.add('Controle', 	width=12, command=self.controleParametres, 		cursor='hand2')
		buttonBox.add('Annuler', 	width=12, command=self.root_params.destroy, 		cursor='hand2')
		buttonBox.add('Enregistrer', 	width=12, command=self.saveParametres, 			cursor='hand2')
		 
		buttonBox.pack()
	#-----------------------------
	# update l'ecran suivi
	#-----------------------------	
	def refreshSuivi(self) :
		#lecture du fichier trace
		self.suivis.delete(0, 'end')
		if(os.path.isfile("trace.log")) :
			fs = open("trace.log", "r")
			lignes_traces = fs.readlines()
			fs.close()
			ind = 0
			for ligne in lignes_traces :
				ind +=1
				ligne = ligne.strip()
				ligne = ligne.strip('\t')
				self.suivis.insert(ind , ligne)
		return True
	#-----------------------------
	# mettre a blanc fichier trace
	#-----------------------------	
	def resetFichierLog(self):
		
		self.dialog4 = Pmw.MessageDialog(None, title= 'Confirmation',
			message_text = 'Souhaiter-vous mettre a  blanc le fichier trace ?',
			buttonboxpos = 'e',
			iconpos = 'n',
			icon_bitmap = 'warning',
			buttons = ('Ok',  'Fermer'),
			defaultbutton = 'Fermer');
		
		self.dialog4.withdraw()
		# Create some buttons to launch the dialogs.
		result = self.dialog4.activate()
		if (result != 'Ok') :
			return False
		
		if(os.path.isfile("trace.log")) :
			fs = open("trace.log", "w")
			self.suivis.delete(0, 'end')
			self.suivis.insert(1 , '------------ traces erreurs appli --------------')
			fs.close()
		return True
			
	
	#---------------------------------
	# show ampoule tempoi
	#-------------------------------
		
	def showTemoin(self, colfill="red") :
		if colfill == "red" :	
			self.canvas_bicolor_r.create_oval(1, 1, 15, 15, outline="white", fill="red", width=1)
			self.canvas_bicolor_r.update()
			self.canvas_bicolor_v.create_oval(1, 1, 15, 15, outline="white", fill="black", width=1)
			self.canvas_bicolor_v.update()

		else : 
			self.canvas_bicolor_v.create_oval(1, 1, 15, 15, outline="white", fill="green", width=1)
			self.canvas_bicolor_v.update()
			self.canvas_bicolor_r.create_oval(1, 1, 15, 15, outline="white", fill="black", width=1)
			self.canvas_bicolor_r.update()
	#---------------------------
	#- lance application  Convertor 
	#---------------------------
	def runApplicationConvertor(self):
		#
		#--------------------------------------------------------------------------
		# 0- controle l'existance des chemin charge dans les Variables Environnement
		#-----------------------------------------------------------------------
		
		if not self.src_filenames and not type(self.src_filenames) is list :
			return
		#
		fichier_source =  self.src_filenames[0]
		
		if not os.path.exists(fichier_source) :
			return
			#
		srcname 	= os.path.basename(fichier_source)
		

		format_video = self.label_format_video['text'].lower()
		format_video = format_video.strip() 
		
		codec_video = self.label_codec_video['text'].lower()
		codec_video =  codec_video.strip()
		
		format_audio = self.label_audio['text'].lower() 
		format_audio = format_audio.strip() 

		#  definition saisi
		definition_video = self.label_definition['text'].lower()
		t_definition_video = definition_video.split("x")
		d_width = t_definition_video[0]
		d_height =  t_definition_video[1]
		#--------------------------
		# lancement de la conversion

		self.bprogress  = BarreProgression(None, 3)
		self.bprogress.start()
		
		fichiers_source = self.src_filenames
		#print "mes fichiers video saisi ...%s" % join(fichiers_source, "; ")
		
		if fichiers_source :
			for video in fichiers_source :
				self.convertVideo(fichier_source, format_video, format_audio, codec_video, d_width, d_height)
				#self.getCommande(fichier_source, format_video, format_audio, codec_video, d_width, d_height)
				#threading.Thread(None, self.convertVideo, None, [fichier_source, format_video, format_audio, codec_video, d_width, d_height]).start()
				time.sleep(0.22)
				print("au suivant *************** !!!")
				
		
		return True
		
	#---------------------------------------
	# convert fichier video au format saisi
	#---------------------------------------
	def convertVideo(self, fichier_source, format_video, format_audio, codec_video, r_width, r_height) :
		"""
		"""
		base_name = os.path.basename(fichier_source)
		rep_source 	= os.path.dirname(fichier_source)
		nom_video  	= os.path.splitext(base_name)[0]
		
		t_timestamp =  long(time.time())
		
		if mswindows :
			cc = Converter("c:/bin/ffmpeg.exe", "c:/bin/ffprobe.exe")
		else :
			cc = Converter("/usr/bin/ffmpeg", "/usr/bin/ffprobe")
		
		
		#fic_out = "out/" + tfic_out[0][:10] + "_" + str(t_timestamp)+ "mkv"
		#fic_out = self.var_environnement['DIRDEST'] + nom_video [:30] + "_" + format_video + "_" + r_width + "X" + r_height + str(t_timestamp)+ ".mkv"
		#fic_out = os.path.normpath(os.path.join(rep_source, fic_out))
		#print fic_out
		#---------------------------------------------
		# 1- Convertir la video ou musique recuperer
		#---------------------------------------------
		fic_out = self.formate_nomfichier(base_name)
		# ratio du format
		ratio = ["4:3", "16:9"]
		
		conv = cc.convert(fichier_source , fic_out , {
			'format': format_video,
			'audio': {
			    'codec': 	format_audio,
			    'samplerate': 11025,
			    'channels': 2
			},
			'video': {
			    'codec'	: codec_video,
			    'width'	: r_width,
			    'height'	: r_height,
			    'fps'	: 15,
			    'mode' 	: '16:9',
			}})

	
		for timecode in conv:
			message =  "Converting (%f) ...\r" % timecode
			self.suivis.insert(self.suivant(), message)
			self.bprogress.next_pas()
			pass 
	
		#stop snipper
		self.bprogress.arreter()
	
	def getCommandeFFmpeg(self, fichier_source, format_video, format_audio, codec_video, r_width, r_height) :
		#
		base_name 	= os.path.basename(fichier_source)
		rep_source 	= os.path.dirname(fichier_source)
		nom_video  	= os.path.splitext(base_name)[0]
		#
		fic_out = self.formate_nomfichier(base_name)
		
		
		if mswindows :
			cc = Converter("c:/bin/ffmpeg.exe", "c:/bin/ffprobe.exe")
		else :
			cc = Converter("/usr/bin/ffmpeg", "/usr/bin/ffprobe")
		#--------------------
		mesOptions  = {
			'format': format_video,
			'audio': {
			    'codec': 	format_audio,
			    'samplerate': 11025,
			    'channels': 2
			},
			'video': {
			    'codec'	: codec_video,
			    'width'	: r_width,
			    'height'	: r_height,
			    'fps'	: 15
			}}
		
		options = cc.getOptions(fichier_source , fic_out , mesOptions);
		#		
		cmdes = cc.ffmpeg.getCommande(fichier_source , fic_out , options)
		#print options
		"""
		#['-an',   '-vcodec', 'libx264', '-r', '15', '-s', '1440x1080', '-aspect', '1440:1080', '-f', 'avi', '-pass', '1', '-acodec', 'libmp3lame', '-ac', '2', '-ar','11025'
		#['-vcodec', 'libx264', '-r', '15', '-s', '1440x1080', '-aspect', '1440:1080', '-f', 'avi', '-pass', '2']
		==> codage en mkv(h264) resoltion 1440x1080
				ffmpeg', '-i', 'monolitique.avi', '-acodec', 'libmp3lame', '-ac', '2', '-ar', '11025', '-vcodec', 'libx264', '-r', '15', '-s',
				'1440x1080', '-aspect', '1440:1080', '-f', 'avi', '-y', u'/home/aziz/dev/python/convertor/outmonolitiqu_1393583076mkv
		/usr/bin/ffmpeg -i /home/aziz/dev/python/convertor/in/monolitique.avi -acodec libmp3lame -ac 2 -ar 11025 -vcodec libx264 -r 15 -s 1440x1080 -aspect 16:9 \
		-f avi -pass 2 /home/aziz/dev/python/convertor/out/monolitiqueavi.avi
		"""		
		commande = "/usr/bin/ffmpeg -i %s %s %s" % (fichier_source, join(cmdes, ' '), fic_out)
		print(commande)
		
		#
		return commande
	
	##########################
	# sauvegarde de la config
	###########################
	def saveParametres(self) :
		#
		maintenant = datetime.now()
		date_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
		t_timestamp =  long(time.time())
		t_id = "PM_" + str(t_timestamp)
		
		self.dialog3 = Pmw.MessageDialog(None, title= 'Confirmation',
			message_text = 'Souhaiter-vous Enregistrer cette config ?',
			buttonboxpos = 'e',
			iconpos = 'n',
			icon_bitmap = 'warning',
			buttons = ('Ok', 'Annuler', 'Close'),
			defaultbutton = 'Close');
		
		self.dialog3.withdraw()
		# Create some buttons to launch the dialogs.
		result = self.dialog3.activate()
		if (result != 'Ok') :
			return False
		
		#----------------------------------------------------------------------------
		# 1- test si config user existe ==> on la supprime et on remplce par la new
		#---------------------------------------------------------------------------
		if searchConfigUserFromFileXml(self.username) :
			#Suppression 
			deleteConfigUserFromFileXml(self.username)
		
		#----------------------------------------------------------------------------
		# 2- creer l'entete si le fchier n'existe pas sinon on recharge fichierData
		#---------------------------------------------------------------------------		
		fichierData = os.getcwd() + "/config/param.xml"
		if not os.path.isfile(fichierData) :
			#--------------------------------------------------------------------
			# si le fichier param n'existe pas je le creer avec une entete xml 
			#-----------------------------------------------------------------
			xfout  = open(fichierData, 'w', 'utf-8')
			enteteXML = """<?xml version="1.0" encoding="UTF-8"?><ROOT></ROOT>"""
			xfout.write(enteteXML)
			#on clos
			xfout.close()
			
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		#----------------------------------------------------------------------------
		# 3- creer les balises config username 
		#---------------------------------------------------------------------------	
		#**********************************************************
		new_username	= createElemntXml(xmldoc, 'PARAM')
		username_id = xmldoc.createAttribute('ID')
		username_id.nodeValue = str(t_id)
		new_username.setAttributeNode(username_id)
		
		username_created = xmldoc.createAttribute('CREATED')
		username_created.nodeValue = str(date_complet)
		new_username.setAttributeNode(username_created)

		top_elem = xmldoc.documentElement
		ind = 0		 
		## ajout d'une ligne xml
		#if not( self.tab_entry.has_key(cle)) :
		cles = self.tab_entry.keys()
		ligne = ""

		self.vars_xml = ['TRACE','DIRSRC', 'DIRDEST']
	
		
		for elem in self.var_environnement_default.keys() :
			## ajout d'une sequence a la racine
			ind = ind + 1
			valeur_input = self.tab_entry[elem].get()
			#Replace les slash en fin de chaine
			valeur_input = valeur_input.rstrip('/')
			valeur_input = valeur_input.rstrip('\\')
			
			#self.tab_entry['HOME0'].delete(0,"end")
			#self.tab_entry['HOME0'].insert(0, home_0)
			
			# remplacer les \ par "/"
			valeur_input = valeur_input.replace('\\', '/')
			ligne = createElemntXml(xmldoc, elem, valeur_input)
			# Ajout de la ligne a la racine
			new_username.appendChild(ligne)
			
		#-----------------------------------------------------------------
		# 4-ajout new user sur le noeud users et enregistrement du contenu
		#-----------------------------------------------------------------
		root[0].appendChild(new_username)
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		## fermeture des flux fichiers
		afout.close()
		#recharge les variables
		self.chargeFichierXmlParam()
		#-------------------------------------
		## 5-fermeture de la fentre paramettrage
		#-------------------------------------
		self.root_params.destroy()
		return True


	

	def update(self, event, cle):
		#
		username = str(os.getenv("USERNAME"))
		
		rubrique_jumeaux_1 = ['HOMEAPP']
		 	
		success=True
		try:
		    x_saisi = str(self.tab_entry[cle].get())
		    
		    		     
		except ValueError:
			success=False
		
		if success:
			
			if cle == 'HOMEAPP' :
				home_0 = self.tab_entry['HOMEAPP'].get()
				# on supprime les slashs en fin chaine
				x_saisi = x_saisi.rstrip(chr(92))
				x_saisi = x_saisi.rstrip('/')
				
				

	#---------------------------------
	# edition fichier config
	#-------------------------------
	def editerFichier(self, nom_fichier) :
		
		my_env = os.environ #env actuelle
		argument= os.getcwd() + "/out/" +  nom_genere
		commande = "notepad.exe "
			
		#print commande + argument	
		p = subprocess.Popen( commande + argument, env=my_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
		outputlines = p.stdout.readlines()
		#print outputlines
		#p.wait()
	#---------------------------------
	# fentere infos 
	#-------------------------------

	def afficheInfos(self, msg,  lig=None) :
		#
		if lig :
			if lig == -1 :
				self.suivis.delete(0, END) 
			self.suivis.insert(lig, msg) 
		else :
			self.suivis.delete(0, END) 
			self.suivis.insert(0, msg) 
		
	#---------------------------------
	# show ampoule tempoi
	#-------------------------------
		
	def showTemoin(self, colfill="red") :
		if colfill == "red" :	
			self.canvas_bicolor_r.create_oval(1, 1, 15, 15, outline="white", fill="red", width=1)
			self.canvas_bicolor_r.update()
			self.canvas_bicolor_v.create_oval(1, 1, 15, 15, outline="white", fill="black", width=1)
			self.canvas_bicolor_v.update()

		else : 
			self.canvas_bicolor_v.create_oval(1, 1, 15, 15, outline="white", fill="green", width=1)
			self.canvas_bicolor_v.update()
			self.canvas_bicolor_r.create_oval(1, 1, 15, 15, outline="white", fill="black", width=1)
			self.canvas_bicolor_r.update()


	def apropos(self) :
		##
		msg = """
		start Convertor  Version 0.99
		version library OCI Oracle 10g
		Powered by bdelaziz SADQUAOUI  Lyon
		Created by Abdelaziz Sadquaoui (asadquaoui@atlass.fr)
		Support : http://www.support.atlass.fr
		Copyright Abdelaziz Sadquaoui © 2012 - 2013
		"""
		messages = Pmw.MessageDialog(None, title = 'A propos', message_text = msg);
		messages.show();
			
	
	##---------------------------------
	## viewer de Contenue fichier 
	##---------------------------------
	def viewContenueFile(self, conteneur, fichier=None) :
		
		if fichier and not os.path.isfile(fichier) :
			tkMessageBox.showerror("Erreur ", u"Fichier %s introuvable" % fichier)
			return False
		
		elif not fichier :
			return False
		
		if not conteneur :
			self.root_view = Tk();
			conteneur = self.root_view
		
			 
		self.view_texte = tkinter.Text(conteneur, bg='white',
				       foreground='blue',font = 'Calibri 10 bold', width=80 )
		scrl = Scrollbar(conteneur, command=self.view_texte.yview)
		scrl.pack(side='right')
		self.view_texte.config(yscrollcommand=scrl.set)
		self.view_texte.pack(fill = 'both', expand = 0, padx = 6, pady = 6)
		#---------------------------------
		# lire le fichier et l'inserer
		ff = open(fichier, 'r')
		traces = ff.readlines()
		for ligne in traces :
			ligne = ligne.strip()
			ligne.encode('utf-8')
			ligne += "\n"
			self.view_texte.insert(INSERT ,ligne)
		#self.view_texte.insert(END , "end ...")
		
		return True
	
	def ajouterVideo(self) :
		"""
		self.repfic = tkFileDialog.askopenfilename(title="Ouvrir le fichier:", initialdir=self.rep, \
		initialfile = self.fic, filetypes = [("Fichiers Python","*.py;*.pyw"), ("All", "*")]) 
		if len(self.repfic) > 0:
		self.rep=os.path.dirname(self.repfic)
		self.fic=os.path.basename(self.repfic)
		"""
		#ajouter  = BtParcourir(self.group_sources.interior())
		#ajouter.afficheParcourir(2, 1)
		
		 # define options for opening or saving a file
		self.file_opt = options = {}
		options['defaultextension'] = '.avi'
		#options['filetypes'] = [('all files', '*.*')]
		options['filetypes'] = [("Fichiers Video","*.mp4 *.avi *.wma *.flv *.mpeg *.mp3 *.m2ts"), ("*.avi *.mp3"), ("All", "*")]
		
		options['initialdir'] = os.path.dirname(os.path.abspath(__file__))
		options['initialdir'] = self.var_environnement['DIRSRC']
		options['initialdir'] = "~/Vidéos"
		#options['initialfile'] = os.path.abspath(__file__)
		options['parent'] = self.group_options.interior()
		options['title'] = 'saisir les video sources '
		options['multiple'] = 1
		
		#
		#fic_local , self.src_filenames = askopenfilename(**options)
		#------------------------------------
		#- charges les fichier saisi
		#------------------------------------
		lesfichiers  = askopenfilenames(**options)
		
		
		lesfichiers = list(lesfichiers)
		self.src_filenames = []
		for elem in lesfichiers:
			self.src_filenames.append(elem.encode("utf-8"))
			#prob de la video 
			self.infoFormat(elem)
		
		return self.src_filenames
		 

	# assembler des fichiers videos venant d'un portable
	def concat_videos(self) :
		mpdir = tempfile.mkdtemp()
		log = logging.getLogger('concat_decoder')
		tmpdir =  os.getcwd() + "/tmp" 
		log.info('Created temp dir ' + tmpdir + '.')
		indir = os.getcwd() + '/in'
		
		INPUT_EXT = '.mp4'
		OUT_EXT = '.ts'
		RESULT_FILE = os.getcwd() + '/out' + OUT_EXT
		# recupere une intro au meme format
		#ffmpeg -i diaposMariage_2016mix.mp4  -ss 00:00:00 -t 00:00:05 -s 480x852 out/entree.mp4

		
		log.info('### MOVs -> MPGs')
		#self.src_filenames.sort(None, None, reverse=True)
		for infile in self.src_filenames :
			fichier_in 	= infile.decode("utf8", 'ignore')

			if infile.endswith(INPUT_EXT):
				outfile = tmpdir + '/' + os.path.basename(infile) + OUT_EXT
				#cmd = 'ffmpeg -i ' + infile + ' -qscale:v 1 '  + outfile
				#cmd = 'ffmpeg -i ' + infile + ' -c copy -vbsf h264_mp4toannexb '  + outfile
				cmd = 'ffmpeg -i ' + infile + ' -c copy -vbsf h264_mp4toannexb '  + outfile
				os.system(cmd)
				log.info(cmd)

		log.info('### MPGs -> OUT.MPG')
		files = ''
		tmp_videos = os.listdir(tmpdir)
		tmp_videos.sort()
		for infile in tmp_videos:
			if infile.endswith(OUT_EXT):
				#infile = tmpdir + '/' + infile
				infile = os.path.basename(infile)

				files = files + 'tmp/' + infile + '|'
		
		#cmd = 'ffmpeg -i concat:"' + files + '" -c copy ' + RESULT_FILE
		#cmd = 'ffmpeg -i concat:"' + files + '" -c copy -absf aac_adtstoasc ' + 'video_out.ts'
		cmd = 'ffmpeg -i concat:"' + files + '" -c copy -absf aac_adtstoasc ' + 'out/video_out.mp4'
		os.system(cmd)
		log.info('RESULT=' + cmd)
		### Clean
		#log.info('Removing temp dir ' + tmpdir + '...')
		#shutil.rmtree(tmpdir)
		#log.info('DONE')

	def concat_fichiers_audio(self):
		"""
		# ==> fonctionne avconv -i "concat:001.mp4|002.mp4|003.mp4" -c copy full.mp4
		# a partir d'une liste de fichiers infic.txt==> avconv  -f h264 concat -i infic.txt   -c copy -bsf:a aac_adtstoasc  test_all.mkv
		# ok fusionner plusieurs mp3 ==>  avconv -i "concat:YebadOuNavdou.mp3|TafatDdunitIw.mp3" -c copy out.mp3
		'fusionner un fichier audio et un fichier video pour creer une video avec une piste sonore' :
		"ffmpeg -i son.wav -i video.yuv out.mpg",
		"""
		INPUT_EXT = "mp3"
		files = ""
		
		for infile in self.src_filenames :
				fichier_in 	= infile.decode("utf8", 'ignore')
	
				if infile.endswith(INPUT_EXT):
					infile = os.path.basename(infile)
					files = files +   infile + '|'
		
		cmd = "avconv -i " + files + " -c copy out.mp3"
		os.system(cmd)
		log.info('RESULT=' + cmd)


#########################
## Main programme 
#########################
if __name__ == '__main__':

	font='Fixed'                  # all text (Label, Button, Listbox....  
	bg='grey86'                   # all backgrounds (Frame, Button etc)  
	tbg='white'                   # Text backgrounds (Entry, Listbox,Text)
	fg='black'                    # All foreground text 
	sbg='navy'                    # selected background
	sfg='white'                   # selected foreground 
	abg='grey77'                  # active background
	afg='black'                   # active foreground
	#BACKGROUND(silver)  =  "#C0C0C0" # Default background
	BACKGROUND  =  "#dfdfdf" # Default background
	#BACKGROUND  =  "#b6b6b6" # Default background
	ACTIVE_FG   =  "#664400"      # Standard active foreground color
	ACTIVE_BG   =  "#ffdd77"      # Standard active background color
	TROUGH      =  "#997744"      # Standard trough color
	BLEUAPP     = '#D0E3FF'


	# all widgets
	root = tkinter.Tk();
	root.configure(width= 10, height=10)
	#root.iconbitmap("images/setup.ico")
	
	
	root.option_add('*activeBackground', abg)
	root.option_add('*activeForeground', afg)
	root.option_add('*selectBackground', sbg)
	root.option_add('*selectForeground', sfg)
	#root.option_add('*font', font) 
	
	root.option_add('*background', BLEUAPP)
	root.option_add('*foreground', "#222")

	tr = ClssStartConvertor(root)
	
	Pmw.initialise(root)
	root.config(relief=tkinter.RAISED, bd=3)
	root.title("Convertor 0.99 www.atlass.fr")
	## la bouclen d'attente evenements
	root.mainloop()
	#root.destroy()



"""
Video FormatsAPPENDIXA.List of Most Common

"Format TS" : "Un fichier TS est un fichier d'un DVD video. Un DVD video peut contenir des donnees destinees g des platines de salon ainsi que des donnees",

Codecs MPEG (Moving Pictures Expert Group ): three video formats, MPEG 1, 2, and 4.

MPEG1: Old, supported by everything (at least up to 352x240), reasonably efficient. good format for the web.

MPEG2: A version of MPEG 1, with better compression.720x480. Used in HDTV, DVD, and SVCD.MPEG4: A family of codecs, some of which are open, others Microsoft proprietary.

H.264: Most commonly used codecs for videos uploaded to the web.
Part of the MPEG4 codec.MPEG spinoffs: mp3 (for music) and VideoCD.

MJPEG (Motion JPEG): A codec consisting of a stream of JPEG images.
Common in video from digital camer as, and a reasonable format for editing videos, but it doesn't compress well, so it's not good for web distribution.

DV (Digital Video): Usually used for video grabbed via firewire off a video camera.Fixed at 720x480 @ 29.97FPS, or 720x576 @ 25 FPS.
Not very highly compressed.

WMV (Windows Media Video): A collection of Microsoft proprietary video codecs.
Since version 7, it has used a special version of MPEG4.

RM (Real Media): a closed codec developed by Real Networks for streaming video and audio.

DivX: in early versions, essentially an ASF (incomplete early MPEG4) codec inside an AVI container; DivX 4 and later are a more full MPEG 4 codec...no resolutionlimit.
Requires more horsepower to play than mpeg1, but less than mpeg2.
Hard to find mac and windows players.

Sorenson 3: Apple's proprietary codec, commonly used for distributing movie trailers(inside a Quicktime container).

Quicktime 6: Apple's implementation of an MPEG4 codec.RP9: a very efficient streaming proprietary codec from Real(not MPEG4).

WMV9: a proprietary, non MPEG4 codec from Microsoft.

Ogg Theora: A relatively new open format from Xiph.org.Dirac: A very new open format under development by the BBC.
B.List of Most Common Containers
AVI (Audio Video Interleave): aWindows'standard multimedia container.

MPEG4 Part 14 (known as .mp4):is thestandardized container for MPEG4.

FLV (Flash Video):
the format used to deliver MPEG video through Flash Player .

MOV: Apple's QuickTime container format.

OGG, OGM &OGV:open standard containers.

MKV (Mastroska):
another open specification container that you've seen if you've ever downloaded anime.
VOB(DVD Video Object ):It's DVD's standard container.

ASF:a Microsoft format designed for WMV and WMA — files can end in .

wmv

	conv = cc.convert(fichier_source , fic_out , {
	'format': 'mkv',
	'audio': {
	    'codec': 'mp3',
	    'samplerate': 11025,
	    'channels': 2
	},
	'video': {
	    'codec': 'h264',
	    'width': 720,
	    'height': 400,
	    'fps': 15
	}})
	# definition  = ["720x400", "1280x720" ]
	#
	-target type
	 Specify target file type ("vcd", "svcd", "dvd", "dv", "dv50", "pal-vcd", "ntsc-svcd", ... ). All the format options (bitrate, codecs, buffer sizes) are then set automatically. You can just type:
	#For extracting images from a video:
	ffmpeg -i foo.avi -r 1 -s WxH -f image2 foo-%03d.jpeg

	For creating a video from many images:
	ffmpeg -f image2 -i foo-%03d.jpeg -r 12 -s WxH foo.avi
	
	#You can put many streams of the same type in the output:
	ffmpeg -i test1.avi -i test2.avi -vcodec copy -acodec copy -vcodec copy -acodec copy test12.avi -newvideo -newaudio
	Filters:+
	anull            Pass the source unchanged to the output.
	aspect           Set the frame aspect ratio.
	crop             Crop the input video to x:y:width:height.
	fifo             Buffer input images and send them when they are requested.
	format           Convert the input video to one of the specified pixel formats.
	hflip            Horizontally flip the input video.
	noformat         Force libavfilter not to use any of the specified pixel formats
	 for the input to the next filter.
	null             Pass the source unchanged to the output.
	pad              Pad input image to width:height[:x:y[:color]] (default x and y:
	 0, default color: black).
	pixdesctest      Test pixel format definitions.
	pixelaspect      Set the pixel aspect ratio.
	scale            Scale the input video to width:height size and/or convert the i
	mage format.
	slicify          Pass the images of input video on to next video filter as multi
	ple slices.
	unsharp          Sharpen or blur the input video.
	vflip            Flip the input video vertically.
	buffer           Buffer video frames, and make them accessible to the filterchai
	n.
	color            Provide an uniformly colored input, syntax is: [color[:size[:ra
	te]]]
	nullsrc          Null video source, never return images.
	nullsink         Do absolutely nothing with the input video.
"""
"""
# ------------------ DOC -----------------------
 FFMPEG: Convert AVCHD (*.mts, *.m2ts) files to AVI files
Labels: command-line, ffmpeg, video
Most Camcorders including the "Canon LEGRIA HF R16" record Digital High Definition Video in full HD resolution at 50 frames (interlaced) in mts/m2ts-format.

To create more a transportable Standard definition DVD quality progressive avi file,
you can convert them with ffmpeg.

Assuming you have installed ffmpeg and all the libraries you might need,
use the following command to get the job done relatively fast.

1. Euro format: (PAL)

ffmpeg -i inputfile.m2ts -deinterlace -target pal-dvd outputfile.avi

2.American Format: (NTSC) 
ffmpeg -i inputfile.m2ts -deinterlace -target ntsc-dvd outputfile.avi

3. XVID (Computer Format @ Max Resoution / same as source)
  
ffmpeg -i inputfile.m2ts -threads 0 -deinterlace -f avi -r 25 -vcodec libxvid -vtag XVID  -aspect 16:9 -maxrate 1800k -b 1500k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis -aic -cmp 2 -subcmp 2 -g 300 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 outputfile.avi 


4. XVID (Computer Format @ Reasonable Web Resolution) 

ffmpeg -i inputfile.m2ts -threads 0 -deinterlace -f avi -r 25 -vcodec libxvid -vtag XVID -s 480x360 -aspect 16:9 -maxrate 1000k -b 700k -qmin 3 -qmax 5 -bufsize 4096 -mbd 2 -bf 2 -trellis -aic -cmp 2 -subcmp 2 -g 300 -acodec libmp3lame -ar 48000 -ab 128k -ac 2 outputfile.avi



* Note: the setting -threads 0 will use all cores available.

If you want to convert the recorded files at full HD resolution,
use the following command:

ffmpeg -i inputfile.m2ts -deinterlace -sameq outputfile.avi


For full FFmpeg manual visit: ffmpeg.org
For installation instruction on the Latest version for Ubuntu visit this forum article.

Posted: Wednesday, May 04, 2011 
"""
format_video = {
	"sqcif" :  "128x96","qcif" :  "176x144", 
	'cif' :    "352x288",
	"4cif":    "704x576", 
	"16cif":    "1408x1152",
	"qqvga":    "160x120",
	"qvga":    "320x240",
	"vga":    "640x480",
	"svga":    "800x600",
	"xga":    "1024x768",
	"uxga":    "1600x1200",
	"qxga":    "2048x1536",
	"sxga":    "1280x1024",
	"qsxga":    "2560x2048",
	"hsxga":    "5120x4096",
	"wvga":    "852x480",
	"wxga":    "1366x768",
	"wsxga":    "1600x1024",
	"wuxga":    "1920x1200",
	"woxga":    "2560x1600",
	"wqsxga":    "3200x2048",
	"wquxga":    "3840x2400",
	"whsxga":    "6400x4096",
	"whuxga":    "7680x4800",
	"cga":    "320x200",
	"ega":    "640x350",
	"hd480":    "852x480",
	"hd720":    "1280x720",
	"hd1080":    "1920x1080"
	}

"""
Si vous êtes sous linux et que vous utilisez de temps en temps ffmpeg, voici quelques lignes de commande qui vous seront surement utiles :

Obtenir toutes les infos d'une video

    ffmpeg -i video.avi

Convertir x images en une petite video. C'est images sont stockees dans le repertoire courant et s'appelles image1.jpg, image2.jpg et ainsi de suite...

    ffmpeg -f image2 -i image%d.jpg video.mpg

Convertir une video en x images... Cela generera des fichiers image1.jpg, image2.jpg...etc dans le repertoire courant. Les formats supportes sont PGM, PPM, PAM, PGMYUV, JPEG, GIF, PNG, TIFF, SGI.

    ffmpeg -i video.mpg image%d.jpg

Encoder une video pour l'iPhone ou l'iPod Touch

    ffmpeg -i source_video.avi input -acodec aac -ab 128kb -vcodec mpeg4 -b 1200kb -mbd 2 -flags +4mv+trell -aic 2 -cmp 2 -subcmp 2 -s 320x180 -title X final_video.mp4

Explications :

    Source : source_video.avi
    Codec audio : aac
    Bitrate audio : 128kb/s
    Codec video : mpeg4
    Bitrate video : 1200kb/s
    Taille : 320px par 180px
    video generee : final_video.mp4

Même chose pour la PSP

    ffmpeg -i source_video.avi -b 300 -s 320x240 -vcodec xvid -ab 32 -ar 24000 -acodec aac final_video.mp4

Explications :

    Source : source_video.avi
    Codec audio : aac
    Bitrate audio : 32kb/s
    Codec video : xvid
    Bitrate video : 1200kb/s
    Taille : 320px par 180px
    video generee : final_video.mp4

Extraire le son d'une video et en faire un MP3

    ffmpeg -i source_video.avi -vn -ar 44100 -ac 2 -ab 192 -f mp3 sound.mp3

Explications :

    Source video : source_video.avi
    Bitrate audio : 192kb/s
    Format de sortie : mp3
    Son genere : sound.mp3

Convertir un wav en mp3

    ffmpeg -i son_origine.avi -vn -ar 44100 -ac 2 -ab 192 -f mp3 son_final.mp3

Convertir un avi en mpeg

    ffmpeg -i video_origine.avi video_finale.mpg

Convertir un mpeg en avi

    ffmpeg -i video_origine.mpg video_finale.avi

Convertir un avi en gif anime non compresse

    ffmpeg -i video_origine.avi gif_anime.gif

Mixer un son et une video

    ffmpeg -i son.wav -i video_origine.avi video_finale.mpg

Convertir un avi en flv

    ffmpeg -i video_origine.avi -ab 56 -ar 44100 -b 200 -r 15 -s 320x240 -f flv video_finale.flv

Convertir un avi en dv

    ffmpeg -i video_origine.avi -s pal -r pal -aspect 4:3 -ar 48000 -ac 2 video_finale.dv

Ou encore :  ffmpeg -i video_origine.avi -target pal-dv video_finale.dv

Convertir un avi en mpeg pour les lecteurs DVD

    ffmpeg -i source_video.avi -target pal-dvd -ps 2000000000 -aspect 16:9 finale_video.mpeg

Explications :

    Format de sortie : target pal-dvd
    Taille maximum du fichier genere : ps 2000000000
    Format : aspect 16:9

Convertir un avi en divx

    ffmpeg -i video_origine.avi -s 320x240 -vcodec msmpeg4v2 video_finale.avi

Convertir un ogm en mpeg pour DVD

    ffmpeg -i film_sortie_cinelerra.ogm -s 720x576 -vcodec mpeg2video -acodec mp3 film_terminee.mpg

Convertir un avi en SVCD mpeg2 NTSC

    ffmpeg -i video_origine.avi -target ntsc-svcd video_finale.mpg

Convertir un avi en SVCD mpeg2 PAL

    ffmpeg -i video_origine.avi -target pal-svcd video_finale.mpg

Convertir un avi en VCD Mpeg 2 NTSC

    ffmpeg -i video_origine.avi -target ntsc-vcd video_finale.mpg

Convertir un avi en VCD Mpeg 2 PAL

    ffmpeg -i video_origine.avi -target pal-vcd video_finale.mpg

Encoding multipass

    ffmpeg -i fichierentree -pass 2 -passlogfile ffmpeg2pass fichiersortie-2
"""

