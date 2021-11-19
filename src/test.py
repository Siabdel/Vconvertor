# -*- coding:utf-8 -*-
# module general
import sys, os
import pdb
# module local
from commun_helpers import subprocessLaunchWithoutConsole, createElemntXml
from commun_helpers import deleteConfigUserFromFileXml
# loggin trace
import logging

"""
cc = Converter("c:/bin/ffmpeg.exe", "c:/bin/ffprobe.exe")
info = cc.probe('e:/python/convertor/Piste01.ogg')

conv = cc.convert('e:/python/convertor/Piste01.ogg' , 'e:/python/convertor/output.mkv', {
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
    
==>

ffmpeg.exe -i e:/python/convertor/test1.ogg -acodec libmp3lame -ac 2 -ar 11025 -vcodec libx264 -r 15 -s 720x400 -aspect 720:400 
-f matroska -y /e:/python/convertor/output.mkv
###


for timecode in conv:
    print "Converting (%f) ...\r" % timecode

cmds = ['c:/bin/ffprobe.exe', '-show_format', '-show_streams', 'e:/python/convertor/test1.ogg']

Popen(cmds, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                     close_fds=True)
"""



if __name__ == "__main__":
    """
    test logg
    """
    logging.basicConfig(filename=os.path.join(os.path.curdir, __name__), filemode='w', level=logging.ERROR)
    logging.info("Ici error ....")
    logging.debug('This message should go to the log file')
    print "creer un fichier toto.log"
    logging.info('So should this')
    logging.warning('And this, too')


                     