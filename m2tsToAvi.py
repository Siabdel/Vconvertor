# -*- coding: utf-8 -*-
# module local
import tkMessageBox
import os, string
import subprocess
from subprocess import Popen, PIPE
import signal
from string import *


list_video = """RMC Découverte - Alien Theory (L'héritage de Von Däniken) - 18-01-2014 20h52 05h13 (519).m2ts
RMC Découverte - Alien Theory (La source du mal) - 26-01-2014 01h15 45m (536).m2ts
RMC Découverte - Alien Theory (Les catastrophes climatiques) - 26-01-2014 00h30 45m (535).m2ts
RMC Découverte - Alien Theory (Les cultes du diable) - 25-01-2014 23h50 40m (534).m2ts
RMC Découverte - Alien Theory (Les dieux vikings) - 18-01-2014 23h15 02h (520).m2ts
RMC Découverte - Alien Theory (Les dieux vikings) - 25-01-2014 23h00 45m (533).m2ts
RMC Découverte - Alien Theory (Les monolithes) - 25-01-2014 22h58 02m (532).m2ts
RMC Découverte - Alien Theory (Les mystères du IIIe Reich) - 05-01-2014 00h41 44m (515).m2ts
RMC Découverte - Alien Theory (Mystérieuses reliques) - 25-01-2014 21h53 22m (529).m2ts
RMC Découverte - Alien Theory (Mystérieuses reliques) - 25-01-2014 21h53 22m (530).m2ts
RMC Découverte - Alien Theory (Stratégies secrètes) - 25-01-2014 20h56 34m (527).m2ts
RMC Découverte - Alien Theory (Stratégies secrètes) - 25-01-2014 20h56 34m (528).m2ts
RMC Découverte - Mystères des profondeurs (Tsunami et vagues scélérates) - 04-11-2013 22h53 22m (480).m2ts
RMC Découverte - Planète carnivore (L'ours polaire) - 09-11-2013 16h45 15m (483).m2ts"""

LOCAL_DIR =  os.path.dirname(os.path.abspath(__file__))


def convert_M2TS_to_avi(video_in):
    """
    If you want to convert the recorded files at full HD resolution,
    use the following command:
    
    ffmpeg -i inputfile.m2ts -deinterlace -sameq outputfile.avi
    """
    
    fichier_video =  os.path.abspath(__file__)
    #print "le fichier en entree = %s " % fichier_video

    
    if os.path.isfile (fichier_video) :
        #
        print video_in
        commande = "ffmpeg -i %s -deinterlace -sameq outputfile.avi" % str(video_in)
        returncode, data, erreur = subprocessLaunchWithoutConsole(commande)
        return True
    
    
    
def subprocessLaunchWithoutConsole(command):
    """Launches 'command' windowless and waits until finished"""
    startupinfo = subprocess.STARTUPINFO()
    
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    #traceLog("\n la commande = %s " %  command)
    
    try:
        #proc = subprocess.Popen(command , stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
        proc = subprocess.Popen(command , stdin=None, stdout=subprocess.PIPE)
        #stdout, stderr = proc.communicate(str.encode('latin1'))
        code_erreur = proc.returncode
        data 		= proc.stdout.readlines()
        erreur 		= proc.stderr.read()
        traceLog("\n stdout = %s erreur = %s" %(data, erreur))
        
        #return (proc.returncode, stdout.decode('latin1').upper() , stderr.decode('latin1').upper())
        return (proc.returncode, data , erreur.decode('latin1').upper())
    
    except Exception, message :
        #messages = "Exception %s: subprocessLaunchWithoutConsole %s" %(ex.errno, ex.strerror)
        text_messages = "Exception ***: subprocessLaunchWithoutConsole %s" %(message)
        tkMessageBox.showerror("Exception:", text_messages)
        return ("", "", message.decode('latin1').upper())

# traitement des conversion video

list_video = split(list_video, '\n')
#print "Debut de traitement %s" % list_video[2]
for elem in list_video	:
    #
    #print elem
    try :
        convert_M2TS_to_avi(elem)
    except Exception as err :
        print "il y a erreur %s" % str(err)
        
    break