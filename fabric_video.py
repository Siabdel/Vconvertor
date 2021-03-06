#!/usr/bin/python
#! -*- encoding:utf-8 -*-
from  fabric.api import local, run, cd, env, prefix, put, get, lcd, execute, env, hosts
import os

#from ilogue.fexpect import expect, expecting, run
from fabric.contrib.console import confirm, prompt
from fabric.contrib import django

django.settings_module('agenda.settings')
from django.conf import settings


# serveur OVH 51.254.101.190:8000
env.hosts = ['51.254.101.190']
env.user = 'abdel'

env.local = ['127.0.0.1']
env.prod = ['root@51.254.101.190']
env.password = 'Grutil001'
app = 'agenda'

#/path/to/project en prod
LOCAL_WORKING_DIR = '/home/abdel/Vidéo/'

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


def get_resolution_smartphone(video):
    """
    On convertie la resolution video au format smartphone 800x450 :
    lancer fab changer_resolution_smartphone:nom_video
    """
    rep = confirm("vous voulez changer la résolution a une video ?")
    if rep:
            local("avconv -i " + video + " -s 800x450 out_smartphone.mp4")


def get_resolution_pc(video):
    """
    On convertie la resolution dideo au format smartphone 800x450 :
    lancer fab changer_resolution_smartphone:nom_video
    """
    rep = confirm("vous voulez changer la résolution a une video ?")
    if rep:
            local("avconv -i " + video + " -s 1280x720 out_pc.mp4")


def concat_audio(files):
    """
    fusionner plusieurs fichiers audio en un seul a
    """
    rep = confirm("vous voulez concatener ces fichiers ?")
    if rep:
        cmd = "avconv -i concat:'" + files + "' -c copy   out_audio.mp3"
        local(cmd)
        print "command= %s" % (cmd)


def concat_rep_audio(directory, TRIE=False):
    """
    fusionner plusieurs fichiers audio en un seul a
    partir d'un répértoire
    """
    fichiers_audio = ""
    if os.path.isdir(directory):
        rep = confirm("vous voulez concatener ces fichiers ?")
        if rep:
       
            for root, dirs, files in os.walk(directory, topdown=False):
            # pour chaque fichier importer data
                files.sort(reverse=TRIE)
                #
                for fic in files :
                    print root, dirs
                    fichiers_audio +=  os.path.join(directory, fic) + "|"
                    
            # fusionner les fichiers audio
            cmd = "avconv -i concat:'" + fichiers_audio + "' -c copy   out_audio.mp3"
            local(cmd)
            print "command= %s" % (cmd)


def concat_video(video_1, video_2):
    """
    2) Merge the 2 videos Convert all to TS
    ffmpeg -i 1f.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts 1f.ts
    ffmpeg -i 2f.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts 2f.ts
    Merge
    ffmpeg -i "concat:1f.ts|2f.ts" -bsf:a aac_adtstoasc -c copy output.mp4
    """
    
    video_ext = video_1.split('.')[-1]
    
    rep = confirm("vous voulez concatener des videos ?")
    if rep:
        
        #2) Merge the 2 videos Convert all to TS
        cmd1 = "ffmpeg -i %s -c copy -vbsf h264_mp4toannexb -s 800x450 video_1.ts" % (video_1)
        cmd2 = "ffmpeg -i %s -c copy -vbsf h264_mp4toannexb -s 800x450 video_2.ts" % (video_2)

        local(cmd1)
        local(cmd2)
        
        # Merge -c copy -vbsf h264_mp4toannexb -s 800x450
        #  cmd = "ffmpeg -i concat:%s|%s -c copy -absf aac_adtstoasc  video_out.%s" % ('video_1.ts', 'video_2.ts', video_ext)
       
        cmd = "ffmpeg -i concat:'%s|%s' -c copy -absf aac_adtstoasc  video_out.%s" % ('video_1.ts', 'video_2.ts', video_ext)
        print "command= %s" % (cmd1 + '\n' + cmd2)
        local(cmd)
        



def effect_fad_atend(fichier_in):
    """
    2 videos of 4 seconds each. Need to join it with fade between them.videos are 25 fps.
    1) Add fade out (light to dark) at the end of the 1st and fade in (dark to light) at the beggining of the 2nd:
    
    ffmpeg -i 1.mp4 -y -vf fade=out:76:24 1f.mp4
    
    ffmpeg -i 2.mp4 -y -vf fade=in:0:25 2f.mp4
    76:24 mean the fade out will start frame 76 and will finish 24 frames later = 1s fade out.
    """
    
    rep = confirm("vous voulez ajouter un effect fade ?")
    if rep:
        cmd = "ffmpeg -i " + fichier_in + " -y -vf fade=out:144:255 out_fadeatend.mp4"
        local(cmd)
        print "command= %s" % (cmd)

    
#Extraire le son de la video
"""
-i “input file”
-vn “skip the video part”
-ac “audio channels”
-ar “audio rate”
-ab “audio bit-rate“ 320 kbit
-f “file format to use”

# Extraire le son de la video":"ffmpeg -i 'whatever.format' -vn -ac 2 -ar 44100 -ab 320k -f mp3 output.mp3",
#Séparer la vidéo du son -vn : désactive l’enregistrement vidéo -f : force le format de sortie (facultatif: par défaut FFMPEG choisit le format spécifié parl’extension
'Extraire le son d\'une video' : "ffmpeg -i fichier_video.avi -vn -f mp3v fichier_son.mp3",
#Séparer la vidéo du son -an : désactive l’enregistrement audio
'Récupérer uniquement le flux vidéo' :"ffmpeg -i fichier_video.avi -an -f avi fichier_sans_son.mp4",

# generer du gif animés
'générer de la même manière des gif animés' : "ffmpeg -i test.avi out.gif",
# Fusionner du son et de la video
'fusionner un fichier audio et un fichier vidéo pour creer une video avec une piste sonore' :
    "ffmpeg -i son.wav -i video.yuv out.mpg",
"""

def extraire_son(fichier_in):
    """
    Extraire le son de la video": "ffmpeg -i 'whatever.format' -vn -ac 2 -ar 44100 -ab 320k -f mp3 output.mp3",
    Extraire le son d\'une video' : "ffmpeg -i fichier_video.avi -vn -f mp3v fichier_son.mp3",
    Explications :

    Source : source_video.avi
    Codec audio : aac
    Bitrate audio : 32kb/s
    Codec vidéo : xvid
    Bitrate vidéo : 1200kb/s
    Taille : 320px par 180px
    vidéo générée : final_video.mp4

    Extraire le son d'une vidéo et en faire un MP3

    ffmpeg -i source_video.avi -vn -ar 44100 -ac 2 -ab 192 -f mp3 sound.mp3
    """
    rep = confirm("vous voulez extraire le son de la video ?")
    if rep:
        cmd = "ffmpeg -i " + fichier_in + " -vn -ac 2 -ar 44100 -ab 320k -f mp3 out_son.mp4"
        local(cmd)
        print "command= %s" % (cmd)


def extraire_video_silent(fichier_in):
    """
    #Séparer la vidéo du son -an : désactive l’enregistrement audio
    Récupérer uniquement le flux vidéo' :"ffmpeg -i fichier_video.avi -an -f avi fichier_sans_son.mp4",
    """
    rep = confirm("vous voulez extraire la video de la video ?")
    if rep:
        cmd = "ffmpeg -i " + fichier_in + " -an -f avi  out_video_seul.mp4"
        local(cmd)
        print "command= %s" % (cmd)
        
        
def extract_images_from_video(video_in, resolution):
    """
    #For extracting images from a video:
    ffmpeg -i foo.avi -r 1 -s WxH -f image2 foo-%03d.jpeg
    """
    rep = confirm("vous voulez extraire des images de la video ?")
    if rep:
        cmd = "ffmpeg -i " + video_in + " -r 1 -s " + resolution + " img-%03d.jpeg"
        local(cmd)
        print "command= %s" % (cmd)
    
    

def convertir_images_en_video(infiles):
    """
    # creation de video a partir de plusieurs images
    'Création de vidéos à partir d\'un ensemble d\'images': "ffmpeg -r 24 -b 1800 -i %02d.bmp out.mpg",
    "For extracting images from a video" : "ffmpeg -i foo.avi -r 1 -s WxH -f image2 foo-%03d.jpeg",
    for example = une serie images "mariage_0004 à mariage_0255.png" == mariage%04d
    ffmpeg -r 24 -b 1800 -i mariage_%04d.png video_out.mpg
    # *** Effectuer un screencast
    #Un screencast consiste en une capture vidéo de votre écran et FFMPEG fait ça très facilement :
    #-b : permet de régler le taux d’échantillonnage de la vidéo (cela influe sur la qualité vidéo)
    #-f : l’argument x11grab permet de spécifier qu’il faut capturer « l’écran »
    #-s : la taille (ici votre résolution)
    #-r : le nombre d’images par seconde (25 fps par défaut)
    #-i : ici le numéro de votre écran de votre serveur X11 (variable d’environnement DISPLAY)
    """
    
    rep = confirm("vous voulez creation de video a partir de plusieurs images ?")
    if rep:
        cmd = "ffmpeg -r 24 -b 1800 -i " + infiles + " video_out.mpg"
        local(cmd)
        print "command= %s" % (cmd)

def convertir_avi_en_mkv(video_in):
    """
    "Convertir fichier avi en un fichier mkv (le format Matroska)":
    "ffmpeg -i entree.avi -threads 4 -f matroska -vcodec libvpx -vb 1350000
    -rc_lookahead 16 -keyint_min 0 -g 360 -skip_threshold 0 -level 116 -qmin 15
    -qmax 30 -acodec libvorbis -ab 128k -ar 44100 -ac 2 sortie.mkv ",
    """
    rep = confirm("vous voulez convertir une video mpeg4 en mkv ?")
    if rep:
        cmd = "ffmpeg -i " + video_in + " -threads 4 -f matroska -vcodec libvpx -vb 1350000 "
        cmd += "-rc_lookahead 16 -keyint_min 0 -g 360 -skip_threshold 0 -level 116 -qmin 15 "
        cmd += "-qmax 30 -acodec libvorbis -ab 128k -ar 44100 -ac 2 video.mkv "
   
   
        local(cmd)
        print "command= %s" % (cmd)

def convertir_mp4_en_mkv(video_in):
    """
    Convertir fichier avi en un fichier mkv (le format Matroska)":
     sortie.mkv ",
    """
    rep = confirm("vous voulez convertir une video mpeg4 en mkv ?")
    if rep:
        cmd = "ffmpeg -i " + video_in + "  -f matroska  video.mkv "
   
   
        local(cmd)
        print "command= %s" % (cmd)

def rotation_video_90(video_in, direction=0):
    """
    # Pivoter la video de 90 degre a droite
    #ex/ : Pivoter la video" : "avconv -i %s -vf 'transpose=1' -codec:v libx264 -preset slow -crf 25 -codec:a copy %s",
    ex/ : Pivoter la video" : "ffmpeg -i %s -vf 'transpose=1' -vcodec  libx264 -s 480x852 -acodec copy %s",
    direction a drte = 1
    direction a gche = 0 (par defaut)
    """
    video_ext = video_in.split('.')[-1]
    
    rep = confirm("vous voulez faire une rotation de la vidéo en 90 ?")
    if rep:
        cmd = "ffmpeg -i " + video_in + " -vf 'transpose=" + direction + " -vcodec  libx264 -acodec copy video_out." + video_ext
        local(cmd)
        print "command= %s" % (cmd)

def decouper_video(video_in, debut='00:00:00', duree='00:00:05'):
    """    
    # découper un bout de video 
    #"découper un bout de video": "ffmpeg -ss 00:00:30.00 -t 00:00:25:00 -i video.flv video-new.avi" #ne marche pas bien
    #devrait te couper un bout de 25seconde après 30s du début., #
    "découper un bout de video": "avconv -i video_source.m2ts -vcodec copy -acodec copy -ss 00:00:30  -t 00:00:25 video_elvis.mp4",
    # découpage video
    #ffmpeg -i movie.mp4 -ss 00:03:56 -c copy -t 00:00:29 output.mp4
    lancer la cmd = fab decouper_video:intro.mp4, 00:00:00, 00:00:30 -f myfab.py
    """

    video_ext = video_in.split('.')[-1]
    
    rep = confirm("vous voulez découper un bout de video ?")
    if rep:
        cmd = "ffmpeg -i %s"%video_in + " -ss %s"%debut + " -c copy -t %s" % duree + " video_out.%s"%video_ext
        local(cmd)
        print "command= %s" % (cmd)

def decouper_audio(video_in, debut='00:00:00', duree='00:00:05'):
    """
    decoupage audio
    ffmpeg -i input.wmv -ss 00:00:30.0 -c copy -t 00:00:10.0 output.wmv
    ffmpeg -i input.wmv -ss 30 -c copy -t 10 output.wmv
    lancer la cmd = fab decouper_audio:intro.mp3, 00:00:00, 00:00:30 -f myfab.py
    """
    
    
    audio_ext = audio_in.split('.')[-1]
    
    rep = confirm("vous voulez découper un bout de fichier audio ?")
    if rep:
        cmd = "ffmpeg -i %s"%audio_in + " -ss %s"%debut + " -c copy -t %s" % duree + " audio_out.%s"%audio_ext
        local(cmd)
        print "command= %s" % (cmd)
        
        
def fusionner_video_audio(video_in, audio_in):
    """ 
    # Fusionner du son et de la video
    fusionner un fichier audio et un fichier vidéo pour creer une video avec une piste sonore' :
    "ffmpeg -i son.wav -i video.yuv out.mpg"
    """

    video_ext = video_in.split('.')[-1]
    
    rep = confirm("vous voulez fusionner vidéo avec audio ?")
    if rep:
        cmd = "ffmpeg -i %s -i %s out_video_mixed.%s"% (audio_in, video_in, video_ext)
        local(cmd)
        print "command= %s" % (cmd)
   
    
