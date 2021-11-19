# -*- coding:utf-8 -*-
# module general
import sys, os
import pdb

import Tkinter
from Tkinter import Checkbutton, Radiobutton, Scrollbar, Toplevel, Button
from Tkinter import Listbox, Label, Entry, Canvas
from Tkinter import TOP, BOTTOM, LEFT, RIGHT, YES, LEFT, RIGHT, Y
import Pmw
# fabric
from fabric.contrib.project import env
from fabric.api import roles
#from fabric.contrib.project import getcwd, env, local, cd
#from fabric.api import run, cd,  prefix, put, get, roles
# module local
# import de interface
from application import MixinTkApp
# module local
from commun_helpers import subprocessLaunchWithoutConsole, createElemntXml
from commun_helpers import deleteConfigUserFromFileXml
# loggin trace
import logging


logging.basicConfig(filename=__file__.split('.')[0] + '.log', level=logging.INFO,
                    format="%(asctime)s -- %(name)s -- %(levelname)s" )

env.hosts = ["192.168.0.15",]
env.login =	  "aziz"

env.hosts = ["192.168.0.15",]
env.login =	  "aziz"

@roles('webservers')
def list_dir_remote(dir=None):
    """docstring for list_dir"""

    dir = dir or env.cwd
    string = run("for i in %s*; do echo $i; done" % dir)
    files = string.replace("\r","").split("\n")
    return file

class ClssSynchroRep(MixinTkApp) :
    """
    Synchronise les fichiers et dossiers
    """

    def start_appli(self):
        """
        start application
        :return:
        """
        self.list_folders_tosave = []

        # affiche page 1
        self.une_source_alafois()
        # affiche page 2
        self.select_repertoire_src()

    def une_source_alafois(self):
        self.sframe = Tkinter.Frame(self.page1, bd=1, bg='#FFFFFF', width=400, height=540);
        #self.sframe.pack(side=TOP, fill='both', expand=YES)

        group_repertoires = Pmw.Group(self.page1, tag_text='Choix des répertoires ')
        group_repertoires.pack(side=TOP, expand=YES, padx=2, pady=2)

        # ouvrir sources et destination
        # options['multiple'] = 1

        self.sourceIn = Tkinter.Entry(group_repertoires.interior(), width=40)
        self.sourceIn.grid(row=0, column=1)

        dsource = Button(group_repertoires.interior(), text='Répertoire Sources', bg='#455', fg='#fff', width=20)
        # lambda x, y : x + y
        s_options = {'title': 'Ajouter un Dossier source',
                     'initialdir': self.var_environnement_default['LOCAL_DIR'],
                     'dest': self.sourceIn}

        dsource.bind('<Button-1>', lambda event: self.selectdirectory(s_options))
        dsource.grid(row=0, column=2)
        #
        self.destinIn = Tkinter.Entry(group_repertoires.interior(), width=40)
        d_options = {'title': 'Ajouter un Dossier destination',
                     'initialdir': self.var_environnement_default['REMOTE_DIR'],
                     'dest': self.destinIn}
        self.destinIn.grid(row=1, column=1)
        ddest = Button(group_repertoires.interior(), text='Répertoire Destination', bg='#455', fg='#fff', width=20)
        # lambda x, y : x + y
        rdir_default = self.var_environnement_default['REMOTE_DIR']
        ddest.bind('<Button-1>', lambda event: self.selectdirectory(d_options))
        ddest.grid(row=1, column=2)

        # button lancement
        Button(self.page1, text='Sauvegarder', width=55, height=2).pack(side=BOTTOM)

    def select_repertoire_src(self):
        # --------------------------------------
        # Selection des reperoire a sauvegarder
        # -------------------------------------
        local_dir_src = self.var_environnement_default['LOCAL_DIR']
        self.group_src = Pmw.Group(self.page2, tag_text='Sauvegarde / Synchro [%s]' % local_dir_src)
        self.group_src.pack(side=TOP, expand=YES, padx=2, pady=2)

        self.list_src = Listbox(self.group_src.interior())
        ascenseur_src = Scrollbar(self.group_src.interior())
        ascenseur_src.config(command=self.list_src.yview)
        self.list_src.grid(row=1, column=1)
        ascenseur_src.grid(row=1, column=2)

        self.list_src.config(yscrollcommand=ascenseur_src.set)
        self.list_src.config(bg="#fff", fg="#222", height=10, width=30)
        self.list_src.bind('<Double-1>', lambda event: self.selectListSrc(event))

        # charge list des reperoire source a partir du path indiquer dans la config
        self.charge_list_src()

        self.list_maselection = Listbox(self.group_src.interior())
        self.list_maselection.config(bg="#fff", fg="#33f", height=10, width=30)

        self.list_maselection.bind('<Double-1>', lambda event: self.unSelectListSrc(event))

        self.list_maselection.grid(row=1, column=3, padx=12)

        # Button lancement sauvegarde
        bt_run = Button(self.group_src.interior(), text='Ok', width=35, height=30,
                        command=self.runApplication, image=self.img_convert)
        bt_run.grid(row=1, column=4)

    def charge_list_src(self):
        """
        charge la liste des reperoires source
        dans la listbox a partir du path default
        """
        self.list_folders_home = []
        local_dir_src = self.var_environnement_default['LOCAL_DIR']
        self.list_src.delete(0, 'end')

        # listes des rep a partir de home
        dirlist = []

        for compteur, dirname in enumerate(sorted(os.listdir(local_dir_src))):
            if os.path.isdir(os.path.join(local_dir_src, dirname)):
                dirlist.append(dirname)
                self.list_src.insert(compteur, dirname)
                self.list_folders_home.insert(compteur, os.path.join(local_dir_src, dirname))

        self.list_folders_home.sort()

    def selectListSrc(self, event):
        """
        selection du dossier source
        :return ajout de la selection dans list_folders_tosave
        """
        widget = event.widget
        maselection = widget.curselection()

        if len(maselection) > 0:
            value = widget.get(maselection[0])

            try:
                self.list_folders_tosave.index(value)

            except:
                self.list_maselection.insert('end', os.path.basename(value))
                self.list_folders_tosave.insert(maselection[0], value)

        return True

    def unSelectListSrc(self, event):
        """
        deselection un dossier
        """
        widget = event.widget
        maselection = widget.curselection()

        if len(maselection) > 0:
            value = widget.get(maselection[0])
            self.list_maselection.delete(maselection[0])
            self.list_folders_tosave.pop(maselection[0])

        return True

    # --------------------------------
    # - lance application  Convertor
    # -------------------------------
    def runApplication(self):
        """
        lancement de l'application de Synchronise les fichiers et dossiers
        """
        # for elem in self.list_folders_tosave:
        fichiers_src = ' '.join(self.list_folders_tosave)
        self.var_environnement_default['RUN_TEST'] = 'n'
        self.var_environnement_default['FICHIERS_SRC'] = fichiers_src

        command = "sshpass -p $(cat FILE) rsync --progress --log-file=remote_rsync.log -e 'ssh '" \
                  " -av%(RUN_TEST)s %(FICHIERS_SRC)s %(REMOTE_LOGIN)s@%(REMOTE_IP)s:%(REMOTE_DIR)s" \
                  %   (self.var_environnement_default)

        logging.info('Rsync with command: ' + ' '.join(command))

        returncode, data, erreurs = subprocessLaunchWithoutConsole(command)
        #
        if erreurs:
            for ligne in erreurs:
                self.suivis.insert('end', ligne.decode('utf-8').strip())
                logging.error(ligne.decode('utf-8').strip())

        if data:
            for ligne in data:
                self.suivis.insert('end', ligne.decode('utf-8').strip())
                logging.info(ligne.decode('utf-8').strip())

        return

        # --------------------------------
        # - lance application  Convertor
        # -------------------------------
        def runApp1(self):
            """
            lancement
            """
            logger.error('*************** ERROR ***********')
            # for elem in self.list_folders_tosave:
            fichiers_src = ' '.join(self.list_folders_tosave)
            self.var_environnement_default['RUN_TEST'] = 'n'
            self.var_environnement_default['FICHIERS_SRC'] = fichiers_src

            command = "sshpass -p $(cat FILE) rsync --progress --log-file=remote_rsync.log -e 'ssh '" \
                      " -av%(RUN_TEST)s %(FICHIERS_SRC)s" \
                      "%(REMOTE_LOGIN)s@%(REMOTE_IP)s:%(REMOTE_DIR)s" % \
                      (self.var_environnement_default)

            logger.debug('Rsync with command: ' + ' '.join(command))
            returncode, data, erreurs = subprocessLaunchWithoutConsole(command)
            #
            if erreurs:
                for ligne in erreurs:
                    self.suivis.insert('end', ligne.decode('utf-8').strip())

            if data:
                for ligne in data:
                    self.suivis.insert('end', ligne.decode('utf-8').strip())

            return


#------------------------
# Main programme
#------------------------
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
    root = Tkinter.Tk();
    root.configure(width= 10, height=10)
    #root.iconbitmap("images/setup.ico")

    root.option_add('*activeBackground', abg)
    root.option_add('*activeForeground', afg)
    root.option_add('*selectBackground', sbg)
    root.option_add('*selectForeground', sfg)
    #root.option_add('*font', font) 
   
    root.option_add('*background', "#fff" )
    root.option_add('*foreground', "#22f")

    tr = ClssSynchroRep(root)
    tr.start_appli()

    Pmw.initialise(root)
    root.config(relief=Tkinter.RAISED, bd=3)
    root.title("Synchro Save 0.99 www.atlass.fr")
    ## la bouclen d'attente evenements
    root.mainloop()
