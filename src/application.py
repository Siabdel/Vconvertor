#! /usr/python
# -*- coding:utf-8 -*-
import fileinput, codecs
import os, sys, stat, string, datetime, time, re
import Pmw
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import Tk, tkinter, PhotoImage, StringVar, Radiobutton
from Tkinter import TOP, BOTTOM, YES, LEFT, RIGHT, Y, IntVar, W, N, S, E, ALL, NORMAL, DISABLED

from Tkinter import Checkbutton, Radiobutton, Scrollbar, Toplevel, Button
from Tkinter import Listbox, Label, Entry, Canvas
from tkFileDialog import askdirectory, askopenfilename, askopenfilename, Directory
from ScrolledText import Scrollbar, ScrolledText
import tkFont
import os, sys, time
from xml.dom import minidom
import fileinput
import decimal
from  traceback import print_exc
from string import strip
import glob
import bdb
# module local 
from commun_helpers import subprocessLaunchWithoutConsole, createElemntXml
from commun_helpers import deleteConfigUserFromFileXml


class MixinTkApp(Tkinter.Frame):
    """
    class Application
    """
    def __init__(self, root):
        self.root = root
        self.appframe = Tkinter.Frame.__init__(self, root)
        self.my_font = tkFont.Font(family="Monaco", size=12)  # use a fixed width font so columns align

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.jpeg'
        options['filetypes'] = [('All', '*')]
        options['initialdir'] = 'C:\\'
        options['parent'] = root
        options['title'] = 'Select a File'
        self.tab_entry = {}


        self.var_environnement_default = {
            'ID': '',
            'LOCAL_DIR': '/home/abdel/',
            'REMOTE_HOST' : 	'',
            'REMOTE_IP'	: 	'',
            'REMOTE_LOGIN'	: '',
            'REMOTE_PASSWORD'	: '',
            'REMOTE_PORT'	: '',
            'REMOTE_LOGIN'	: '2222',
            'REMOTE_DIR'	: '',
            'TRACE'		: 	os.path.dirname(os.path.abspath(__file__)) + "/out",

        }

        # les images icones
        self.img_convert 	= PhotoImage(file = "images/convert.gif" )
        self.img_play 		= PhotoImage(file = "images/play.gif" , height=50)
        self.img_param 		= PhotoImage(file = "images/param.gif" )
        self.img_ajouter	= PhotoImage(file = "images/ajouter.gif" , height=50)
        self.img_reload		= PhotoImage(file = "images/reload.gif" , height=50)
        self.img_quitter	= PhotoImage(file = "images/quit_rouge.gif" , width=50, height=20)

        # multi frames
        self.notebook1 = Pmw.NoteBook(self.appframe,
                                      createcommand = None,
                                      lowercommand = 	None,
                                      raisecommand = 	None,
                                      hull_width 	= 600,
                                      hull_height = 300,
                                      )

        # Pack the notebook last so that the buttonbox does not disappear
        # when the window is made smaller.
        self.notebook1.pack(fill = 'both', expand = 1, padx = 5, pady = 5 )

        self.page1 = self.notebook1.add('Page1')
        self.page2 = self.notebook1.add('Page2')
        self.page2.focus()
        # afficher les pages
        group_info = Pmw.Group(self.page1, tag_text='Suivi')
        group_info.pack(side=BOTTOM, expand=YES, padx=2, pady=2)

        # affiche la page
        self.default_pages(group_info)
        # charger la config des paramétrer
        self.chargeConfiguration()


    def default_pages(self, group):
        # -------------------------
        # - Info Suivi
        # -------------------------
        group_info = Pmw.Group(self.appframe, tag_text='Suivi')
        group_info.pack(side=TOP,  expand = YES, padx = 2, pady = 2)

        self.suivis 	= Listbox(group_info.interior(), font=self.my_font)
        ascenseur 	= Scrollbar(group_info.interior())
        ascenseur.config(command = self.suivis.yview)
        # attach listbox to scrollbar
        ascenseur.pack(side=RIGHT, fill=Y)

        self.suivis.config(yscrollcommand = ascenseur.set)
        self.suivis.config(background='white', foreground='blue')
        self.suivis.config(height = 5, width = 55)
        self.suivis.pack()

        buttonBoxAdmin = Pmw.ButtonBox(self.appframe)
        bt1 = buttonBoxAdmin.add('Paramètrage',  	cursor='hand2' ,width=30, height=20,
                                 command = self.parametrages, image=self.img_param)
        bt2 = buttonBoxAdmin.add('Quitter',  	cursor='hand2' ,width=30, height=20,
                                 command = self.quit, image= self.img_quitter)


        buttonBoxAdmin.pack(side=RIGHT, padx=3, pady=3)

        self.tipinfo1 = Pmw.Balloon(self.appframe)
        self.tipinfo1.bind(bt1, 'Paramètrage du lanceur')
        buttonBoxAdmin.setdefault('Paramètrage')

    # -- Page 2
    def page2_defaut(self):
        """
        affiche page2 par defaut
        :return: group checkbutton
        """
        group_options = Pmw.Group(self.page2, tag_text='Options')
        group_options.pack(side=TOP,  expand = YES, padx = 2, pady = 2)

        var = IntVar()
        for castmember, row, col, status in [
            ('Normal', 0 ,0 ,NORMAL), ('Compressé', 0 ,1 ,NORMAL),
            ('Ananlyse', 1 ,0 ,DISABLED), ('Test After', 1 ,1 ,NORMAL),
            ('Cloturer a la fin de traitement' ,2 ,0 ,NORMAL), ('Terry Gilliam', 2 ,1 ,NORMAL)]:
            setattr(var, castmember, IntVar())
            Checkbutton(group_options.interior(), text=castmember, state=status, anchor=W,
                        variable = getattr(var, castmember)).pack(anchor=W)

        # options for buttons
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}


    def selectdirectory(self, options):
        """
        Returns an opened Directory .
        options = {}
        options['initialdir'] = os.path.dirname(os.path.abspath(__file__))
        options['initialdir'] = self.var_environnement_default['LOCAL_DIR']
        options['title'] = 'Choisissez un repertoire'
        options['multiple'] = 1
        """
        # print "les options event=%s... options = %s" % (event, options)
        # recupere la destination Entry
        if options.get('dest') :
            self.dest = options['dest']
            del options['dest']

        nomFic = askdirectory(**options)
        if nomFic  :
            self.dest.delete(0, "end")
            self.dest.insert(0, nomFic)

        return True

    # -------------------
    # Parametrage
    # -------------------
    def parametrages(self) :
        self.root_params = Toplevel()
        self.root_params.option_add('*background', "#CCC")
        self.root_params.option_add('*foreground', "#33F")

        self.notebook2 = Pmw.NoteBook(self.root_params,
                                      createcommand = None,
                                      lowercommand = 	None,
                                      raisecommand = 	None,
                                      hull_width 	= 450,
                                      hull_height 	= 340,
                                      )

        # Pack the notebook last so that the buttonbox does not disappear
        # when the window is made smaller.
        self.notebook2.pack(fill = 'both', expand = 1, padx = 5, pady = 5 )

        self.page_param1 = self.notebook2.add('Paramètres')
        self.page_param2 = self.notebook2.add('test Connexion')

        self.page_param1.focus()

        # ajout dune Frame
        self.pframe1 = Tkinter.Frame(self.page_param1, bd =1,  bg ='#FFFFFF', width=400, height=540);
        self.pframe1.pack(fill = 'both', expand = 1)

        self.pframe2 = Tkinter.Frame(self.page_param2, bd =1,  bg ='#FFFFFF', width=400, height=540);
        self.pframe2.pack(fill = 'both', expand = 1)

        # --------------------------------------
        # parametrages Variables environnement
        # ---------------------------------------

        self.group_param1 = Pmw.Group(self.pframe1, tag_text=r'Paramètrage Convertor')
        self.group_param1.pack(fill = 'both', expand = 0, padx = 6, pady = 6)
        self.group_param2 = Pmw.Group(self.pframe2, tag_text='Connexion')
        self.group_param2.pack(fill = 'both', expand = 0, padx = 6, pady = 6)


        # ---------------------------------------------
        # charger le tableau des variables environnement
        # ---------------------------------------------

        for ind, cle in   enumerate(self.var_environnement_default.keys()) :
            #
            Label(self.group_param1.interior(), text= cle).grid(row=ind, column=0)
            self.tab_entry[cle ]= Entry(self.group_param1.interior(), width=60, bg='white')
            # self.tab_entry[cle].config(bg="#FFFFCC")
            # self.tab_entry[cle].config(state = Tkinter.DISABLED)

            # si n'est pas dans le tableau on le rajoute
            if self.var_environnement_default.has_key(cle) :
                self.tab_entry[cle].insert(0, self.var_environnement_default[cle])

            # username 
            if cle == 'ID' :
                self.tab_entry[cle].delete(0, "end")
                self.tab_entry[cle].insert(0, self.var_environnement_default[cle])
                # self.tab_entry[cle].config(state = "readonly")
                #
                self.tab_entry['ID'].bind('<KeyPress>', lambda event : self.update(event, 'ID'))


            self.tab_entry[cle].grid(row=ind , column=1)
            # print type(self.tab_entry[cle])
            ind = ind +1
            ## activation debugage

        # -----------------------------
        # Les different choix
        # -----------------------------
        libelles = ["Oui", "Non"]
        valNomages = ["O", "N"]

        self.optionsTest = StringVar()
        self.optionsTest.set(valNomages[1])

        group_choix = Pmw.Group(self.root_params, tag_text='Execution en test')
        group_choix.pack(fill='both', expand=0, padx=6, pady=6)

        n = 0
        choix_nomage = []
        for n in range(len(libelles)):
            bt_test = Radiobutton(group_choix.interior(), text=libelles[n],
                                  width=12,
                                  variable=self.optionsTest,
                                  value=valNomages[n],
                                  command=None).grid(row=1, column=n + 1)

        # ---------------------------------------------
        # Lancement de IAH
        # ---------------------------------------------

        self.canvas_bicolor_r = Canvas(self.group_param2.interior(), width=15, height=15, cursor='hand2')
        self.canvas_bicolor_r.create_oval(1, 1, 15, 15, outline="white", fill='#f00', width=1)
        self.canvas_bicolor_r.grid(row=0, column=0)

        self.canvas_bicolor_v = Canvas(self.group_param2.interior(), width=15, height=15, cursor='hand2')
        self.canvas_bicolor_v.create_oval(1, 1, 15, 15, outline="white", fill='#000', width=1)
        self.canvas_bicolor_v.grid(row=0, column=1, padx=22)

        # buttonBox = Pmw.ButtonBox(self.group_param3.interior())
        buttonBox = Pmw.ButtonBox(self.root_params)
        buttonBox.add('Annuler', width=12, command=self.root_params.destroy, cursor='hand2')
        buttonBox.add('Enregistrer', width=12, command=self.save_param, cursor='hand2')

        buttonBox.pack()

    def askopenfilename(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        # get filename - edited to be part of self
        self.filename = tkFileDialog.askopenfilename(**self.file_opt)

        # open file on your own
        if self.filename:
            print "askopenfilename value: " + self.filename
            return self.filename

    def printing(self):
        print "Value on click: " + self.filename

    def quit(self):
        self.root.destroy()

    def grille_choix(self):
        """
        grille de choix avec des RADIOBUTTON et CHECKBUTTON
        """
        group_options = Pmw.Group(self.page2, tag_text='Choix')
        group_options.pack(side=TOP, expand=YES, padx=2, pady=2)

        var = IntVar()

        for text, value in [('Passion fruit', 1), ('Loganberries', 2),
                            ('Mangoes in syrup', 3), ('Oranges', 4),
                            ('Apples', 5), ('Grapefruit', 6)]:
            Radiobutton(group_options.interior(), text=text, value=value, variable=var).pack(anchor=W)
            var.set(3)

        group_check_options = Pmw.Group(self.page2, tag_text='Suivi')
        group_check_options.pack(side=TOP, expand=YES, padx=2, pady=2)

        for castmember, row, col, status in [
            ('John Cleese', 0, 0, NORMAL), ('Eric Idle', 0, 1, NORMAL),
            ('Graham Chapman', 1, 0, DISABLED), ('Terry Jones', 1, 1, NORMAL),
            ('Michael Palin', 2, 0, NORMAL), ('Terry Gilliam', 2, 1, NORMAL)]:
            setattr(var, castmember, IntVar())
            Checkbutton(group_check_options.interior(), text=castmember, state=status, anchor=W,
                        variable=getattr(var, castmember)).pack(anchor=W)

            # -------------------------
            # - Info Suivi
            # -------------------------
            group_info = Pmw.Group(pframe, tag_text='Suivi')
            group_info.pack(side=TOP, expand=YES, padx=2, pady=2)

            my_font = tkFont.Font(family="Monaco", size=12)  # use a fixed width font so columns align
            self.suivis = Listbox(group_info.interior(), font=my_font)
            ascenseur = Scrollbar(group_info.interior())
            ascenseur.config(command=self.suivis.yview)
            # attach listbox to scrollbar
            ascenseur.pack(side=RIGHT, fill=Y)

            self.suivis.config(yscrollcommand=ascenseur.set)
            self.suivis.config(background='black', foreground='white')
            self.suivis.config(height=5, width=55)
            self.suivis.pack()

            self.buttonBoxAdmin = Pmw.ButtonBox(pframe)
            bt1 = self.buttonBoxAdmin.add('Ajouter', cursor='hand2', width=30, height=20,
                                          command=self.ouvrirRepertoire, image=self.img_ajouter)
            bt4 = self.buttonBoxAdmin.add('Paramètrage', cursor='hand2', width=30, height=20,
                                          command=self.parametrages, image=self.img_param)
            self.buttonBoxAdmin.pack(side=RIGHT, padx=3, pady=3)
            self.tipinfo1.bind(bt1, 'Lancer Convertor')
            self.tipinfo1.bind(bt4, 'Paramètrage du lanceur')

    def save_param(self):
        """
        """
        self.dialog3 = Pmw.MessageDialog(None, title='Confirmation',
                                         message_text='Souhaiter-vous Enregistrer cette config ?',
                                         buttonboxpos='e',
                                         iconpos='n',
                                         icon_bitmap='warning',
                                         buttons=('Ok', 'Annuler'),
                                         defaultbutton='Close')

        self.dialog3.withdraw()
        # Create some buttons to launch the dialogs.
        result = self.dialog3.activate()
        if (result != 'Ok'):
            return False

        fichierData = os.getcwd() + "/config/config.xml"
        maintenant = datetime.datetime.now()
        date_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
        t_timestamp = long(time.time())
        t_id = "SC_" + str(t_timestamp)

        xmldoc = minidom.parse(fichierData)
        root = xmldoc.getElementsByTagName("ROOT")

        # ----------------------------------------------------------------------------
        # 1- test si ID existe ==> on la supprime et on remplce par la new
        # ---------------------------------------------------------------------------
        # 
        if self.searchConfigFromFileXml(root, self.var_environnement_default['ID']):
            # suppression element pour le remplacer apres
            elem = self.searchConfigFromFileXml(root, self.var_environnement_default['ID'])
            root[0].removeChild(elem)

        # creer nouveau param 
        new_scenario = createElemntXml(xmldoc, 'PARAM')
        scenario_id = xmldoc.createAttribute('ID')
        scenario_id.nodeValue = str(t_id)
        new_scenario.setAttributeNode(scenario_id)

        scenario_created = xmldoc.createAttribute('CREATED')
        scenario_created.nodeValue = str(date_complet)
        new_scenario.setAttributeNode(scenario_created)

        # Ajout des parametres du scenario
        for key, val in self.var_environnement_default.items():
            if key == 'ID':
                att = xmldoc.createAttribute(key)
                att.nodeValue = val
                new_scenario.setAttributeNode(att)
            # self.tab_entry[cle].insert(0, self.var_environnement_default[cle])
            new_noeux = createElemntXml(xmldoc, key, self.tab_entry[key].get())
            new_scenario.appendChild(new_noeux)

        # on rattache a root
        root[0].appendChild(new_scenario)
        # ------------------------
        # save contenu en fichier
        # ------------------------
        contenueXml = xmldoc.toxml()
        # save contenu en fichier
        with codecs.open(fichierData, 'w', 'utf-8') as fd:
            fd.write(contenueXml)
        # On recharge la config a nouveau
        self.chargeConfiguration()
        # on clos la fenetre de parametrage
        self.root_params.destroy()

    # ---------------------------------------
    # suppression Transaction From File DataXml
    # ---------------------------------------
    def searchConfigFromFileXml(self, root, search):
        # on charge le fichier data xml en xmldoc

        top = root[0]
        les_configs = top.getElementsByTagName('PARAM')

        for config_courant in les_configs:
            #
            if config_courant.attributes["ID"].value == search:
                # element trouver
                # print "search trouver ... %s " % (config_courant.attributes["ID"].value )
                return config_courant
        return False

    def chargeConfiguration(self):
        """
        charge la config en cours a partir du fichier 'config.xml'
        """
        list_parametres = {}
        # lecture du fichier config
        fichierData = os.getcwd() + "/config/config.xml"
        if not os.path.isfile(fichierData):
            self.save_default_config()

        xmldoc = minidom.parse(fichierData)
        root = xmldoc.getElementsByTagName("ROOT")

        # recherche de campagne_id
        top = root[0]
        config_courant = top.getElementsByTagName('PARAM')[0]

        for key, value in self.var_environnement_default.items():
            # print key, config_courant.getElementsByTagName(key)[0].firstChild.data
            # add

            if key == 'ID':
                self.var_environnement_default[key] = config_courant.attributes["ID"].value

            else:
                try:
                    self.var_environnement_default[key] = config_courant.getElementsByTagName(key)[0].firstChild.data

                except Exception:
                    pass

                    # suivant
                    # cap = config_courant.nextSibling

        # print list_Campagne_xml
        return self.var_environnement_default

        # -----------------------------
        # update l'ecran suivi
        # -----------------------------

    def refreshSuivi(self):
        # lecture du fichier trace
        self.suivis.delete(0, 'end')
        if (os.path.isfile("trace.log")):
            fs = open("trace.log", "r")
            lignes_traces = fs.readlines()
            fs.close()
            ind = 0
            for ligne in lignes_traces:
                ind += 1
                ligne = ligne.strip()
                ligne = ligne.strip('\t')
                self.suivis.insert(ind, ligne)
        return True

    def apropos(self):
        ##
        msg = """
    	start Convertor  Version 0.99
    	version library OCI Oracle 10g
    	Powered by bdelaziz SADQUAOUI  Lyon
    	Created by Abdelaziz Sadquaoui (asadquaoui@atlass.fr)
    	Support : http://www.support.atlass.fr
    	Copyright Abdelaziz Sadquaoui © 2012 - 2013
    	"""
        messages = Pmw.MessageDialog(None, title='A propos', message_text=msg);
        messages.show();


if __name__ == '__main__':
    root = Tkinter.Tk()
    root.title("Application")
    MixinTkApp(root).pack()
    root.mainloop()