# -*- coding: utf-8 -*-
from Tkinter import *
import Pmw
import Tkinter
import tkMessageBox
import threading
import subprocess
from tkFileDialog import *
import time
from time import (strftime, mktime)
import shutil, errno
from math import fmod, fabs
import os
from xml.dom import minidom
import xml.parsers.expat
from datetime import datetime
from codecs import open
from string import Template
from commun_helpers import getListTransactionsDefault, subprocessLaunchWithoutConsole, traceLog
import sys
import subprocess
#from csv import *
#-----------------------------------
# MultiThread2
#------------------------------------

class MultiThread(threading.Thread) :
	
	def __init__(self, ligne_cmde, arg) :
		threading.Thread.__init__(self)
		debut = 10 
		self.commandes = ligne_cmde
		self.arguments = arg
	
	def start_tache(self) :
		my_Scheduler = Scheduler()
		my_Scheduler.schedule("Sauvegarde Base",  datetime.now(),  self.every_x_mins(1.60),	self.Sauvegarde);

		my_Scheduler.run()
		
		
	def run(self):
		 
		try :
			#a = threading.Thread(None, self.lancenavigateur , None, (20,), {"cmde": navigateur , "arg":argum} )
			argum = "file:///" +  self.arguments  ;
			tt = threading.Thread(None, self.lanceCommande , None, (), {"cmde": self.commandes , "arg": "file:///" +  self.arguments  } )
			tt.start()
			 
		except WindowsError, ValueError :
			msg = "erreur de threading.Thread  %s " % str(ValueError)
			#print msg
			#messages = Pmw.MessageDialog(self.page0, title='Connexion base', message_text=msg)
		
			
	
	def lanceCommande(self, cmde, arg) :
		#
		
		stderr = subprocess.STDOUT
		stdout = subprocess.STDOUT
		try :
			retval = subprocess.call([cmde, arg], 0, None, None)
			
		except WindowsError, ValueError :
			msg = "erreur de subprocess.call  %s " % str(ValueError)
			#print msg
			#messages = Pmw.MessageDialog(self.page0, title='Connexion base', message_text=msg)
			
			
	def every_x_secs(self, x):
		"""
		Returns a function that will generate a datetime object that is x seconds
		in the future from a given argument.
		"""
		return lambda last: last + datetime.timedelta(seconds=x)

	def every_x_mins(self, x):
		"""
		Returns a function that will generate a datetime object that is x minutes
		in the future from a given argument.
		"""
		return lambda last: last + datetime.timedelta(minutes=x)
	
	def daily_at(self, time):
		"""
		Returns a function that will generate a datetime object that is one day
		in the future from a datetime argument combined with 'time'.
		"""
		return lambda last: datetime.datetime.combine(last + datetime.timedelta(days=1), time)

#-----------------------------
# class MyButton 
#----------------------------- 
class MyButton(Tkinter.Button):
	# This is just an ordinary button with special colors.
	"""
	Valid resource names: activebackground, activeborderwidth,
	activeforeground, background, bd, bg, borderwidth, cursor,
	disabledforeground, fg, font, foreground, postcommand, relief,
	selectcolor, takefocus, tearoff, tearoffcommand, title, type.
	
	"""
	def __init__(self, master=None, cnf={}, **kw):
		self.__toggle = 0
		self.__cursor='hand2'
		kw['background'] = '#fff'
		kw['activebackground'] = 'red'
		 
		apply(Tkinter.Button.__init__, (self, master, cnf), kw)
	

#-----------------------------
# class boutton parcourir 
#-----------------------------
class BtParcourir :
	"""
	class pour faire un boutton parcourir different
	affiche le block fichier parcourir
	"""
	 
	def __init__(self, parent,  style=0) :
		self.style = style
		self.mimages = None
		self.parent  = parent
		self.entNameFichier = Entry(self.parent, width=30, bg='white');
		#
		if (self.style == 0) :
			self.bouParcourir = Button(self.parent, text='Parcourir ...', width=15, command=None)
			self.bouParcourir.bind('<Button-1>', lambda  event : self.getOpenOneFichier())  ## 
		else :
		
			options = {
				'images' 	: 	['images/openfolder'],
				'infosBull' 	:	['ouvrir Fichier data' ],
				'commandes' 	:	[self.getOpenOneFichier],
				'hor'		:	'horizontal'
				}
			self.mimages = MenuImages(self.parent, options)

		
	def getBouParcourir(self) :
		#----------------------------------------------
		return self.bouParcourir
	
	def getEntyFichier(self) :
		#----------------------------------------------
		return self.entNameFichier 
	
	
	##------------------------------
	# --- affiche Parcourir
	##------------------------------
	def afficheParcourir(self, ligne, col) :
		#
		if (self.style == 0) :
			self.entNameFichier.grid(row=ligne, column=col)
			self.bouParcourir.grid(row=ligne, column=col + 1)
		else :
			self.entNameFichier.grid(row=ligne, column=col)
			self.mimages.afficheMenu(ligne, col + 1)
	##------------------------------
	#--- fonction ouverture fichier
	##------------------------------
	def getOpenOneFichier(self) :

		# ouvrir un seul fichier

		nomFic =  askopenfilename()
		if nomFic :
			self.entNameFichier.delete(0, "end")
			self.entNameFichier.insert(0, nomFic)
			return nomFic
		else : 
			return None	
		
		

#-----------------------------
# class menu en boutton active
#-----------------------------
class MenuImages :

	def __init__(self, parent, options) :
		# Création d'un objet manu en images gif
		self.boutons = []
		self.width = 20
		self.height = 20
		self.hor = 'horizontal'
		self.infosBull = None
		images = []

		if (options.has_key('images')) :
			images = options['images']
		else :
			return

		if (options.has_key('infosBull')) : 
			self.infosBull 	= options['infosBull']
		else :
			 options['infosBull'] = ("")
			 
		if (options.has_key('commandes')) : 
			self.commandes 	= options['commandes']
		else :
			options['commandes'] = ("")
		
		if (options.has_key('hor')): 
			self.hor 	= options['hor']
		else :
			options['hor'] = 'horizontal'
			
		if (options.has_key('width')): 
			self.width 	= options['width']
		
		if (options.has_key('height')):
			self.height 	= options['height']
			
		
		self.tip = Pmw.Balloon(parent)
		#--------------------------------------------------------
		# Création de la barre d'outils (c'est un simple cadre) :
		#--------------------------------------------------------
		##toolbar = Frame(self.mainframe, bd =1,  bg ='white')
		##toolbar.pack(expand =YES, fill =X)
		# Nombre de boutons à construire :
		"""
		photo = PhotoImage(file='toto.gif')
		item = can1.create_image(250, 250, image = photo)
		can1.pack()
		
		fen = Tk()
		fileMenu = Menubutton(fen, text = 'Fichier')
		fileMenu.pack(side = TOP)
		me1 = Menu(fileMenu)
		me1.add_command(label = 'Ouvrir', command = ouvrir)
		fileMenu.configure(menu = me1)

		
		"""
		
		self.nBou = len(images)

		# Les icônes des boutons doivent être placées dans des variables
		# persistantes. Une liste fera l'affaire :
		self.photoI =[None]*self.nBou
		i = 0

		for ind in range(self.nBou):
			# Création de l'icône (objet PhotoImage Tkinter) :
			
			
			self.photoI[ind] =PhotoImage(file = images[ind] +'.gif', width=self.width )
			# Création du bouton.:
			# On utilise une expression "lambda" pour transmettre
			# un argument à la méthode invoquée comme commande :
			self.boutons.append( Button(parent, image =self.photoI[ind], text = 'Scanner ...', relief =GROOVE, command = self.commandes[ind],  width=self.width, height=self.height, cursor='hand2'))
		##

	def afficheMenu(self, ligne=0, col=0) :
		c =l =0
		if( self.nBou > 1 ):
			for bt in range(self.nBou):

				if ( self.hor == 'horizontal') :
					c = c + 1
					l = ligne 
				elif ( self.hor == 'vertical'):
					j = j+1
					c= col

				self.boutons[bt].grid(row=l, column=c)

				#bou.pack(side =LEFT)
				# association du bouton avec un texte d'aide (bulle) :
				self.tip.bind(self.boutons[bt], self.infosBull[bt])
		else :
			self.boutons[0].grid(row=ligne, column=col)
			# association du bouton avec un texte d'aide (bulle) :
			self.tip.bind(self.boutons[0], self.infosBull[0])

		## retour des bourtons creer
		return self.boutons
			

##-------------------------
## Class Oracle 
##----------------------
class oracleHelper :

	def __init__(self, parent) :
		#
		self.parent = parent
		
	def connexion (chaine) :
		##-------------------------
		### Ouverture de la base 
		##----------------------
		##chaine =  "susie/grutil@CHOLET2007"
		##chaine =  self.ent1.get() + "/" +   self.ent2.get() + "@" +  self.ent3.get()
		try :
			connection = cx_Oracle.connect(chaine)
		except :
			messages = Pmw.MessageDialog(self.page0, title='Connexion base', message_text="Impossible de se connecter à la base !")
			#print "Impossible de se connecter à la base !"
			return
		return connection
		
	##-------------------------
	## execution sql
	##----------------------
		
	def execute_sql(self, sql) :
		##
		try :

			curseur = self.connection.cursor()
			curseur.execute(sql)
			return curseur;

		except cx_Oracle.DatabaseError, exc :
			error, = exc.args
			self.afficheInfos("Impossible d'executer cette requete ! " + str(error.code) + " " + str(error.message))
			#print >> sys.stderr, "Oracle-Error-Code:", error.code
			#print >> sys.stderr, "Oracle-Error-Message:", error.message
			return None

		except Exception, message:
			#print message
			self.afficheInfos("Impossible d'executer cette requete ! " + error.message)

			return None

	
	def testConnect(self):
		#print chaine
		#a = threading.Thread(None, self.isConnect , 'Therda name', (chaine,) )
		i = 0
		while i < 3 :
			chaine = self.list[i]
			self.afficheInfos(chaine)
			try :
				#connection = cx_Oracle.connect("user", "password", "TNS")
				self.connection = cx_Oracle.connect(chaine) 
				self.parent.infoBase( "Connexion ok" +  chaine ) 
				self.parent.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
				self.parent.update()


			except :
				self.parent.afficheInfos( "Erreur de connexion", "connexion à echouer" + chaine )
				self.parent.connection = None 

				#self.parent.st.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
				#self.parent.st.update()
			i = i+1
		# stop thread
		self.stop
		
		
	def getRecord(sql) :
		""" verifie l'existance d'un enregistremet 
		"""
		## Execution de la requete
		cnx = connexion()
		curs1 = cnx.cursor()
			
		
		
		try :
			message =  curs1.execute(sql)
			 
		except cx_Oracle.DatabaseError, exc :
			error, = exc.args
			self.afficheInfos("Impossible d'executer cette requete ! " + str(error.code) + " " + str(error.message))
			return None

		except Exception, message:
			#print message
			self.afficheInfos("Impossible d'executer cette requete ! " + error.message)
		
			return None
	
		## lecture de donnes de base 
		 
		row = curs1.fetchone()
		 
		if row : 
			#(id, code, libelle) = (row[0], row[1], row[2])
			## fermetures de base et curseurs	
			cnx.close()
			return row 
		## fermetures de base et curseurs	
		cnx.close()		
		return -1
		

	############################
	## Export ligne insert oracle
	############################
	def exportLigneInsert(curseur, table, sequence) :
		enreg = []
		clePrim = []
		insertInto = ""

		while 1 : 
			i = 0
			ligne = ""
			enreg = curseur.fetchone()  
			if enreg == None :
				break
			while i < len(enreg)  :
				if type(enreg[i]) == cx_Oracle.DATETIME :
					print "valeur date ", enreg[i]
					col = "to_date('" + str(enreg[i]) + "', 'yyyy-mm-dd hh24:mi:ss')"
				elif type(enreg[i]) == cx_Oracle.NUMBER :
					print "valeur nombre", enreg[i]	
					col =  str(enreg[i])  				
				elif type(enreg[i]) == cx_Oracle.STRING :
					print "valeur chaine", enreg[i]
					col = strsql(enreg[i], 'text') 

				else :
					col = strsql(enreg[i], 'text') 	
					tt = str(enreg[i])

				if enreg[i] == None :
					col = 'null'
				## ------------------
				# format la ligne 
				if i == 0 :
					ligne += sequence + ".nextval, "
				elif i == len(enreg) - 1 :
					ligne += col 
				else :
					ligne += col + ","
				i+=1

			# ecriture en fichier de la ligne insert 
			ligne  = "insert into " + table + " values (" + ligne +  ");" + "\n"
			##print ligne
			insertInto += ligne
		##
		return insertInto
		
	#shutdown abort:
	def shutdown_abort(sid):
		try:
			os.environ['TWO_TASK']=sid
			handle=cx_Oracle.connect("sys", "yourpwd", sid, cx_Oracle.SYSDBA)
			handle.shutdown(mode = cx_Oracle.DBSHUTDOWN_ABORT)
			return 0
		except cx_Oracle.DatabaseError,info:
			print "Error: ",info
			return 1

	# startup nomount:
	def startup_nomount(sid):
		try:
			os.environ['TWO_TASK']=sid
			handle=cx_Oracle.connect("sys", "yourpwd", sid, cx_Oracle.SYSDBA | cx_Oracle.PRELIM_AUTH)
			handle.startup()
			return 0
		except cx_Oracle.DatabaseError,info:
			print "Error: ",info
			return 1

	# mount:
	def db_mount(sid):
		try:
			os.environ['TWO_TASK']=sid
			handle=cx_Oracle.connect("sys", "yourpwd", sid, cx_Oracle.SYSDBA)
			cursor = handle.cursor()
			cursor.execute("alter database mount")
			return 0
		except cx_Oracle.DatabaseError,info:
			print "Error: ",info
			return 1

	# open resetlogs
	def db_open_resetlogs(sid):
		try:
			os.environ['TWO_TASK']=sid
			handle=cx_Oracle.connect("sys", "yourpwd", sid, cx_Oracle.SYSDBA)
			cursor = handle.cursor()
			cursor.execute("alter database open resetlogs")
			return 0
		except cx_Oracle.DatabaseError,info:
			print "Error: ",info
			return 1

	# open
	def db_open(sid):
		try:
			os.environ['TWO_TASK']=sid
			handle=cx_Oracle.connect("sys", "yourpwd", sid, cx_Oracle.SYSDBA)
			cursor = handle.cursor()
			cursor.execute("alter database open")
			return 0
		except cx_Oracle.DatabaseError,info:
			print "Error: ",info
			return 1

	# Flashback database to a given restore point:
	def flashback_db(restore_point,sid):
		try:
			os.environ['TWO_TASK']=sid
			handle=cx_Oracle.connect("sys", "yourpwd", sid, cx_Oracle.SYSDBA)
			cursor = handle.cursor()
			sql="flashback database to restore point "+restore_point
			print sql
			cursor.execute(sql)
			return 0
		except cx_Oracle.DatabaseError,info:
			print "Error: ",info
			os.exit(1)		

	############################
	## Remlacement "'" en "\'"
	############################
	def strsql(chaine, type) :
		chaine = str(chaine)
		chaine = chaine.replace("'" , "\''")
		if type == 'text' :
			chaine = "'" + chaine + "'"
		elif type == 'date' :
			chaine = "to_date('" + chaine + "', 'dd/mm/yyyy') "
		return chaine 
	
	
	
	
class clssTestConnect(threading.Thread):
	def __init__(self, parent, listChaine=[]):
		threading.Thread.__init__(self)
		self.list = listChaine
		##frame apar pour ce thread
		root=Tk()
		self.mainframe = Tkinter.Frame(root,  bd =1,  bg ='blue')
		self.mainframe.pack(fill = 'both', expand = 1)
		self.parent = parent
		#flag terminated      
		self.Terminated = False

		#Déclaration du texte déroulant  
		self.group1 = Pmw.Group(self.mainframe, tag_text='Infos Base')
		self.group1.pack(fill = 'both', expand = 0, padx = 6, pady = 6)

		self.st = ScrolledText(self.group1.interior())
		self.st.pack(expand=1,fill='both',side='bottom')
		#on applique à tout le texte la police par défaut
		self.st.config(font = 'Arial 8 bold')
		self.st.config(foreground='black')
		#on configure le fond du 'texte dérouant'
		self.st.config(background='white')
		parent.infoBase( "Je suis tout seul à tester ok" ) 
		self.afficheInfos( "Je suis tout seul à tester ok")
		bouTest = Button(self.mainframe, text='ok', width=10, command=self.run)
		bouTest.pack()
		  


	def run(self):
		i = 0
		self.afficheInfos( "Je suis dans run") 
		
		
		while   i < 1:
		    #print   i
		    i += 1
		    #time.sleep(2.0)
		    chaine = self.list[i]
		    self.afficheInfos(chaine) 
		self.testConnect()
		self.stop
		    
		#print "le thread    s'est termine proprement"
	
	def stop(self):
		self.Terminated = True
		self.stop()
		self.afficheInfos( "Je suis arreter") 

	def testConnect(self):
		#print chaine
		i = 0
		#a = threading.Thread(None, self.isConnect , 'Therda name', (chaine,) )
		Label(self.mainframe, text='Status base').grid(row=1, column=1)
		self.statusBase = Canvas(self.group12.interior(), height=20, width=20, bg="black")
		self.statusBase.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
		self.statusBase.grid(row=1, column=2)

		while i < 3 :
			chaine = self.list[i]
			self.afficheInfos(chaine)
			try :
				#connection = cx_Oracle.connect("user", "password", "TNS")
				self.connection = cx_Oracle.connect(chaine) 
				self.parent.infoBase( "Connexion ok" +  chaine ) 
				self.parent.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
				self.parent.update()


			except :
				self.parent.afficheInfos( "Erreur de connexion", "connexion à echouer" + chaine )
				self.parent.connection = None 

				#self.parent.st.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
				#self.parent.st.update()
			i = i+1
		# stop thread
		self.stop

	def afficheInfos(self, text):

		#on insète le texte 'texte' dans le widget 'texte déroulant' nommé 'st'
		self.st.insert(Tkinter.END,text)
		self.st.insert(Tkinter.END, '\n')
		
			 
		
	
	def testConnectMain(self):
		#print chaine
		i = 0
		#a = threading.Thread(None, self.isConnect , 'Therda name', (chaine,) )

		while i < 3 :
			chaine = self.list[i]
			self.afficheInfos(chaine)
			try :
				#connection = cx_Oracle.connect("user", "password", "TNS")
				self.connection = cx_Oracle.connect(chaine) 
				self.infoBase( "Connexion ok" +  chaine ) 
				self.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
				self.update()


			except :
				self.afficheInfos( "Erreur de connexion connexion à echouer" + chaine )
				self.connection = None 

				#self.parent.st.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
				#self.parent.st.update()
			i = i+1
		# stop thread
		self.stop
	
	#Pointeur de souris en forme de main
	def lamain(self, event):
		self.st.config(cursor='hand2')
	
	#Pointeur de souris en forme de flèche
	def fleche(self, event):
		self.st.config(cursor='arrow')


	def colore(self, mot, couleur):
		start = 0.0
		while 1:
			try:
				i = self.st.search(mot,start,Tkinter.END)
				j = self.st.index('%s+%dc'%(i,len(mot)))
				self.st.tag_add(couleur,i,j)
				start = j
			except:
				break


	#####################
	###
	####################
	def isConnect(self, chaine ):
		
		try :
			#connection = cx_Oracle.connect("user", "password", "TNS")
			self.connection = cx_Oracle.connect(chaine) 
			self.infoBase( "Connexion ok" +  chaine ) 
			self.statusBase.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
			self.statusBase.update()
			return None

		except :
			self.afficheInfos(  "Erreur de connexion", "connexion à echouer" + chaine )
			self.connection = None 
			
			self.statusBase.create_oval(1, 1, 20, 20, outline="white", fill="red", width=1)
			self.statusBase.update()
			return true

	#####################
	###
	####################
	def scanDB(self) :
		#scan à partir du fichier tnsnames.ora
		#
		ORACLE_HOME = os.getenv("ORACLE_HOME","")
		
		#getenv(key, default=None)
		#Get an environment variable, return None if it doesn't exist.

		fichierTnsname  = 'C:\\oracle\\ora92\\network\\admin\\tnsnames.ora'

		#fichierTnsname  = self.SERVICE_PATH + '\\FatalError.txt'

		#print dateFichierJour

		if os.path.isfile(fichierTnsname) :
			#self.trace.insert(Tkinter.END, fichierTnsname + '\n')
			#self.trace.importfile(fichierTnsname)
			# 2- lire fichier tnsname
			#  

			fs = open(fichierTnsname, 'r') 
			 
			##ligne = fs.readline(-120)
			ligne = ""
			tabLigne = []
			while 1 :
		 
				ligne = fs.readline()
				if (ligne == "") :
					break
				
				
				resultat = re.search("^[a-zA-Z].+", ligne );
				
				if (resultat == None) :
					continue
				
				ligne = ligne.strip('\n')
				ligne = ligne.strip('=')
				ligne = ligne.strip(' ')
				#print ligne 
				## recupere les zones dans un tableau
				tabLigne.append(ligne)
				 


			 
			fs.close()

		else :
			Pmw.MessageDialog(self.mainframe, title='scanDb', message_text="Erreur de fichier tnsnames.ora introuvable" + fichierTnsname)
			return -1
			
			
		## test des connexions 
		i = 0 
		j = 0 
		dicoDB = {}
		##re_nombre = re.compile(r"(\d+)") # on exprime, on compile l’expression régulière
		## 4 resultat = re_nombre.search(une_chaine) #renvoie l’objet None en cas d’échec
		
		chaine = "admin@free.fr"
		
		re_nombre = re.compile(r"(^[^@]+@[^@]\.[^@]{2,4}$)")
		resultat = re_nombre.search(chaine );
		
		 
		
		filtre = """
		    ^                   	# debut de la chaine
		    (susie|system|sys)  	# user susie ou system ou sys
		     		 		#
		    \/(grutil|manager|manager) 	# avec / plus le mot de pass grutil ou manager
		    @[^@]+			# @ plus la chaine de connextion du tnsnames.ora
		    $                    	# end of string
		    """
		 
		chaineConnexion =  []
		while (j < len(tabLigne)) :
			chaine = "susie/grutil@" + tabLigne[j]
			
			resultat = re.search(filtre, chaine, re.VERBOSE);
			
			if(resultat != None) :
				#self.infoBase(str(j) + " /****" +  chaine ) 
				chaineConnexion.append(chaine);
				#a = threading.Thread(None, self.isConnect , 'Therda name', (chaine,) )
				#a.start()
				
				
				
			j = j+1
		#
		##progTest = clssTestConnect(self, chaineConnexion);
		self.list = chaineConnexion;
		self.testConnectMain()
		
		
		return True
		 

			
			
		while (i < 5) :
			
			 
			i = i + 1 

			#plus compteur
			
			
			## Message Alert 
			#tkMessageBox.showinfo("Etat", "Connexion Reussi")

			 
			"""
			# connect via SQL*Net string or by each segment in a separate argument
			#connection = cx_Oracle.connect("user/password@TNS")
			#connection = cx_Oracle.connect("user", "password", "TNS")
			
			cursor = connection.cursor()
			cursor.arraysize = 50
			cursor.execute(""
			        select Col1, Col2, Col3
			        from SomeTable
			        where Col4 = :arg_1
			          and Col5 between :arg_2 and :arg_3"",
			        arg_1 = "VALUE",
			        arg_2 = 5,
			        arg_3 = 15)
			for column_1, column_2, column_3 in cursor.fetchall():
			    print "Values:", column_1, column_2, column_3

			"""
			
			
			cursor = self.connection.cursor()
			cursor.arraysize = 50
			
			#--------------------------
			# on recupere nom etablissement 
			#--------------------------
			
			cursor.execute("select et_nometab from etab ")
						        	
			for nomEtab in cursor.fetchone():
				#print "Values:", nomEtab 
				dicoDB["etablissement"] = nomEtab
				
			
			
			
			#---------------------------------
			# on recupere la version susie 
			#-------------------------------
			cursor.execute("select  MAX( NPATCH || ' ' || dpatch  )  FROM susie.iv4trc")
			
			  						        	
			for version in cursor.fetchone():
				#print "Values:",  version 						
				tab = version.split(' ')
				dicoDB["date Version"] = tab[0]
				dicoDB["Version"] = tab[1]
		
			##self.trace.configure(text_fg ='red')
			self.afficheInfos(str(i) + "/" + str(len(tabLigne)) + "\t" + tabLigne[i] + "\n" , tabLigne[i])
			
			self.statusBase.create_oval(1, 1, 20, 20, outline="white", fill="green", width=1)
			self.statusBase.update()
			# compteur + 1 
			## remplissage du dico connexion 
			self.tabDico[tabLigne[i]] = dicoDB
			print tabLigne[i] 
			print self.tabDico 
			i = i + 1
			# fermer la connexion
			self.connection.close()


		return True
			
	##--------------------
	##--test de connexion
	##--------------------
	def testConnect(self):
		""" connect via SQL*Net string or by each segment in a separate argument
		test la connexion oracle via sqlNet et retourn None ou 1
		"""
		if (self.ent1.get() == "") | (self.ent2.get() == "") | (self.ent3.get() == "") :
			Pmw.MessageDialog(self.page1, title='Connect',	message_text="Saisie incomplete !")
			return -1


		# un refrech
		#self.trace.delete(0.0, Tkinter.END)		
		#self.trace.clear()
		
		chaine =  self.ent1.get() + "/" +   self.ent2.get() + "@" +  self.ent3.get()
		if self.debug == 1 :
			mess = "chaine de connexion = ", chaine
			#self.trace.insert(Tkinter.END, mess + '\n')

		try :
			self.connection = cx_Oracle.connect(chaine)  
			## Message Alert 
			tkMessageBox.showinfo("Erreur de connexion", "Connexion Reussi")
			
			self.connection.close()
			self.connection = None
			return True


		except :
			## Message Alert 
			tkMessageBox.showerror("Erreur de connexion", "connexion à echouer")
			self.connection = None 
			return ERR_NOTCONNECT

		return True
	
	#---------------------------------
	# executer pl-sql function
	#-------------------------------
	def execute_plsql_callfunc(self, fonction, curseur) :
		"""
		function pour executer du plsql fonction 
		"""

		l_version = curseur.var(cx_Oracle.STRING )

		##curseur = self.execute_sql(sql) 
		#ligne = curseur.callfunc("pck_expRimP.FUN_LireVersion", cx_Oracle.STRING, [l_version]) 

		ligne = None

		try :
			ligne = curseur.callfunc(fonction,  cx_Oracle.STRING) 
			#print ligne 

		except cx_Oracle.DatabaseError, exc :
			error, = exc.args
			self.afficheInfos("Erreur: Impossible d'executer cette requete PLSQL! " + str(error.code) + " " + str(error.message))

		return ligne 
	#---------------------------------
	# executer sql 
	#-------------------------------

	def execute_sql(self, sql) :
		##

		#trace en fichier log
		self.traceAppli("dans execute_sql() ...lig=717 ")

		try :
			curseur = self.connection.cursor()
			curseur.execute(sql)
			#trace en fichier log
			self.traceAppli("execusion sql ok dans execute_sql() ...lig=726 " + sql)
			return curseur;

		except cx_Oracle.DatabaseError, exc :
			error, = exc.args
			self.afficheInfos("Erreur: Impossible d'executer cette requete ! " + str(error.code) + " " + str(error.message))
			#print >> sys.stderr, "Oracle-Error-Code:", error.code
			#print >> sys.stderr, "Oracle-Error-Message:", error.message
			self.traceAppli("Erreur: Impossible d'executer cette requete ! lig=735 " + str(error.code) + " " + str(error.message))

			return None

		except Exception, message:
			#print message
			self.afficheInfos("Erreur: Impossible d'executer cette requete ! " +  str(message))
			self.traceAppli("Erreur: Impossible d'executer cette requete ! lig=742 " +  str(message))


			return None
		## retour du curseur 
		return curseur
		

#--------------------
#Barre de progression 
#--------------------
 
class BarreProgression(threading.Thread) :  
	"""
	Barre de progression 
	"""
	def __init__(self, parent=None, nb=100) :
		# si pas de parent interface independante
		self.parent = parent
		self.deamona = None
		self.vitesse = 1
		self.compt=0
		self.pos=0
		self.pas_encours = 0 	# compteur de pas encours
		self.maxpas 	= 100
		self.pas_calculer = float(nb)  / 100
		 
		
		self.pas_executer = 0
		
		#print "pas calculer = %s " % self.pas_calculer
		#print "nbre element = %s " % nb
		
		threading.Thread.__init__(self)
		
		
		if(self.parent == None) :
			principale = Tkinter.Tk()
			self.parent = principale
			#principale.iconbitmap("./images/setup.ico")
			
			# self.iconise(200)
			self.fen=Frame(principale, height=10, width=400, bd=2, relief=GROOVE, bg='#80c0c0')
			#self.fen.configure(bg='#FFF', fg='#f00')
			self.label_win = Label(self.fen, text='start ...', font=("Calibri", 12, 'italic'))
			self.label_win.config(bg='#000', fg='#fff')
			
			self.label_win.pack(side=TOP)
					
		else :
			self.fen=Frame(self.parent, height=10, width=400, bd=2, relief=GROOVE)
		
		
		self.can=Canvas(self.fen, height=10, width=400, bg="white")
		self.couleurCurseur = "red"
		
		
		
	## modidifer la vitesse de progreesion
	def setVitesse(self, v) :
		self.vitesse = v
		

	## modidifer la vitesse de progreesion
	def setPosition(self, v) :
		self.posEncours = v
		
	## start progression
	def start(self) :
		#
		self.fen.pack(fill = 'x', expand = 1)
		self.can.pack(fill = 'x', expand = 1)
					
	
	## start progression
	def deroule(self, nfois=100) :
		#
		self.next_pas()
		 
	
	##---------
	## next pas
	##---------
	def next_pas(self) :
		#----------
		self.pas_encours = self.pas_encours + 1
		taux_pas = float(self.pas_encours) / float(self.pas_calculer) # calcul du pas relatif 
	
		titre = "progress ... %s %s" % (str(int(taux_pas)), chr(37))
		
		self.label_win.configure(text=titre)
		self.label_win.update()
		if self.maxpas == self.maxpas :
			self.clear()
			
		if taux_pas >= 1 and taux_pas < self.maxpas :
			#print "taux pas = %d " % self.pas_encours
			
			afaire = int(taux_pas) - self.pas_executer
			for i in range( afaire  ) :
				self.un_pas() # pas suivant 
				self.pas_executer = self.pas_executer + 1
			
	def un_pas(self) :
			
		self.compt = self.compt + 4.2
		self.can.create_rectangle((1, 1, self.compt, 10), outline="white", fill="green")
		self.can.update()
		 
		
	## stop progression
	def arreter(self) :
		self.label_win.configure(text= "Traitement complete" )
		self.label_win.update()
		time.sleep(1)
		#self.can.destroy()
		self.parent.destroy() # Destroy frame and all children
	
	def clear(self) :
		self.can.create_rectangle((0, 1, 2, 20), outline="white", fill="white", width=1)
	
	def refesh(self, message=None):
		if message :
			self.label_win.configure(text= message )
		self.label_win.update()
	
	def iconise(self, after=2000) :
		#iconisé la fenetre barre progression
		self.parent.after(after, self.parent.iconify)
		
class MessageDialogBoxAs :

	def __init__(self) :
		#
		self.root = Tk();
		self.root.title('Confirmation Box')
		self.root.option_add('width',  200); 
		self.root.option_add('height', 80)
		self.root.option_add('*background', '#D0E3FF')
		self.root.option_add('*foreground', "#222")
		pframe = Tkinter.Frame(self.root, bd =1,  bg ='#FFFFFF', width=  200, height=80);
		pframe.pack(fill = 'both', expand = 1)
		"""
		ent1= Entry(self.root)
		ent1.pack()
		"""
		#
		comment = Label(pframe, text="Vous voulez enregistrer ce paramétrage ?").pack(fill=BOTH, expand=1, padx=20, pady=20)
		#comment.configur(foreground='red', background='#fff')
		
		self.buttonBox = Pmw.ButtonBox(pframe, labelpos='nw', label_text=None)
		self.buttonBox.pack(fill=BOTH, expand=1, padx=10, pady=10)
		
		bb =self.buttonBox.add('OK',    width=12, command = None)
		bb.bind('<ButtonRelease-1>', lambda  event:     self.buttonPress(event))
		self.buttonBox.add('apply',  	width=12, command = lambda b='apply':  self.buttonPress(b))
		self.buttonBox.add('Annuler', 	width=12,command = lambda b='Annuler': self.buttonPress(b))
		# Set the default button (the one executed when <Enter> is hit).
		self.buttonBox.setdefault('OK')
		self.buttonBox.index('Annuler', 0)
		self.buttonBox.index('OK', 1)
		
		self.root.bind('<Return>', lambda event : self.defaultKey)
		#self.spooler_taches.bind('<Double-ButtonRelease-1>', lambda event : self.lanceTacheInterne(self.spooler_taches.selection_get()))
			
		self.root.focus_set()

	
	def buttonPress(self, btn, event=None):
		if event :
		    #print 'The "%s" button was pressed type event = %s' % (btn, event.type)
		    self.root.destroy()
		    return -1
		    
		else:
		    #print 'The "%s" button was pressed ' % (btn)
		    
		    self.root.destroy()
		    return 99

	def defaultKey(self, event):
	    #
	    self.buttonBox.invoke()
	    self.buttonBox.alignbuttons()
	#----------------------------------------
	# fin des class MessageDialogBoxAs
	#----------------------------------------

#----------------------------------------
# clss spool des transactions
#----------------------------------------
class clss_spool_transactions (Listbox):
	
	def __init__(self, parent) :
		self.parent = parent
		self.tempo_default = 0.5
		self.cycle_default = 1
		self.comment = ""
		self.arg1 = ""
		self.arg2 = ""
		self.arg3 = ""
		self.entry_tempo 	= None
		self.entry_cycle 	= None
		self.entry_comment 	= None
		self.entry_arg1 	= None
		self.buttonBoxOpt	= None
		self.group_cmde		= None
		self.id_scenario_courant = 0
		
		
		self.db_transactions = {}
		self.list_transactions = []
		# init
		self.group_transaction = Pmw.Group(self.parent, tag_text='Liste des transactions ' )
		self.group_transaction.config(padx = 10, pady = 10)
		listBB = Listbox.__init__(self, self.group_transaction.interior(), selectmode=EXTENDED, height=5, width=30)
		
		
	def show_list_transactions(self, lig=0, col=0) :
		#
		self.group_transaction.grid(row=lig, column=col)
		self.ascenseur1 = Scrollbar(self.group_transaction.interior())
		self.ascenseur1.config(command = self.yview)
		self.config(yscrollcommand = self.ascenseur1.set)
		self.config(background='#AFAFAF', foreground='#11F', font = 'Calibri 10 bold')
		self.ascenseur1.pack(side='right')
		self.pack(side='left')
		
	def addTransaction(self,  s_nom, s_tempo=0.5, s_cycle=1, s_comment="", arg1="",arg2="",arg3="") :
		#
		self.tempo 	= s_tempo
		self.nom 	= s_nom
		self.cycle 	= s_cycle
		id_trans	= long(time.time())
		ind = len(self.list_transactions) 
		
		#on ajoute la liste
		
		s_nom = str(ind) + ":" + s_nom
		if self.db_transactions.has_key(self.id_scenario_courant) :
			self.db_transactions[self.id_scenario_courant].append({'id': str(ind), 'nom':s_nom, 'cycle':s_cycle, 'tempo':s_tempo, 'comment':s_comment, 'arg1':arg1 , 'arg2':arg2, 'arg3':arg3})
		else :
			self.db_transactions[self.id_scenario_courant] = []
			self.db_transactions[self.id_scenario_courant].append({'id': str(ind), 'nom':s_nom, 'cycle':s_cycle, 'tempo':s_tempo, 'comment':s_comment, 'arg1':arg1 , 'arg2':arg2, 'arg3':arg3});
		
		self.list_transactions.insert(ind, s_nom )
		
		self.insert(Tkinter.END, s_nom)
		# Mettre a jour les option en double clic ou CTRL+U
		self.bind('<Double-ButtonRelease-1>', lambda event : self.afficheOptionsTransaction(self.curselection()))
		self.bind('<Control-u>', 		lambda event : self.afficheOptionsTransaction(self.curselection()))
		# Suppresseion de la ligne  en double clic ou CTRL+D
		self.bind('<Control-d>', 		lambda event : self.delTransaction(self.curselection()))

		return True
	
	def afficheOptionsTransaction(self, id_curselection) :
		#Suppression des precedent
		self.cancelOptions()
		ind, = id_curselection
		# Suppresion des anciens
		 
		#dans libelle transaction je récupere l'ID 
		lib_element =  self.get(ind)
		t_lib_element = lib_element.split(':')
		 
		vrai_id = t_lib_element[0]
		id_element = int(vrai_id) 
		
		#print self.id_scenario_courant, id_element
		
		options =  self.db_transactions[self.id_scenario_courant][id_element]
		#print self.list_transactions[ind]
		self.group_cmde = Pmw.Group(self.parent, tag_text='commande ...' )
		self.group_cmde.grid(row=2, column=0, columnspan=5)
		
		self.label_opt1 = Label(self.group_cmde.interior(),  text="tempo :") 
		self.label_opt1.grid(row=0, column=0)
		self.label_opt2 = Label(self.group_cmde.interior(),  text="cycle :") 
		self.label_opt2.grid(row=0, column=2)
		self.label_opt3 = Label(self.group_cmde.interior(),  text="comment :") 
		self.label_opt3.grid(row=0, column=4)
		
		self.entry_tempo 	= Entry(self.group_cmde.interior(), width=3, background='#ffffbf', foreground='#000040')
		self.entry_tempo.insert(0, options['tempo'])
		 
		self.entry_cycle 	= Entry(self.group_cmde.interior(), width=3, background='#ffffbf', foreground='#000040')
		self.entry_cycle.insert(0, options['cycle'])
		
		self.entry_comment 	= Entry(self.group_cmde.interior(), width=15, background='#fff', foreground='#000090')
		self.entry_comment.insert(0, options['comment'])
		
		self.entry_argument1 	= Entry(self.group_cmde.interior(), width=15, background='#fff', foreground='#000090')
		self.entry_argument1.insert(0, options['arg1'])
		
		#
		self.entry_tempo.grid(row=0, column=1)
		self.entry_cycle.grid(row=0, column=3)
		self.entry_comment.grid(row=0, column=5)
		
		self.label_opt4 = Label(self.group_cmde.interior(),  text="Arg1 :")
		self.label_opt4.grid(row=0, column=6)
		self.entry_argument1.grid(row=0, column=7)
		
		
		self.entry_tempo.focus()
		 
		self.buttonBoxOpt = Pmw.ButtonBox(self.group_cmde.interior())
		self.buttonBoxOpt.add('Valider',	width=10, command = lambda id=id_element :self.updateListeTransaction(id))
		self.buttonBoxOpt.add('Cancel',		width=10, command = self.cancelOptions)
		self.buttonBoxOpt.grid(row=2, column=0, columnspan=5)
		 
		 
		
		
	def updateListeTransaction(self, id_element) :
		 
		options =  self.db_transactions[self.id_scenario_courant][int(id_element)]
		 
		options['tempo'] 	= self.entry_tempo.get()
		options['cycle'] 	= self.entry_cycle.get()
		options['comment'] 	= self.entry_comment.get()
		options['arg1'] 	= self.entry_argument1.get()
		"""
		options['arg2'] 	= self.entry_argument2.get()
		options['arg3'] 	= self.entry_argument3.get()
		"""
		self.activate(int(id_element))
		self.db_transactions[self.id_scenario_courant][id_element] = options
		#
		self.cancelOptions()
		#
		self.group_cmde = Pmw.Group(self.parent, tag_text='commande ...' )
		self.group_cmde.grid(row=2, column=0, columnspan=5)
		
		self.buttonBoxOpt = Pmw.ButtonBox(self.group_cmde.interior())
		self.buttonBoxOpt.add('Save',		width=10, command = self.updateScenarioFileDataXml)
		self.buttonBoxOpt.add('Cancel',		width=10, command = self.cancelOptions)
		self.buttonBoxOpt.grid(row=2, column=0, columnspan=5)
		 
		 
		
		
	def delTransaction(self, id_curselection=None):
		#
		#print "suppression id  = %s de la selection %s" % (str(id_curselection), str(self.curselection()))
		if id_curselection :
			ind, = id_curselection
			# print self.index(id_curselection)
			#dans libelle transaction je récupere l'ID 
			lib_element =  self.get(ind)
			t_lib_element = lib_element.split(':')
			vrai_id = t_lib_element[0]
			id_element = int(vrai_id )
			 
			# supprimer de la liste 
			del (self.db_transactions[self.id_scenario_courant][id_element])
			#
			#print "suppression de la selection %s" % str(self.curselection())
			self.delete(self.curselection())
			return True
		
		return False
	
	def cancelOptions(self):
		#
		#if isinstance(entry_tempo, Entry) :
		#print "\n entree tempo avant = %s" , self.entry_tempo
		 
		if self.entry_tempo  :
			self.label_opt1.destroy()
			self.label_opt2.destroy()
			self.label_opt3.destroy()
			self.label_opt4.destroy()
			self.entry_tempo.destroy()
			self.entry_tempo = None
			
			self.entry_cycle.destroy()
			self.entry_comment.destroy()
			self.entry_argument1.destroy()
			
			self.buttonBoxOpt.destroy()
			self.group_cmde.destroy()
			
			
			
		
	def getTransaction(self, trans_id=None):
		#
		if trans_id and self.list_transactions.has_key(trans_id) :
			return self.list_transactions.has_key(trans_id)
		else :
			return False
	
	def getListTransactions(self):
		for transaction in self.db_transactions[self.id_scenario_courant] :
			for id, nom, in transaction :
				self.list_transactions.append(nom)
		
		return True
	

	#-------------------------------------------------------------------
	# enregitrement data scenario transations 
	#------------------------------------------------------------------
	def saveFileDataXml(self) :
		#print scenario_list_transactions
		self.dialog3 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
			message_text = 'Souhaiter-vous Enregistrer ce scenario ?',
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
			#-------------------------------------------------------
			# enregitrement des variable user en fichier param.xml
			#-------------------------------------------------------
		fichierData = os.getcwd() + "/data/data_scenario.xml"
	
		maintenant = datetime.now()
		date_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
		t_timestamp =  long(time.time())
		t_id = "SC_" + str(t_timestamp)
		
		if not os.path.isfile(fichierData) :
		    xfout  = open(fichierData, 'w', 'utf-8')
		    enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
		    xfout.write(enteteXML)
		    #on clos
		    xfout.close()
		    #---------------------------------
	
		 
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		
		new_scenario	= self.createElemntXml(xmldoc, 'SCENARIO')
		 
		 
		scenario_id = xmldoc.createAttribute('ID')
		scenario_id.nodeValue = str(t_id)
		new_scenario.setAttributeNode(scenario_id)
		
		scenario_created = xmldoc.createAttribute('CREATED')
		scenario_created.nodeValue = str(date_complet)
		new_scenario.setAttributeNode(scenario_created)
		
		for  options in self.db_transactions[self.id_scenario_courant] :
			#
			#print options  
			#---------------------------------
			# Creer les noeux de transactions
			#---------------------------------
			t_nom 		= options['nom'].split(':')
			nom_transaction	= t_nom[1]
			t_fonction 	= "self." + nom_transaction
			t_cycle 	= options['cycle']
			t_tempo 	= options['tempo']
			t_comment 	= options['comment']
			
			t_arg1	 	= options['arg1']
			t_arg2	 	= options['arg2']
			t_arg3	 	= options['arg3']
			
			new_transaction	= self.createElemntXml(xmldoc, 'TRANSACTION')
			# Ajout de la ligne a la racine de Transaction
			x_name			= self.createElemntXml(xmldoc, 'NOM', 	nom_transaction)
			x_function		= self.createElemntXml(xmldoc, 'FONCTION', t_fonction)
			x_tempo			= self.createElemntXml(xmldoc, 'TEMPO', 	str(t_tempo))
			
			x_cycle 		= self.createElemntXml(xmldoc, 'CYCLE', 	str(t_cycle))
			x_comment		= self.createElemntXml(xmldoc, 'COMMENT', 	t_comment)
			
			x_arg1			= self.createElemntXml(xmldoc, 'ARGUMENT1', 	t_arg1)
			x_arg2			= self.createElemntXml(xmldoc, 'ARGUMENT2', 	t_arg2)
			x_arg3			= self.createElemntXml(xmldoc, 'ARGUMENT3', 	t_arg3)
			
			
			#on ajoute option transaction
			new_transaction.appendChild(x_name)
			new_transaction.appendChild(x_function)
			new_transaction.appendChild(x_tempo)
			new_transaction.appendChild(x_cycle)
			new_transaction.appendChild(x_comment)
			
			new_transaction.appendChild(x_arg1)
			new_transaction.appendChild(x_arg2)
			new_transaction.appendChild(x_arg3)
			
			#on ajoute au  balise transaction au scenario
			new_scenario.appendChild(new_transaction)
		
		 
		root[0].appendChild(new_scenario)
		# ------------------------
		# save contenu en fichier
		# ------------------------
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		#on clos 
		afout.close()
		#
		# remettre a zero le tableau de transaction
		self.db_transactions[self.id_scenario_courant] = []
		
		####
		self.cancelOptions()
		self.delete(0, Tkinter.END)
	
	#-------------------------------------------------------------------
	# Mise a jour data scenario transations 
	#------------------------------------------------------------------
	def updateScenarioFileDataXml(self) :
		#print scenario_list_transactions
		self.dialog3 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
			message_text = 'Souhaiter-vous Mettre a jour ce scenario ?',
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
		#-------------------------------------------------------
		# on charge le fichier data xml en xmldoc
		#-------------------------------------------------------
		fichierData = os.getcwd() + "/data/data_scenario.xml"
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_scenarios = top.getElementsByTagName('SCENARIO')
		
		for scenario in les_scenarios :
			scenario_id = scenario.attributes['ID']
			#
			if scenario_id.value == self.id_scenario_courant :
				#transactionent trouvé 
				#transaction.getElementsByTagName('NOM')[0].firstChild.data = "xxxxxxxx"
				break
		
		indice = 0
		for  options in self.db_transactions[self.id_scenario_courant] :
			#
			#---------------------------------
			# Mettre a jour des transactions
			#---------------------------------

			self.updateBaliseXml(xmldoc, scenario.getElementsByTagName('CYCLE')[indice], 	options['cycle'])
			self.updateBaliseXml(xmldoc, scenario.getElementsByTagName('TEMPO')[indice], 	options['tempo'])
			self.updateBaliseXml(xmldoc, scenario.getElementsByTagName('COMMENT')[indice], 	options['comment'])
			self.updateBaliseXml(xmldoc, scenario.getElementsByTagName('ARGUMENT1')[indice], 	options['arg1'])
			self.updateBaliseXml(xmldoc, scenario.getElementsByTagName('ARGUMENT2')[indice], 	options['arg2'])
			self.updateBaliseXml(xmldoc, scenario.getElementsByTagName('ARGUMENT3')[indice], 	options['arg3'])
			
			# suivant
			indice += 1
		
		# ------------------------
		# save contenu en fichier
		# ------------------------
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		#on clos 
		afout.close()
		
		####
		self.cancelOptions()
		self.delete(0, Tkinter.END)
	#-----------------------------------------------
	# mise a jour balise xml
	#----------------------------------------------	
	def updateBaliseXml(self, xmldoc, elem, data_value) :
		#
		if( elem.hasChildNodes()) :
			elem.firstChild.data =  data_value
		else :	
			# 
			text_xml= xmldoc.createTextNode(data_value)
			elem.appendChild(text_xml)
		return True
	
	def delScenarioFileXml(self, scenario_id=None) :
		#-------------------------------------------------------
		# on charge le fichier data xml en xmldoc
		#-------------------------------------------------------
		if not scenario_id :
			return False
		
		fichierData = os.getcwd() + "/data/data_scenario.xml"
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_scenarios = top.getElementsByTagName('SCENARIO')
		 
		for scenario in les_scenarios :
			#
			if scenario.attributes['ID'].value == scenario_id :
				#transactionent trouvé 
				break
		# suppression element
		top.removeChild(scenario)
		print "suppression de elem %s " % scenario.nodeName
		# ------------------------
		# save contenu en fichier
		# ------------------------
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		#on clos 
		afout.close()
		# refresh la liste des scenario
		self.refreshListeScenariosDispos()
		return True
		
	
	#-----------------------------------------------
	# ajout d'une sequence dans le pooler xml
	#----------------------------------------------
	def createElemntXml(self, xmldoc, lib_balise, texte=None, attrib=None, attrib_Value=None) :
		
		# nouvelle sequence d'expression reguliere
		newXmlElem = xmldoc.createElement(lib_balise)
		if attrib :
			att 	= xmldoc.createAttribute(attrib)
			att.nodeValue = str(attrib_Value)
			newXmlElem.setAttributeNode(att)
		if texte :
			text_xml= xmldoc.createTextNode(texte)
			newXmlElem.appendChild(text_xml)
			
		return newXmlElem
#----------------------------------------
# clss gestion desscenarion 
#----------------------------------------
class clss_gestion_scenarios(clss_spool_transactions) :
	
	def __init__(self, parent) :
		self.parent = parent
		self.seq_compteur = 0
		self.tempo_default = 0.5
		self.cycle_default = 1
		self.comment = ""
		self.arg1 = ""
		self.arg2 = ""
		self.arg3 = ""
		self.entry_tempo 	= None
		self.entry_cycle 	= None
		self.entry_comment 	= None
		self.entry_arg1 	= None
		self.buttonBoxOpt	= None
		self.group_cmde		= None
		
		self.db_transactions = {}
		self.list_transactions = []
		self.id_scenario_courant = None
		# init 
		clss_spool_transactions.__init__(self, self.parent)

	#---------------------------
	#- Affichage des composents
	#---------------------------
	
	def show_list_scenarios(self) :
		
		# 1- affichage liste des scenario
		self.group_scenarios_dispos = Pmw.Group(self.parent, tag_text='Liste des scenarios ' )
		self.group_scenarios_dispos.config(padx = 10, pady = 10)
		self.group_scenarios_dispos.grid(row=0, column=0)
		
		self.list_scenarios_dispos = Listbox(self.group_scenarios_dispos.interior(), selectmode=EXTENDED, height=5, width=30)
		self.ascenseur_scenario = Scrollbar(self.group_scenarios_dispos.interior())
		self.ascenseur_scenario.config(command = self.list_scenarios_dispos.yview)
		
		self.list_scenarios_dispos.config(yscrollcommand = self.ascenseur_scenario.set)
		self.list_scenarios_dispos.config(background='#AFAFAF', foreground='#11F', font = 'Calibri 10 bold')
		
		self.list_scenarios_dispos.pack(side='left')
		self.ascenseur_scenario.pack(side='right')
		#self.list_scenarios_dispos.grid(row=0, column=1)
		#self.ascenseur1.grid(row=0, column=1)
		
		
		# 2- affichage image refreash
		self.img_refresh = PhotoImage(file = "images/refreach_2.gif" , height=40, width=40 )
		bt_refresh = Button(self.parent, text='Refresh', image=self.img_refresh, command=self.refreshListeScenariosDispos )
		#bt_refresh.pack()
		bt_refresh.grid(row=0, column=1)
		
		# 3- Affichage des transactions du scenario
		#self.pack(side='right')
		
		self.show_list_transactions(0, 2)
		# on charge la listBox
		self.chargeListeScenariosDispos()
	
	
	def addTransaction(self, scenario_id=None, s_nom="", s_tempo=0.5, s_cycle=1, s_comment="", arg1="",arg2="",arg3="") :
		#
		self.tempo 	= s_tempo
		self.nom 	= s_nom
		self.cycle 	= s_cycle
		id_trans	= long(time.time())
		
		#on ajoute la liste
		s_nom = str(self.seq_compteur) + ":" + s_nom
		new_elem = {'id': str(self.seq_compteur), 'nom':s_nom, 'cycle':s_cycle, 'tempo':s_tempo, 'comment':s_comment, 'arg1':arg1 , 'arg2':arg2, 'arg3':arg3}
		
		
		if scenario_id == None :
			scenario_id = 99
		
		
		if self.db_transactions.has_key(scenario_id) :
		
			self.db_transactions[scenario_id].insert(self.seq_compteur, new_elem )
			 
			 
			 
		else :
			self.db_transactions [scenario_id]  = []
			self.db_transactions[scenario_id].insert(self.seq_compteur, new_elem )

		self.list_transactions.insert(self.seq_compteur, s_nom )
		self.insert(Tkinter.END, s_nom)

		# Mettre a jour les option en double clic ou CTRL+U
		self.bind('<Double-ButtonRelease-1>', 		lambda event : self.afficheOptionsTransaction(self.curselection()))
		self.bind('<Control-u>', 		lambda event : self.afficheOptionsTransaction(self.curselection()))
		# Suppresseion de la ligne  en double clic ou CTRL+D
		self.bind('<Control-d>', 		lambda event : self.delTransaction(self.curselection()))
		
		# incremente
		self.seq_compteur = self.seq_compteur + 1
		

		return True
	
	def getScenarioId(self) :
		#
		return self.id_scenario_courant;
		
		
	def refreshListeScenariosDispos(self) :
		#
		return self.chargeListeScenariosDispos()
		
	#------------------------------
	# charger liste des scenario
	#-------------------------
	def getListScenarios(self):
		##
		tab_transactions = self.chargeFichierSenariosXml()
		#print id, data[0]['NAME']
		list_scenario = []
		for elem in tab_transactions  :
			for id_scenario, data in  elem.items() :
				list_scenario.append(id_scenario)
				
				
		return list_scenario


	def chargeListeScenariosDispos(self) :
		 
		# list des transaction scenarion  
		list_scenarios = self.getListScenarios()
		 
		# init a vide
		self.list_scenarios_dispos.delete(0, Tkinter.END)
		#
		for element in list_scenarios :
			## boucle de remplissage lite
			self.list_scenarios_dispos.insert(END, element)
			self.list_scenarios_dispos.bind('<Double-ButtonRelease-1>', lambda event : self.selectionnerScenario(self.list_scenarios_dispos.selection_get()))
			#
			self.list_scenarios_dispos.bind('<Control-d>', lambda event : self.delScenarioFileXml(self.list_scenarios_dispos.selection_get()))
		self.list_scenarios_dispos.focus_force()
		self.list_scenarios_dispos.select_set(0, 0)
			 
		return True

	def selectionnerScenario(self, id_scenario) :
		self.id_scenario_courant = id_scenario
		# efface l'ecran de controle sur les lignes
		self.cancelOptions()
		# on recherche id contenue dans les scenario
		list_transactions = self.getTransactionsScenario(id_scenario)
		#init
		self.seq_compteur = 0
		self.db_transactions[id_scenario] = []
		
		 
		self.delete(0, END)
		for element in list_transactions :
			# Ajout des transaction a la liste
			self.addTransaction(id_scenario, element['NOM'], element['TEMPO'], element['CYCLE'], element['COMMENT'], element['ARGUMENT1'])
			 
			
		
	# recupere qu'une liste des nom de transaction 
	def getTransactionsScenarioName(self, scenario_id):
		##(scenario_id.value, created.value) : spool_transactions_xml}
		##
		tab_transactions = self.chargeFichierSenariosXml()
		#print id, data[0]['NAME']
		list_trans = []
		for elem in tab_transactions  :
			for id, data in  elem.items() :
				if id == scenario_id :
					for transaction in data :
						list_trans.append(transaction['NOM'])
					break;
				
		return list_trans
	
	# recupere data transaction 
	def getTransactionsScenario(self, scenario_id):
		##(scenario_id.value, created.value) : spool_transactions_xml}
		##
		tab_transactions = self.chargeFichierSenariosXml()
		#print id, data[0]['NAME']
		list_trans = []
		for elem in tab_transactions  :
			for id, data in  elem.items() :
				if id == scenario_id :
					for transaction in data :
						list_trans.append(transaction)
					break;
				
		return list_trans
	#---------------------------------
	# charger les transactions XML
	#---------------------------------	
	def chargeFichierSenariosXml(self, s_default=False) :
		"""
		"""
		options_transaction_xml = {}
		list_scenario_xml = []
		spool_transactions_xml = []
		if s_default  :
			fichierData = os.getcwd() + "/data/scenario_default.xml"
		else :
			
			fichierData = os.getcwd() + "/data/data_scenario.xml"
			if not os.path.isfile(fichierData ) :
				fichierData = os.getcwd() + "/data/scenario_default.xml"
				
		
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		
		top = root[0]
		tac = top.firstChild
		
		#last = self.getLastchild(top)		
	
		if(tac == None) : 
			return []
	
		while (tac and tac.nodeType == 1) :
			
			spool_transactions_xml = []
			# tac == SCENARIO
			if (tac.hasAttributes()) :
				#
				scenario_id = tac.attributes['ID']
				created = tac.attributes['CREATED']
				
				#print scenario_id.name, scenario_id.value
				
			#print "name = %s , nodetype ==> %s" % ( tac.localName, tac.nodeType )
			
			# deroulement des transactions 
			if(tac.hasChildNodes()) :
				#
				for transaction in tac.childNodes :
					options_transaction_xml = {}
					#
					options_transaction_xml['NOM'] 	= transaction.getElementsByTagName('NOM')[0].firstChild.data
					options_transaction_xml['FONCTION'] 	= transaction.getElementsByTagName('FONCTION')[0].firstChild.data
					if transaction.getElementsByTagName('TEMPO')[0].hasChildNodes() :
						options_transaction_xml['TEMPO'] = transaction.getElementsByTagName('TEMPO')[0].firstChild.data
					else :
						options_transaction_xml['TEMPO'] = 1
					
					if transaction.getElementsByTagName('CYCLE')[0].hasChildNodes() :	
						options_transaction_xml['CYCLE'] = transaction.getElementsByTagName('CYCLE')[0].firstChild.data
					else :
						options_transaction_xml['CYCLE'] = 1
					
					if( transaction.getElementsByTagName('ARGUMENT1') and transaction.getElementsByTagName('ARGUMENT1')[0].hasChildNodes()) : 
						options_transaction_xml['ARGUMENT1'] 	= transaction.getElementsByTagName('ARGUMENT1')[0].firstChild.data
									
					if( tac.getElementsByTagName('COMMENT')[0].hasChildNodes()) : 
						options_transaction_xml['COMMENT'] = tac.getElementsByTagName('COMMENT')[0].firstChild.data
					else :
						options_transaction_xml['COMMENT'] = ""
						
					if( tac.getElementsByTagName('ARGUMENT1')[0].hasChildNodes()) : 
						options_transaction_xml['ARGUMENT1'] = tac.getElementsByTagName('ARGUMENT1')[0].firstChild.data
					else :
						options_transaction_xml['ARGUMENT1'] = ""
					
					if( tac.getElementsByTagName('ARGUMENT2')[0].hasChildNodes()) : 
						options_transaction_xml['ARGUMENT2'] = tac.getElementsByTagName('ARGUMENT2')[0].firstChild.data
					else :
						options_transaction_xml['ARGUMENT2'] = ""
						
					if( tac.getElementsByTagName('ARGUMENT3')[0].hasChildNodes()) : 
						options_transaction_xml['ARGUMENT3'] = tac.getElementsByTagName('ARGUMENT3')[0].firstChild.data
					else :
						options_transaction_xml['ARGUMENT3'] = ""
					
					
					# ajout
					#print options_transaction_xml
					spool_transactions_xml.append(options_transaction_xml)
			#
			list_scenario_xml.append({scenario_id.value : spool_transactions_xml})
			if (tac == root[0].lastChild) :
				break;
			# suivant 
			tac = tac.nextSibling;
			
			
			 
		## fermeture des flux fichiers
		
		return list_scenario_xml
		

	#---------------------------------
	# fin class clss_gestion_scenarios
	#---------------------------------	

	
	#---------------------------------
	# CLASS Campagne de test xml
	#---------------------------------	
	
class ClssCampagneTests :
	
	def __init__(self) :
		# init
		self.tab_transaction 		= []
		self.campagne_scenario_id 	= None
		self_campagne_created		= None
		self.duree_campagne 		= 0
		self.nb_modif_chrono 		= 0
		self.nb_connexions		= 0
		self.nb_plantage_modif_chrono 	= 0
		self.heure_fin_campagne 	= 0
		self.heure_debut_campagne 	= None
		self.nb_transactions		= 0
		
	def startCampagne(self, campagne_id) :	
		# on charge le fichier
		self.campagne_id_courant 	= campagne_id
		self.tab_transaction = self.chargeCampagneXmlById(campagne_id)
		self.statCampagneTests()
		
	
	#---------------------------------
	# charger les transactions XML
	#---------------------------------	
	def chargeCampagneXmlById(self, campagne_id=False) :
		"""
		"""
		self.nb_modif_chrono 	= 0
		self.nb_connexions	= 0
		self.nb_plantage_modif_chrono 	= 0
		self.heure_fin_campagne 	= 0
		self.heure_debut_campagne 	= None
		self.nombre_cycle = 0
		self.version_word		= None
		
		options_transaction_xml = {}
		list_scenario_xml = []
		spool_transactions_xml = []
		if campagne_id  :
			fichierData = os.getcwd() + "/data/data_campagne.xml"
		else :
			return []
	
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		# on pointe ma 1er Campagne
		compagne_trouve = None
		cap = root[0].firstChild
		# recherche de campagne_id
		while (cap and cap.nodeType == 1) :
			#
			if (cap.hasAttributes()) :
				#
				campagne_id			= cap.attributes['ID'].value
				self_campagne_created 		= cap.attributes['CREATED'].value
				self.campagne_scenario_id 	= cap.attributes['SCENARIO_ID'].value
				self.nombre_cycle		= cap.attributes['NB_CYCLE'].value
				self.version_word		= cap.attributes['VERSION_WORD'].value
				
				if campagne_id == self.campagne_id_courant :
					#print "** ===> on a trouve notre campagne %s " % campagne_id_courant.value
					compagne_trouve = cap.firstChild
					break;
				else :
					cap = cap.nextSibling
					
		# on cherche les transaction de cette campagne
		if compagne_trouve == None :
			return []
		
		 
		last = cap.lastChild		
	
		 
		while (compagne_trouve and compagne_trouve.nodeType == 1) :
			#print "** ===> action = %s " % compagne_trouve.getElementsByTagName('ACTION')[0].firstChild.data 
			# deroulement des transactions 
			options_transaction_xml = {}
			# ajout
			
			t_action =  compagne_trouve.getElementsByTagName('ACTION')[0].firstChild.data
			options_transaction_xml["ACTION"] = t_action
	
			t_delta	= compagne_trouve.getElementsByTagName('T_DELTA')[0].firstChild.data
			options_transaction_xml['T_DELTA'] = t_delta
			
			t_timestamp = compagne_trouve.getElementsByTagName('T_TIMESTAMP')[0].firstChild.data
			options_transaction_xml['T_TIMESTAMP'] = t_timestamp
			
			t_heure	= compagne_trouve.getElementsByTagName('T_HEURE')[0].firstChild.data
			options_transaction_xml['T_HEURE'] = t_heure
	
			d_source = compagne_trouve.getElementsByTagName('T_DATE')[0].firstChild.data
			options_transaction_xml['T_DATE'] = d_source
			
			if( compagne_trouve.getElementsByTagName('MESSAGE')[0].hasChildNodes()) : 
			    message =  compagne_trouve.getElementsByTagName('MESSAGE')[0].firstChild.data
			    options_transaction_xml['MESSAGE'] = message 
			
			###------------    
			spool_transactions_xml.append(options_transaction_xml)
				
			# suivant 
			compagne_trouve = compagne_trouve.nextSibling;
			 
		## fermeture des flux fichiers
		#print spool_transactions_xml
		
		return spool_transactions_xml
	
	
		
	def statCampagneTests(self, tab_transaction=None):
		#
		self.nb_modif_chrono 	= 0
		self.nb_connexions	= 0
		self.nb_plantage_modif_chrono 	= 0
		compteur1 = 0
		
		tab_transaction = self.tab_transaction
		
		#connexionAppliSusie
		for transaction in self.tab_transaction :
			 
			if transaction['ACTION'].find( "connexionAppliSusie") != -1  :
				self.nb_connexions += 1
			#
			if transaction['ACTION'].find( "Word") != -1  or transaction['ACTION'].find( "modifier") != -1:
				self.nb_modif_chrono += 1
			#
			if compteur1 == 0 :
				self.heure_debut_campagne = transaction['T_DATE']
				self.campagne_created = transaction['T_DATE']
			
			element = transaction['ACTION']
			#print "***==> action avant = %s " % element
			if element.find('PLANTAGE_SUSIE', 0) != -1:
				self.nb_plantage_modif_chrono += 1
				#print element.find('PLANTAGE_SUSIE')
				#print " action apres %s nbre de plantage= %s " % (element, self.nb_plantage_modif_chrono)
			
			compteur1 += 1
			self.heure_fin_campagne = transaction['T_DATE']
		
		#
		self.nb_transactions = compteur1
		
			
	
	# get scenario id 
	def getNombreTransactions(self) :
		return self.nb_transactions	
	# get scenario id 
	def getCampagneScenarioId(self) :
		return self.campagne_scenario_id
	# donner la date de creation
	def getDateCreated(self) :
		return self.campagne_created
	# donner id de la campagne
	def getCampagneIdCourant(self) :
		return self.campagne_id_courant
	#--
	def getDureeCampagne(self) :
		return self.duree_campagne
	
	# get nbre de connextion
	def getNombreConnexion(self) :
		#
		return self.nb_connexions
		
	
	# get nbre de connextion
	def getNombreModifChrono(self) :
		return self.nb_modif_chrono 
		
	# get nbre de connextion
	def getNombrePlantageBureuatique(self) :
		#
		return self.nb_plantage_modif_chrono
		
	# get nbre de connextion
	def getNombreConnexion(self) :
		#
		return self.nb_connexions
		 
		
	# get nbre de connextion
	def getHeureFinCampagne(self) :
		return self.heure_fin_campagne
		
	# get nbre de connextion
	def getHeureDebutCampagne(self) :
		return self.heure_debut_campagne
		
	# get nbre de connextion
	def getDureeCampagne(self) :
		return int(self.heure_fin_campagne) - int(self.heure_debut_campagne)
	
	# get liste Transactions Campagne 
	def getListTransactionsCampagne(self) :
		return self.tab_transaction
	# get liste Transactions Campagne 
	def getNombreCycle(self) :
		return self.nombre_cycle
	# get liste Transactions Campagne 
	def getNombreCycle(self) :
		return self.nombre_cycle
	# get liste Transactions Campagne 
	def getVersionWord(self) :
		return self.version_word
	
	
	
	
#-----------------------------------
# fin de class ClssCampagneTests
#------------------------------------


#-----------------------------------
# class ClssCampagneTests
#------------------------------------
class ClssGestionCampagne :
	
	def __init__(self) :
		# init
		list_des_scenarios 	= []
		self.tabListCampagne 	= []
		self.spooler_campagnes  = None
		
	def statTouteCampagnes(self) :
		tab_clss_test = []
		tab_stat_campagne = [] 
		#
		self.tab_list_scenarios = self.getListCampagneFromFileXml()
		# 2- pour charque scenario des stat  
		for options  in self.tab_list_scenarios :
			campagne_id = options['campagne_id']
			#print campagne_id
			clss_test = ClssCampagneTests()
			clss_test.startCampagne(campagne_id )
			tab_clss_test.append(clss_test)
			
			
		# calcul des stat
		for lig in tab_clss_test :
			# calcul taux de plantage
			if lig.getNombreModifChrono() > 0 :
				taux_plantage =  "%2.1f " % (100 * lig.getNombrePlantageBureuatique() / lig.getNombreTransactions())
			else :
				taux_plantage = 0
			
			pourcent_plantage = 0
			stat1 = {
				'Campagne id'			: lig.getCampagneIdCourant(),
				'Scenario id'			: lig.getCampagneScenarioId(),
				'created'			: lig.getDateCreated(),
				'Nb Transactions' 		: lig.getNombreTransactions(),
				'Nb de Modif Courrier' 		: lig.getNombreModifChrono(),
				'Nb de plantage' 		: lig.getNombrePlantageBureuatique(),
				'Pourcent echecs' 		: taux_plantage
			}
			tab_stat_campagne.append(stat1)
			 
			
		return tab_stat_campagne


	#-------------------------------------------------------
	# on charge le fichier data xml des scenario
	#-------------------------------------------------------
	def getListScenarioFromFileXml(self) :
		
		list_des_scenarios = [] 
		
		fichierData = os.getcwd() + "/data/data_scenario.xml"
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_scenarios = top.getElementsByTagName('SCENARIO')
		 
		for scenario in les_scenarios :
			#
			list_des_scenarios.append(scenario.attributes['ID'].value )
			
		return 	list_des_scenarios
	

	#-------------------------------------------------------
	# on charge le fichier data xml des scenario
	#-------------------------------------------------------
	def getListTransactionsScenarioFromFileXml(self, scenario_id) :
		list_des_transactions = [] 
		fichierData = os.getcwd() + "/data/data_scenario.xml"
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_scenarios = top.getElementsByTagName('SCENARIO')
		# 
		for scenario in les_scenarios :
			#
			if scenario.attributes['ID'].value == scenario_id :
				#
				
				for transaction in scenario.childNodes :
					options_transaction_xml = {}
					options_transaction_xml['NOM'] = transaction.getElementsByTagName('NOM')[0].firstChild.data
					list_des_transactions.append(options_transaction_xml)
					
		return 	list_des_transactions

	#-------------------------------------------------------
	# on charge le fichier data xml des scenario
	#-------------------------------------------------------
	def getListCampagneFromFileXml(self) :
		
		list_des_campagnes = [] 
		
		if os.path.isfile(os.getcwd() + "/data/data_campagne.xml") :
			
			fichierData = os.getcwd() + "/data/data_campagne.xml"
		else :
			return False
			
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_campagnes = top.getElementsByTagName('CAMPAGNE')
		 
		for campagne in les_campagnes :
			#
			if (campagne.hasAttributes()) :
				#
				options = dict(
					campagne_id 	= campagne.attributes['ID'].value,
					created 	= campagne.attributes['CREATED'].value,
					scenario_id 	= campagne.attributes['SCENARIO_ID'].value
				)
			list_des_campagnes.append(options )
			
		return 	list_des_campagnes
	

	def interfacePrintCampagne(self):
		#
		##---------------------------------
		## ListSelect  list Campagne Execute
		##---------------------------------
		self.tabListCampagne =  self.getListCampagneFromFileXml()
		  
		if self.tabListCampagne == False :
			return False
		root = Tkinter.Tk()
		root.option_add('*background', '#D0E3FF')
		root.option_add('*foreground', "#222")
		root.title('print Campagne')
		header = "|%30s|%20s|%20s|" % ( 'Date', 'Campagne_id', 'Scenario_id')
		group_campagne = Pmw.Group(root, tag_text= header )
		group_campagne.pack(side='top',   expand = 0, padx = 2, pady = 2)
		
		self.spooler_campagnes = Listbox(group_campagne.interior(), selectmode=EXTENDED, height=10, width=60)
		ascenseur2 = Scrollbar(group_campagne.interior())
		
		ascenseur2.config(command = self.spooler_campagnes.yview)
		self.spooler_campagnes.config(yscrollcommand = ascenseur2.set)
		self.spooler_campagnes.config(background='#FFF', foreground='#13F',  font = 'Calibri 10 bold')
		
		self.spooler_campagnes.grid(row=0, column=0) 
		ascenseur2.grid(row=0, column=1)
		#
		
		ind = 0
		#  header
		header = "|%14s|%14s|%14s|" % ( 'Date', 'Campagne_id', 'Scenario_id')
		#self.spooler_campagnes.insert(ind, header)
		for elem in self.tabListCampagne :
			#
			self.spooler_campagnes.insert(ind, '%s|%s|%s|%s' % (ind, elem['created'][:16], elem['campagne_id'], elem['scenario_id']) )
			self.spooler_campagnes.bind('<Double-ButtonRelease-1>', lambda event : self.printRapportHtml(self.spooler_campagnes.selection_get(), True))
			self.spooler_campagnes.bind('<Control-d>', 	lambda event : self.deleteCampagne(self.spooler_campagnes.selection_get()))
			ind = ind + 1
		#
		self.spooler_campagnes.focus_force()
		self.spooler_campagnes.activate(0)
		self.spooler_campagnes.select_set(0, 0)
				
		buttonBox = Pmw.ButtonBox(root)
		buttonBox.add('print rapport Campagne', width=25, command = lambda : self.printRapportHtml(self.spooler_campagnes.selection_get()))
		buttonBox.add('Synthese Campagnes', 	width=25, command = self.printSyntheseCampagnes)
		
		buttonBox.add('graphique perf',	width=25, command = lambda b=True : self.printGraphePlantage(self.spooler_campagnes.selection_get()))
		buttonBox.add('graphique perf chrono',	width=25, command = lambda b=False : self.printGraphePlantage(self.spooler_campagnes.selection_get(), b))
		buttonBox.add('Quitter', width=20, command = root.destroy)
		
		buttonBox.pack(side='bottom')
		return True
	
	
	
	#--------------------------------------------------------------
	#--- impression en html du rapport campagne
	#--------------------------------------------------------------
	def printRapportHtml(self, campagne_id=None, type_total=True) :
		
		corpHTML = ""
		enteteHMTL = ""
		tab_transaction = []
		
		#---------------------------
		# init des  Class
		#---------------------------
		t_campagne_id  	= campagne_id.split('|')
		campagne_id 	= t_campagne_id[2].strip()
		clssCampagneTests = ClssCampagneTests()
		clssCampagneTests.startCampagne(campagne_id)
		scenario_id = clssCampagneTests.getCampagneScenarioId()
		
		
		if campagne_id == None :
			return False
		# charger les pointages des sequences scenario "Modification chrono"
		if (type_total == True):
			# modif as xxx tab_transaction = chargeTransactionsXml(type_total)
			tab_transaction = clssCampagneTests.getListTransactionsCampagne() 
			if tab_transaction == None :
				return False 
		else :
			tab_transaction = clssCampagneTests.getListTransactionsCampagne()
			

		if len(tab_transaction) == 0 :
			return False
		
		
		version_word = "Word" + "2003";
		
		if (type_total == True):
			titre = "Application: SUSIE - %s - 10b - Scenario %s (du %s au %s)" % (clssCampagneTests.getVersionWord(),
											       clssCampagneTests.getCampagneScenarioId() ,
											       clssCampagneTests.getHeureDebutCampagne(),
											       clssCampagneTests.getHeureFinCampagne())
		else :
			titre = "Application: SUSIE - %s  - 10b - OuvrirChrono_ModifierCourrier_RetourSusie (du %s au %s)" % (version_word, clssCampagneTests.getHeureDebutCampagne(),
															      clssCampagneTests.getHeureFinCampagne())

		ind = 1
		date_complet = self.getDateJour()
	
		# 2 ieme partie Description Scenario

		contenue_table1 = ""
		listTrans = self.getListTransactionsScenarioFromFileXml(scenario_id)
		
		for transaction in listTrans :
			contenue_table1 += "<tr><td>%s</td></tr>" % transaction['NOM']
		
		# 2 ieme partie stat de Campagne
		contenue_table2 = ""
		
		if clssCampagneTests.getNombreModifChrono() > 0 and clssCampagneTests.getNombreModifChrono() > 0 :
			taux_plantage =  "%2.1f " % (100 * clssCampagneTests.getNombrePlantageBureuatique() / clssCampagneTests.getNombreTransactions())
		else :
			taux_plantage = 0

		ligne = ""
		ligne_td = self.add_td("%s")
		ligne += ligne_td * 8 % (
			clssCampagneTests.getCampagneIdCourant(),
			clssCampagneTests.getCampagneScenarioId(),
			str(clssCampagneTests.getNombreCycle()),
			str(clssCampagneTests.getNombreTransactions()),
			str(clssCampagneTests.getNombreConnexion()),
			str(clssCampagneTests.getNombreModifChrono()),
			str(clssCampagneTests.getNombrePlantageBureuatique()) ,
			str(taux_plantage) + chr(0x25)
		)
		contenue_table2 += self.add_tr(ligne)
		 
		contenue_table3 = ""
		for elem in tab_transaction :
			delta = elem['T_DELTA']
			adate = elem['T_DATE']
			
			ligne = ""
			
			ligne += self.add_td( str(ind))

			if delta == '0.0' :
				 
				ligne += self.add_td(elem['ACTION'], 'erreur')
			else :
				
				ligne += self.add_td(elem['ACTION'])
				
			ligne += self.add_td( elem['T_DATE'][:10])
			ligne += self.add_td( elem['T_HEURE'])
			ligne += self.add_td( elem['T_TIMESTAMP'])
			ligne += self.add_td( elem['T_DELTA'][:4])
			
			if (elem.has_key('MESSAGE') and elem['MESSAGE'] and elem['MESSAGE'] != 'None') :
				ligne += self.add_td(elem['MESSAGE'], 'erreur')
			else :
				ligne += self.add_td(" ")
			# append ligne 
			contenue_table3 += self.add_tr(ligne)
			ind = ind + 1 
		
		
		#---------------------
		#ecriture en fichier
		#---------------------
		## ouvrir le fichier html
		frout = open(os.getcwd() + "/out/reportSusieRebot.html", 'w') ## Ouvrir fichier resultat
		fic_template = open(os.getcwd() + "/layout/layout_rebot.tmpl", 'r') ## Ouvrir fichier template
		
		# Ecriture de contenue
		templ_layout = fic_template.read()
		#chtt2 = Template(templ_layout)
		
		#s = Template('$titre $scenario_id titre_h1 date_jour contents_table1 contents_table2 contents_table3')
		s = Template(templ_layout)
		 
		d = dict(titre = titre,
			scenario_id 	=  clssCampagneTests.getCampagneScenarioId(),
			titre_h1 		= "SUSIE: SCENARIO DE MESURE DE PERFORMANCE APPLICATIVE",
			date_jour 		= date_complet,
			contents_table1 	= contenue_table1,
			contents_table2 	= contenue_table2,
			contents_table3 	= contenue_table3
		)
		s_out = s.safe_substitute(d) 

		frout.write(s_out)
		
		# cloture des fichiers 
		frout.close()
		fic_template.close()
		
		## lancer navigateur Fire fox pour l'edition
		clssRunExplorer = MultiThread( 'C:/Program Files/Mozilla Firefox/firefox.exe', os.getcwd() + "/out/reportSusieRebot.html")
		clssRunExplorer.run()
		return True
	
	#--------------------------------------------------------------
	#--- print Graphe activite campagne
	#--------------------------------------------------------------
	def printGraphePlantage(self, campagne_id, total=True) :
		#
		t_temps = []
		t_delta = []
		t_temps_total = []
		t_delta_total = []
		tab_transaction = []
		
		t_campagne_id  = campagne_id.split('|')
		campagne_id = t_campagne_id[2].strip()
		
		 
		# label des axes
		xlabel('timestamp (s)')
		ylabel('delta exec (s)')
		
		# charger les pointages des sequences scenario "Modification chrono"
		clssCampagneTests = ClssCampagneTests()
		clssCampagneTests.startCampagne(campagne_id)
		tab_transaction_total = clssCampagneTests.getListTransactionsCampagne()
		 
		if  len(tab_transaction_total) == 0 :
			return False
		
		
		# etendre le tableau adate de + 1
		x_atab = self.etendreValeurTab(t_temps, 0)
		 
		
		#axis( t_temps ) xmax, 
		
		if total == True :
			title( 'SUSIE: SCENARIO DE MESURE DE PERFORMANCE APPLICATIVE ' )
			for elem in tab_transaction_total :
				#
				delta = elem['T_DELTA']
				adate = elem['T_TIMESTAMP']
				t_temps_total.append(float(adate))
				t_delta_total.append(float(delta))
		
			
			
		else  :
			title( 'SUSIE: SCENARIO DE MESURE DE PERFORMANCE BUREAUTIQUE ' )
			for elem in tab_transaction_total :
				if elem['ACTION'] == "piloterOfficeWord" :
					delta = elem['T_DELTA']
					adate = elem['T_TIMESTAMP']
					t_temps_total.append(float(adate))
					t_delta_total.append(float(delta))
		
		plot(t_temps_total, t_delta_total)

		savefig(os.getcwd() + '/out/rebot_graph.png', dpi=300)
		## lancer navigateur Fire fox pour l'edition
		## lancer navigateur Fire fox pour l'edition
		clssRunExplorer = MultiThread( 'C:/Program Files/Mozilla Firefox/firefox.exe', os.getcwd() + "/out/rebot_graph.png")
		clssRunExplorer.run()
		return True
		 
	
	
	def printSyntheseCampagnes(self) :
		
		corpHTML = ""
		enteteHMTL = ""
		tab_transaction = []
		
		#---------------------------
		# la Class
		clss1 = ClssGestionCampagne()
		
		
		#--------------------------------
		# contruire tableau synthese stat
		#--------------------------------
		tab_stat_campagne = clss1.statTouteCampagnes()
		header_keys = tab_stat_campagne[0].keys()
		 
		# entete page HTML
		tete_stat = ""
		for titre in header_keys :
			tete_stat += self.add_th(titre, 'titre2')
			
			
		tete_stat = self.add_tr(tete_stat)
		
		corp_stat = ""
		for elem in tab_stat_campagne :
			#
			ligne = ""
			for data in elem.values() :
				#
				ligne += self.add_td(str(data))
			
			corp_stat += self.add_tr(ligne)
		
		
		#---------------------
		#ecriture en fichier
		#---------------------
		## ouvrir le fichier html
		frout = open(os.getcwd() + "/out/syntheseSusieRebot.html", 'w') ## Ouvrir fichier resultat
		fic_template = open(os.getcwd() + "/layout/layout_synthes.tmpl", 'r') ## Ouvrir fichier template
		
		# Ecriture de contenue
		date_du_jour = self.getDateJour()
		templ_layout = fic_template.read()
		
		
		
		s = Template(templ_layout)
		 
		d = dict(titre = titre,
			contents_titre	= "SYNTHESE SCENARIO DE MESURE DE PERFORMANCE APPLICATIVE" ,
			contents_header1	= tete_stat,
			date_jour 		= date_du_jour[0:10],
			contents_table1 	= corp_stat
		)
		s_out = s.safe_substitute(d) 

		frout.write(s_out)
	
		# cloture des fichiers 
		frout.close()
		fic_template.close()
		
		## lancer navigateur Fire fox pour l'edition
		clssRunExplorer = MultiThread( 'C:/Program Files/Mozilla Firefox/firefox.exe', os.getcwd() + "/out/syntheseSusieRebot.html")
		clssRunExplorer.run()
		
		
		
		return
		
		 
	def add_td(self, data=None, style_class='') :
		#
		"""
		renvoie une format <td>
		"""
		return "<td class='%s'>%s</td>" % ( style_class, data)
		
	
	def add_tr(self, data=None, style_class='') :
		#
		"""
		renvoie une format <tr>
		"""
		return "<tr class='%s'>%s</tr>" % (style_class, data)
		
	def add_th(self, data=None, style_class='') :
		#
		"""
		renvoie une format <th>
		"""
		return "<th class='%s'>%s</th>" % (style_class, data)
	
	def getDateJour(self) :
		maintenant = datetime.now()
		return maintenant.strftime("%d-%m-%Y %H:%M")

	def etendreValeurTab(self, atab, increm=1) :
		#
		xtab = []
		ind = 0
		for elem in atab :
			ind = ind + increm
			xtab.append(elem + ind)
			#print elem + ind
		return xtab
	
	def test_schelduler(self) :
		my_Scheduler = Scheduler()
		my_Scheduler.schedule("toto", datetime.now(), my_Scheduler.every_x_mins(0.10),	self.info_toto);
		# Add the foo task, a receipt is returned that can be used to drop the task from the Scheduler
		#foo_receipt = my_Scheduler.schedule_task(foo_task)
		# Once started, the Scheduler will identify the next task to run and execute it.
		#my_Scheduler.start()
		my_Scheduler.run()
		
		
	def info_toto(self) :
		print " schelduler what else ? .."
		
	def deleteCampagne(self, campagne_id=None):
		#
		#print "suppression id  = %s de la selection %s" % (str(id_curselection), str(self.curselection()))
		if campagne_id == None:
			return False
		
		
		t_campagne_id  	= campagne_id.split('|')
		campagne_id 	= t_campagne_id[2].strip()
		index = t_campagne_id[0].strip()
		#print "suppression de la selection %s" % str(self.curselection())
		# supprimer de la liste
		del(self.tabListCampagne[int(index)])
		print campagne_id
		print t_campagne_id
		
				 
		#
		#-------------------------------------------------------
		# on charge le fichier data xml en xmldoc
		#-------------------------------------------------------
		fichierData = os.getcwd() + "/data/data_campagne.xml"
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_campagnes = top.getElementsByTagName('CAMPAGNE')
		 
		for campagne in les_campagnes :
			if (campagne.hasAttributes()) :
				if campagne.attributes['ID'].value == campagne_id :
					#transactionent trouvé 
					# suppression element
					top.removeChild(campagne)
					print "suppression de elem %s " % campagne.nodeName
					# ------------------------
					# save contenu en fichier
					# ------------------------
					contenueXml = xmldoc.toxml()
					# save contenu en fichier
					afout  = open(fichierData, 'w', 'utf-8')
					afout.write(contenueXml)
					#on clos 
					afout.close()
					# refresh la liste des campagne
					self.refreshListeCampagne()
					
		return True
	
	#----------------------------------
	#-- 
	#----------------------------------
	def refreshListeCampagne(self)  :
		ind = 0
		self.spooler_campagnes.delete(0, 'end')
		
		for elem in self.tabListCampagne :
			#
			self.spooler_campagnes.insert(ind,  ' | ' + elem['created'][:16] + ' | ' +  elem['campagne_id'] + ' | ' +  elem['scenario_id'])
			self.spooler_campagnes.bind('<Double-ButtonRelease-1>', lambda event : self.printRapportHtml(self.spooler_campagnes.selection_get(), True))
			self.spooler_campagnes.bind('<Control-d>', 		lambda event : self.deleteCampagneFileXml(self.spooler_campagnes.selection_get()))
			ind = ind + 1
		
#-----------------------------------
# fin class ClssCampagneTests
#------------------------------------

#----------------------------------------
# clss gestion contructions des scenario
#----------------------------------------
class clss_construction_scenarios() :
	
	def __init__(self, parent) :
		self.parent = parent
		self.seq_compteur = 0
		self.tempo_default = 0.5
		self.cycle_default = 1
		self.comment = ""
		self.arg1 = ""
		self.arg2 = ""
		self.arg3 = ""
		self.entry_tempo 	= None
		self.entry_cycle 	= None
		self.entry_comment 	= None
		self.entry_arg1 	= None
		self.buttonBoxOpt	= None
		self.group_cmde		= None
		
		self.db_transactions = []
		self.list_transactions = []
		self.id_transaction_courant = 0
		
		# init 
		

	#---------------------------
	#- Affichage des composents
	#---------------------------
	
	def buildListTransaction(self) :
		
		##---------------------------------
		## ListSelect des transactions 
		##---------------------------------
		self.group_gestion_transactions = Pmw.Group(self.parent, tag_text='Construction Scenario')
		self.group_gestion_transactions .pack(side='left',   expand = 0, padx = 2, pady = 2)
		
		self.group_transactions_dispo = Pmw.Group(self.group_gestion_transactions.interior(), tag_text='spool Transactions dispo' )
		self.group_transactions_dispo.pack(side='left',   expand = 0, padx = 2, pady = 2)
		 
		self.liste_transactions_active = Listbox(self.group_transactions_dispo.interior(), selectmode=EXTENDED, height=5, width=30)
		self.ascenseur_active = Scrollbar(self.group_transactions_dispo.interior())
		 
		
		self.ascenseur_active.config(command = self.liste_transactions_active.yview)
		self.liste_transactions_active.config(yscrollcommand = self.ascenseur_active.set)
		self.liste_transactions_active.config(background='#AFAFAF', foreground='#11F', font = 'Calibri 10 bold')
		
		self.liste_transactions_active.grid(row=0, column=0) 
		self.ascenseur_active.grid(row=0, column=1)
		
		##-------------------------------------------------------------------------------------
		## 1- charge la liste des transactions default
		##--------------------------------------------------------------------------------------
		list_transactions_default = self.getListTransactionsScenarioFromFileXml()
		#
		for element in list_transactions_default :
			## boucle de remplissage lite
			self.liste_transactions_active.insert(END, element['NOM'])
			self.liste_transactions_active.bind('<Double-ButtonRelease-1>', lambda event : self.selectionnerTransactionDispo(self.liste_transactions_active.selection_get()))
			#self.liste_Transactions.grid(row=1, column=0)
		# parametrrer en mode select unique
		self.liste_transactions_active.config(selectmode=SINGLE, setgrid=1)
		# init la position du select 
		self.liste_transactions_active.select_set(0,0)
		self.liste_transactions_active.activate(0)
		
		##---------------------------------
		## ListSelect spool des transaction
		##---------------------------------
		
		self.group_transactions_active = Pmw.Group(self.group_gestion_transactions.interior(), tag_text='spool Transactions active' )
		self.group_transactions_active.pack(side='right',   expand = 0, padx = 2, pady = 2)
		
		
		self.liste_transactions_active = Listbox(self.group_transactions_active.interior(), selectmode=EXTENDED, height=5, width=30)
		self.ascenseur_active = Scrollbar(self.group_transactions_active.interior())
		 
		
		self.ascenseur_active.config(command = self.liste_transactions_active.yview)
		self.liste_transactions_active.config(yscrollcommand = self.ascenseur_active.set)
		self.liste_transactions_active.config(background='#AFAFAF', foreground='#11F', font = 'Calibri 10 bold')
		
		self.liste_transactions_active.grid(row=0, column=0) 
		self.ascenseur_active.grid(row=0, column=1)
		
				
		# 2- affichage image refreash
		self.img_refresh = PhotoImage(file = "images/joined_lg.gif" , height=20, width=25)
		bt_refresh = Button(self.group_gestion_transactions.interior(), text='Refresh', image=self.img_refresh, command=self.refrechListTransaction)
		bt_refresh.pack()
		
		#bt_refresh.grid(row=0, column=1)
		
		
		buttonBoxGestTransaction = Pmw.ButtonBox(self.group_gestion_transactions.interior())
		#buttonBoxGestTransaction.add('Save',  width=6, command = lambda ll=10 : saveXmlTransctionScenario(self.Listbox_transactions_active.get(0, END)))
		buttonBoxGestTransaction.add('Save',  width=6, command = self.saveScenarioToFileDataXml)  #self.saveFileDataXml
		buttonBoxGestTransaction.pack(side='bottom')


				
	#-------------------------------------------------------
	# on charge le fichier data xml des scenario
	#-------------------------------------------------------
	def getListTransactionsScenarioFromFileXml(self) :
		list_des_transactions = [] 
		fichierData = os.getcwd() + "/data/transactions_dispo.xml"
		
		if not os.path.isfile(fichierData) :
			return []
		
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_transactions = top.getElementsByTagName('TRANSACTION')
		# 
		for transaction in les_transactions :
			#
			if transaction.getElementsByTagName('NOM')[0].hasChildNodes() and transaction.getElementsByTagName('NOM')[0].firstChild != None :
			#
				options_transaction_xml = {}
				options_transaction_xml['NOM'] = transaction.getElementsByTagName('NOM')[0].firstChild.data
				list_des_transactions.append(options_transaction_xml)
					
		return 	list_des_transactions
	

	def selectionnerTransactionDispo(self, element) :
		# on recherche id contenue dans les scenario
		self.addTransactionActive(element)
		return True	

	def addTransactionActive(self,  s_nom, s_tempo=0.5, s_cycle=1, s_comment="", arg1="",arg2="",arg3="") :
		#
		self.tempo 	= s_tempo
		self.nom 	= s_nom
		self.cycle 	= s_cycle
		id_trans	= long(time.time())
		
		#on ajoute la liste
		self.id_transaction_courant += 1
		
		s_nom = str(self.id_transaction_courant) + ":" + s_nom
		#self.db_transactions.append({'id': str(self.id_transaction_courant), 'nom':s_nom, 'cycle':s_cycle, 'tempo':s_tempo, 'comment':s_comment, 'arg1':arg1 , 'arg2':arg2, 'arg3':arg3})
		self.db_transactions.insert(self.id_transaction_courant, {'id': str(self.id_transaction_courant), 'nom':s_nom, 'cycle':s_cycle, 'tempo':s_tempo, 'comment':s_comment, 'arg1':arg1 , 'arg2':arg2, 'arg3':arg3})
		 
		self.liste_transactions_active.insert(self.id_transaction_courant, s_nom )
		
		# Mettre a jour les option en double clic ou CTRL+U
		self.liste_transactions_active.bind('<Double-ButtonRelease-1>', lambda event : self.afficheOptionsTransactionActive(self.liste_transactions_active.curselection()))
		self.liste_transactions_active.bind('<Control-u>', 		lambda event : self.afficheOptionsTransactionActive(self.liste_transactions_active.curselection()))
		# Suppresseion de la ligne  en double clic ou CTRL+D
		self.liste_transactions_active.bind('<Control-d>', 		lambda event : self.delTransaction(self.liste_transactions_active.curselection()))

		return True
	
	def afficheOptionsTransactionActive(self, id_curselection) :
		#Suppression des precedent
		self.cancelOptions()
		id_element, = id_curselection
		id_element = int(id_element)
		# Suppresion des anciens
		 
		#print self.id_scenario_courant, id_element
		
		options =  self.db_transactions[id_element]
		#print self.list_transactions[ind]
		self.group_cmde = Pmw.Group(self.parent, tag_text='commande ...' )
		self.group_cmde.grid(row=2, column=0, columnspan=5)
		
		self.label_opt1 = Label(self.group_cmde.interior(),  text="tempo :") 
		self.label_opt1.grid(row=0, column=0)
		self.label_opt2 = Label(self.group_cmde.interior(),  text="cycle :") 
		self.label_opt2.grid(row=0, column=2)
		self.label_opt3 = Label(self.group_cmde.interior(),  text="comment :") 
		self.label_opt3.grid(row=0, column=4)
		
		self.entry_tempo 	= Entry(self.group_cmde.interior(), width=3, background='#ffffbf', foreground='#000040')
		self.entry_tempo.insert(0, options['tempo'])
		 
		self.entry_cycle 	= Entry(self.group_cmde.interior(), width=3, background='#ffffbf', foreground='#000040')
		self.entry_cycle.insert(0, options['cycle'])
		
		self.entry_comment 	= Entry(self.group_cmde.interior(), width=15, background='#fff', foreground='#000090')
		self.entry_comment.insert(0, options['comment'])
		
		self.entry_argument1 	= Entry(self.group_cmde.interior(), width=15, background='#fff', foreground='#000090')
		self.entry_argument1.insert(0, options['arg1'])
		
		#
		self.entry_tempo.grid(row=0, column=1)
		self.entry_cycle.grid(row=0, column=3)
		self.entry_comment.grid(row=0, column=5)
		
		self.label_opt4 = Label(self.group_cmde.interior(),  text="Arg1 :")
		self.label_opt4.grid(row=0, column=6)
		self.entry_argument1.grid(row=0, column=7)
		
		self.entry_tempo.focus()
		 
		self.buttonBoxOpt = Pmw.ButtonBox(self.group_cmde.interior())
		self.buttonBoxOpt.add('Valider',	width=10, command = lambda id=id_element : self.updateListeTransaction(id))
		self.buttonBoxOpt.add('Cancel',		width=10, command = self.cancelOptions)
		self.buttonBoxOpt.grid(row=2, 		column=0, columnspan=5)
	
	#---------------------
	# destroy options
	#---------------------
	def cancelOptions(self):
		#
		#if isinstance(entry_tempo, Entry) :
		#print "\n entree tempo avant = %s" , self.entry_tempo
		 
		if self.entry_tempo  :
			self.label_opt1.destroy()
			self.label_opt2.destroy()
			self.label_opt3.destroy()
			self.label_opt4.destroy()
			self.entry_tempo.destroy()
			self.entry_tempo = None
			
			self.entry_cycle.destroy()
			self.entry_comment.destroy()
			self.entry_argument1.destroy()
			
			self.buttonBoxOpt.destroy()
			self.group_cmde.destroy()
	#---------------------
	# update options
	#---------------------		
	def updateListeTransaction(self, id_element) :
		# sauvegarde des valeurs option 
		id_element = int(id_element) 
		
		options =  self.db_transactions[id_element]
		 
		options['tempo'] 	= self.entry_tempo.get()
		options['cycle'] 	= self.entry_cycle.get()
		options['comment'] 	= self.entry_comment.get()
		options['arg1'] 	= self.entry_argument1.get()
		
		self.liste_transactions_active.activate(id_element)
		self.db_transactions[id_element] = options
		#
		self.cancelOptions()
		#
		self.group_cmde = Pmw.Group(self.parent, tag_text='commande ...' )
		self.group_cmde.grid(row=2, column=0, columnspan=5)
		
		self.buttonBoxOpt = Pmw.ButtonBox(self.group_cmde.interior())
		self.buttonBoxOpt.add('Save',		width=10, command = self.saveScenarioToFileDataXml)
		self.buttonBoxOpt.add('Cancel',		width=10, command = self.cancelOptions)
		self.buttonBoxOpt.grid(row=2, column=0, columnspan=5)
		 
		 
		
		
	def delTransaction(self, id_curselection=None):
		#
		#print "suppression id  = %s de la selection %s" % (str(id_curselection), str(self.curselection()))
		if id_curselection :
			id_element, = id_curselection
			id_element = int(id_element)
			# print self.index(id_curselection)
			# supprimer de la liste 
			del (self.db_transactions[id_element])
			# "suppression de la selection %s" % str(self.curselection())
			self.liste_transactions_active.delete(self.liste_transactions_active.curselection())
			return True
		
		return False
	
	#-------------------------------------------------------------------
	# enregitrement data scenario transations 
	#------------------------------------------------------------------
	def saveScenarioToFileDataXml(self) :
		#print scenario_list_transactions
		self.dialog3 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
			message_text = 'Souhaiter-vous Enregistrer ce scenario ?',
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
			#-------------------------------------------------------
			# enregitrement des variable user en fichier param.xml
			#-------------------------------------------------------
		fichierData = os.getcwd() + "/data/data_scenario.xml"
	
		maintenant = datetime.now()
		date_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
		t_timestamp =  long(time.time())
		t_id = "SC_" + str(t_timestamp)
		
		if not os.path.isfile(fichierData) :
		    xfout  = open(fichierData, 'w', 'utf-8')
		    enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
		    xfout.write(enteteXML)
		    #on clos
		    xfout.close()
		    #---------------------------------
	
		 
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		
		new_scenario	= self.createElemntXml(xmldoc, 'SCENARIO')
		 
		 
		scenario_id = xmldoc.createAttribute('ID')
		scenario_id.nodeValue = str(t_id)
		new_scenario.setAttributeNode(scenario_id)
		
		scenario_created = xmldoc.createAttribute('CREATED')
		scenario_created.nodeValue = str(date_complet)
		new_scenario.setAttributeNode(scenario_created)
		
		for  options in self.db_transactions :
			#
			#print options  
			#---------------------------------
			# Creer les noeux de transactions
			#---------------------------------
			t_nom 		= options['nom'].split(':')
			nom_transaction	= t_nom[1]
			t_fonction 	= "self." + nom_transaction
			t_cycle 	= options['cycle']
			t_tempo 	= options['tempo']
			t_comment 	= options['comment']
			
			t_arg1	 	= options['arg1']
			t_arg2	 	= options['arg2']
			t_arg3	 	= options['arg3']
			
			new_transaction	= self.createElemntXml(xmldoc, 'TRANSACTION')
			# Ajout de la ligne a la racine de Transaction
			x_name			= self.createElemntXml(xmldoc, 'NOM', 	nom_transaction)
			x_function		= self.createElemntXml(xmldoc, 'FONCTION', t_fonction)
			x_tempo			= self.createElemntXml(xmldoc, 'TEMPO', 	str(t_tempo))
			
			x_cycle 		= self.createElemntXml(xmldoc, 'CYCLE', 	str(t_cycle))
			x_comment		= self.createElemntXml(xmldoc, 'COMMENT', 	t_comment)
			
			x_arg1			= self.createElemntXml(xmldoc, 'ARGUMENT1', 	t_arg1)
			x_arg2			= self.createElemntXml(xmldoc, 'ARGUMENT2', 	t_arg2)
			x_arg3			= self.createElemntXml(xmldoc, 'ARGUMENT3', 	t_arg3)
			
			
			#on ajoute option transaction
			new_transaction.appendChild(x_name)
			new_transaction.appendChild(x_function)
			new_transaction.appendChild(x_tempo)
			new_transaction.appendChild(x_cycle)
			new_transaction.appendChild(x_comment)
			
			new_transaction.appendChild(x_arg1)
			new_transaction.appendChild(x_arg2)
			new_transaction.appendChild(x_arg3)
			
			#on ajoute au  balise transaction au scenario
			new_scenario.appendChild(new_transaction)
		
		 
		root[0].appendChild(new_scenario)
		# ------------------------
		# save contenu en fichier
		# ------------------------
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		#on clos 
		afout.close()
		#
		# remettre a zero le tableau de transaction
		self.db_transactions = []
		self.liste_transactions_active.delete(0, 'end')
		self.cancelOptions()
	
	def refrechListTransaction(self) :
		# remettre a zero le tableau de transaction
		self.db_transactions = []
		self.liste_transactions_active.delete(0, 'end')
		#self.cancelOptions()
	#-----------------------------------------------
	# ajout d'une sequence dans le pooler xml
	#----------------------------------------------
	def createElemntXml(self, xmldoc, lib_balise, texte=None, attrib=None, attrib_Value=None) :
		
		# nouvelle sequence d'expression reguliere
		newXmlElem = xmldoc.createElement(lib_balise)
		if attrib :
			att 	= xmldoc.createAttribute(attrib)
			att.nodeValue = str(attrib_Value)
			newXmlElem.setAttributeNode(att)
		if texte :
			text_xml= xmldoc.createTextNode(texte)
			newXmlElem.appendChild(text_xml)
			
		return newXmlElem
	

#----------------------------------------
# clss gestion des transactions
#----------------------------------------
class clss_gestion_transactions() :
	
	def __init__(self, parent) :
		self.parent = parent
		 
		self.db_transactions = []
		self.list_transactions = []
		self.id_transaction_courant = 0
		self.liste_transactions =   None
		self.selection_transaction_courant 	=  None
		self.selection_id_courant 		=  None
		
		
		# init 
	#---------------------------
	#- Affichage des composents
	#---------------------------
	
	def start(self) :
		
		##---------------------------------
		## ListSelect des transactions 
		##---------------------------------
		self.group_gestion_transactions = Pmw.Group(self.parent, tag_text='Construction Transactions')
		self.group_gestion_transactions .pack(side='left',   expand = 0, padx = 2, pady = 2)
		
		self.group_transactions_dispo = Pmw.Group(self.group_gestion_transactions.interior(), tag_text='spool Transactions dispo' )
		self.group_transactions_dispo.pack(side='left',   expand = 0, padx = 2, pady = 2)
		 
		self.liste_transactions = Listbox(self.group_transactions_dispo.interior(), selectmode=SINGLE, height=5, width=30)
		self.ascenseur_active = Scrollbar(self.group_transactions_dispo.interior())
		 
		
		self.ascenseur_active.config(command = self.liste_transactions.yview)
		self.liste_transactions.config(yscrollcommand = self.ascenseur_active.set)
		self.liste_transactions.config(background='#AFAFAF', foreground='#11F', font = 'Calibri 10 bold')
		
		self.liste_transactions.grid(row=0, column=0) 
		self.ascenseur_active.grid(row=0, column=1)
		
		##-------------------------------------------------------------------------------------
		## 1- charge la liste des transactions default
		##--------------------------------------------------------------------------------------
		list_transactions_default = self.getListTransactionsFromFileXml()
		#
		for element in list_transactions_default :
			## boucle de remplissage lite
			self.liste_transactions.insert(END, element['NOM'])
			self.liste_transactions.bind('<Double-ButtonRelease-1>', lambda event : self.selectionnerTransactionList(self.liste_transactions.selection_get()))
			self.db_transactions.insert(self.id_transaction_courant, element['NOM'])
			#courant suivant
			self.id_transaction_courant += 1
		# parametrrer en mode select unique
		self.liste_transactions.config(selectmode=SINGLE, setgrid=1)
		# init la position du select 
		self.liste_transactions.select_set(0,0)
		self.liste_transactions.activate(0)
		
		buttonBoxGestTransaction1 = Pmw.ButtonBox(self.group_transactions_dispo.interior())
		self.add_trs1 		= buttonBoxGestTransaction1.add('New',  	width=26, command = self.addTransactionActive) #ajout transaction
		self.del_trs1 		= buttonBoxGestTransaction1.add('Supprimer', 	width=26, command = lambda a=1: self.suppressionTransaction(self.liste_transactions.selection_get()))
		buttonBoxGestTransaction1.grid(row=2, column=0)
		
		##---------------------------------
		## saisie transaction
		##---------------------------------
		self.group_transactions_active = Pmw.Group(self.group_gestion_transactions.interior(), tag_text='Transactions active' )
		
		# champd de saisie libelle 
		Label(self.group_transactions_active.interior(), text="Libelle : ").grid(row=1, column=0)
		self.new_transaction = Entry(self.group_transactions_active.interior(), width=60, background='#fff')
		
		self.new_transaction.grid(row=1, column=1)

		#boutton de sauvegarde
		buttonBoxGestTransaction2 = Pmw.ButtonBox(self.group_transactions_active.interior())
		self.update_trs2 = buttonBoxGestTransaction2.add('Save',  width=6, command = lambda a=1 : self.saveTransactionActive(self.new_transaction.get()))
		buttonBoxGestTransaction2.grid(row=2, column=0)
		#self.group_transactions_active.pack(side='right',   expand = 0, padx = 2, pady = 2)
		
		# 2- affichage image refreash
		self.img_refresh = PhotoImage(file = "images/joined_lg.gif" , height=20, width=25)
		bt_refresh = Button(self.group_transactions_active.interior(), text='Refresh', image=self.img_refresh, command=self.refrechListTransaction)
		bt_refresh.grid(row=2, column=1, columnspan=2)
		

		
	#-------------------------------------------------------
	# on charge le fichier data xml des scenario
	#-------------------------------------------------------
	def getListTransactionsFromFileXml(self) :
		list_des_transactions = [] 
		fichierData = os.getcwd() + "/data/transactions_dispo.xml"
		
		if not os.path.isfile(fichierData) :
			return []
		
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		
		les_transactions = top.getElementsByTagName('TRANSACTION')
		# 
		for transaction in les_transactions :
			#
			if transaction.getElementsByTagName('NOM')[0].hasChildNodes() and transaction.getElementsByTagName('NOM')[0].firstChild != None :
				options_transaction_xml = {}
				options_transaction_xml['NOM'] = transaction.getElementsByTagName('NOM')[0].firstChild.data
				list_des_transactions.append(options_transaction_xml)
				#print options_transaction_xml['NOM']
					
		return 	list_des_transactions
	

	def selectionnerTransactionList(self, element) :
		# on recherche id contenue dans les scenario
		# unbind les calback sur ce button
		self.selection_transaction_courant 	=  self.liste_transactions.selection_get()
		x ,		=  self.liste_transactions.curselection()
		self.selection_id_courant = int(x)
		
		self.update_trs2.unbind('<Button-1>')
		self.update_trs2.unbind('<Double-ButtonRelease-1>')
		self.update_trs2.config(command= lambda a=1 : self.saveTransactionActive(self.new_transaction.get()))
		self.update_trs2.config(text= 'modifier') # basculer le bouttton new an add
		#on met le focus
		self.new_transaction.focus_set()
		self.new_transaction.selection_range(0, Tkinter.END)

		#
		self.new_transaction.delete(0, 'end')
		self.new_transaction.insert(0, element)
		self.group_transactions_active.pack(side='right',   expand = 0, padx = 2, pady = 2)
		
		return True	

	def addTransactionActive(self) :
		#
		self.new_transaction.delete(0, 'end')
		self.update_trs2.config(text= 'add') # basculer le bouttton new an add
		self.update_trs2.config(command= lambda a=1 : self.insertTransactionActive(self.new_transaction.get()))
		self.group_transactions_active.pack(side='right',   expand = 0, padx = 2, pady = 2)
		# unbind les calback sur ce button
		
	
	def saveTransactionActive(self, new_transaction):
		#cherchon si cet element s'y touve deja dans la liste
		
		self.replaceElementListBox(self.liste_transactions, self.selection_transaction_courant, self.new_transaction.get())
		# MAJ en fichier xml
		self.updateTransactionFileDataXml(self.selection_transaction_courant , self.new_transaction.get())
		# invsble zone de saisie
		self.group_transactions_active.forget()
		
			
				
	def insertTransactionActive(self, new_transaction) :
		#------------------------------
		self.id_transaction_courant += 1
		self.db_transactions.insert(self.id_transaction_courant, {'id': str(self.id_transaction_courant), 'nom':new_transaction })
		self.liste_transactions.insert(self.id_transaction_courant, new_transaction )
		self.liste_transactions.bind('<Double-ButtonRelease-1>', lambda event : self.selectionnerTransactionList(self.liste_transactions.selection_get()))
		self.liste_transactions.bind('<Control-d>', 		lambda event : self.delTransaction(self.liste_transactions.curselection()))
		self.liste_transactions.activate(self.id_transaction_courant)
		self.liste_transactions.see(self.id_transaction_courant)
		self.new_transaction.delete(0, 'end')
		self.saveTransactionToFileDataXml(new_transaction)
		# invsble zone de saisie
		self.group_transactions_active.forget()
		
		return True
	
	
		
	
	#-------------------------------------------------------------------
	# enregitrement data scenario transations 
	#------------------------------------------------------------------
	def saveTransactionToFileDataXml(self, new_element) :
		self.dialog3 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
			message_text = 'Souhaiter-vous Enregistrer cette transaction ?',
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
			#-------------------------------------------------------
			# enregitrement des variable user en fichier param.xml
			#-------------------------------------------------------
		fichierData = os.getcwd() + "/data/transactions_dispo.xml"
	
		maintenant = datetime.now()
		date_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
		t_timestamp =  long(time.time())
		t_id = "TR_" + str(t_timestamp)
		
		if not os.path.isfile(fichierData) :
		    xfout  = open(fichierData, 'w', 'utf-8')
		    enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
		    xfout.write(enteteXML)
		    #on clos
		    xfout.close()
		    #---------------------------------
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		
		new_transaction	= self.createElemntXml(xmldoc, 'TRANSACTION')
		transaction_id = xmldoc.createAttribute('ID')
		transaction_id.nodeValue = str(t_id)
		new_transaction.setAttributeNode(transaction_id)
		
		transaction_created = xmldoc.createAttribute('CREATED')
		transaction_created.nodeValue = str(date_complet)
		new_transaction.setAttributeNode(transaction_created)

		#---------------------------------
		# Creer les noeux de transactions
		#---------------------------------
		x_nom	= self.createElemntXml(xmldoc, 'NOM')
		#on ajoute option transaction
		
		# Ajout de la ligne a la racine de Transaction
		text_xml = xmldoc.createTextNode(new_element)
		x_nom.appendChild(text_xml)
		new_transaction.appendChild(x_nom)
		
		
				
		root[0].appendChild(new_transaction)
		# ------------------------
		# save contenu en fichier
		# ------------------------
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		#on clos 
		afout.close()
		#
				
	
	def refrechListTransaction(self) :
		# remettre a zero le tableau de transaction
		#self.db_transactions = []
		self.new_transaction.delete(0, 'end')
		#self.cancelOptions()
	#-----------------------------------------------
	# ajout d'une sequence dans le pooler xml
	#----------------------------------------------
	def createElemntXml(self, xmldoc, lib_balise, texte=None, attrib=None, attrib_Value=None) :
		
		# nouvelle sequence d'expression reguliere
		newXmlElem = xmldoc.createElement(lib_balise)
		if attrib :
			att 	= xmldoc.createAttribute(attrib)
			att.nodeValue = str(attrib_Value)
			newXmlElem.setAttributeNode(att)
		if texte :
			text_xml= xmldoc.createTextNode(texte)
			newXmlElem.appendChild(text_xml)
			
		return newXmlElem
	#-----------------------------------------------
	# find Element dans la listBox
	#----------------------------------------------
	def findElementListBox(self, lbox, elem):
		for ind in range(lbox.size()) :
			if lbox.get(ind) == elem :
				print "trouver ..."
				return ind
			
		return False
				
				
	#-----------------------------------------------
	# find Element dans la listBox
	#----------------------------------------------
	def replaceElementListBox(self, lbox, elem, new):
		for i in range(lbox.size()) :
			if lbox.get(i) == elem :
				print "trouver ..."
				lbox.delete(i)
				lbox.insert(i, new)
				lbox.update()
				
	#-------------------------------------------------------------------
	# Mise a jour data transations 
	#------------------------------------------------------------------
	def updateTransactionFileDataXml(self, elem_transaction, new_value) :
		#print Transaction_list_transactions
		self.dialog3 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
			message_text = 'Souhaiter-vous Mettre a jour ce Transaction ?',
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
		#-------------------------------------------------------
		# on charge le fichier data xml en xmldoc
		#-------------------------------------------------------
		fichierData = os.getcwd() + "/data/transactions_dispo.xml"
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_transaction = top.getElementsByTagName('TRANSACTION')
		
		for transaction in les_transaction :
			#
			x_nom = transaction.getElementsByTagName('NOM')[0]
			if elem_transaction == x_nom.firstChild.data :
				x_nom.firstChild.data = new_value
				# suppression element
				"""
				transaction.removeChild(scenario)
				text_xml= xmldoc.createTextNode(new_value)
				transaction.appendChild(text_xml)
				"""
				print "transactionent trouvé %s ancien = %s" % (elem_transaction , new_value)
				# = "xxxxxxxx"
				break
		
		# ------------------------
		# save contenu en fichier
		# ------------------------
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		#on clos 
		afout.close()
		
	#-------------------------------------------------------------------
	# Suppression transations 
	#------------------------------------------------------------------
	def suppressionTransaction(self, elem_transaction) :
				
		# supprimer de la liste
		id_element = self.findElementListBox(self.liste_transactions, elem_transaction)
		del (self.db_transactions[id_element])
		# "suppression de la selection %s" % str(self.curselection())
		self.liste_transactions.delete(self.liste_transactions.curselection())
		# del elem du fichier xml 
		self.deleteTransactionFromFileDataXml(elem_transaction)  
			
			
	def deleteTransactionFromFileDataXml(self, elem_transaction) :
		#print Transaction_list_transactions
		self.dialog3 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
			message_text = 'Souhaiter-vous supprimez Transaction ?',
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
		#-------------------------------------------------------
		# on charge le fichier data xml en xmldoc
		#-------------------------------------------------------
		fichierData = os.getcwd() + "/data/transactions_dispo.xml"
		xmldoc = minidom.parse(fichierData)
		root = xmldoc.getElementsByTagName("ROOT")
		top = root[0]
		les_transaction = top.getElementsByTagName('TRANSACTION')
		
		for transaction in les_transaction :
			#
			x_nom = transaction.getElementsByTagName('NOM')[0]
			if elem_transaction == x_nom.firstChild.data :
				
				# suppression element
				
				top.removeChild(transaction)
							 
				print "transactionent supprimmer %s " % (elem_transaction )
				# = "xxxxxxxx"
				break
		
		# ------------------------
		# save contenu en fichier
		# ------------------------
		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		afout  = open(fichierData, 'w', 'utf-8')
		afout.write(contenueXml)
		#on clos 
		afout.close()
			
	#-----------------------------------------------
	# mise a jour balise xml
	#----------------------------------------------	
	def updateBaliseXml(self, xmldoc, elem, data_value) :
		#
		if( elem.hasChildNodes()) :
			elem.firstChild.data =  data_value
		else :	
			# 
			text_xml= xmldoc.createTextNode(data_value)
			elem.appendChild(text_xml)
		return elem
	
	def importXmlTransactions(self) :
		root = Tkinter.Tk()
		root.title("Import ...")
		#
		list_transactions  = getListTransactionsDefault()
		#		
		for elem in list_transactions  :
			#----------
			self.saveTransactionToFileDataXml(elem)
				
			
		
			
		return True
			
			
class listTaskBox(Listbox) :
		
	def __init__(self, parent):
		self.parent = parent
		self.db_process = []
		self.courant = 0
		#
		if not self.parent :
			self.parent = Tk();
			self.parent.option_add('*background', '#D0E3FF')
			self.parent.option_add('*foreground', "#222")
		
		self.frame_process = Tkinter.Frame(self.parent)
		self.frame_process.pack(fill=Tkinter.X, side=Tkinter.BOTTOM)
		
		#init parent
		Listbox.__init__(self, self.frame_process, selectmode=EXTENDED, height=6, width = 200)
		
	
	def afficheListBox(self) :
		#
		# entete
		info_frame = Tkinter.Frame(self.parent)
		info_frame.pack(fill=Tkinter.X, side=Tkinter.TOP)
		entete = Label(info_frame, text="- Nom DU PROCESSUS ------- PID ------- UTIL. MEMOIRE ----- ETAT ----NOM UTILISATEUR --- TEMPS PROCESSEUR ------------ TITRE ---------------------- ")
		entete.config(background='#CCCCCC', foreground='white', font = 'Calibri 10 bold', width= 200)
		entete.pack(fill=Tkinter.X, side=Tkinter.TOP)
		# group
		self.config(background='white', foreground='blue', font = 'Calibri 9')
		
		self.ascenseur1 = Scrollbar(self.frame_process)
		self.ascenseur1.config(command = self.yview)
		self.config(yscrollcommand = self.ascenseur1.set)
		self.config(background='#AFAFAF', foreground='#11F', font = 'Calibri 10 bold')
		self.ascenseur1.pack(side='right')
		self.pack(side='left')
		
	
	
	
	
	def addTask(self,  image_name=None, pid=None, session_name=None, session_number=None,
		 memory_usage=None, etat=None, username=None, tps_process=None, titre=None) :
		#
		self.image_name 	=  str(image_name)
		self.pid 		=  str(pid)
		self.session_name 	=  str(session_name)
		self.session_number 	=  str(session_number)
		self.memory_usage 	=  str(memory_usage)
		self.etat 		=  str(etat)
		self.username 		=  str(username)
		self.tps_process 	=  str(tps_process)
		self.titre 		=  str(titre)
		# ligne a plat
		ligne =  clssTask(self.image_name, self.pid, self.session_name, self.memory_usage,
				self.session_number, self.etat, self.username, self.titre)
		
		#on ajoute la listeBox
		self.insert(self.getCourant(), ligne)
		#self.bind('<Double-ButtonRelease-1>', 	lambda event : self.killProcessByPid(self.curselection()))
		self.bind('<Control-i>', 		lambda event : self.showInfoProcess(self.curselection()))
		
		#on ajoute la liste DB
		self.db_process.insert(self.getCourant(), {'KEY'	: self.getCourant(),
						    'NAME'		: self.image_name,
						    'PID'		: self.pid,
						    'USERNAME'		: self.username,
						    'TITRE'		: self.titre,
						    'SESSION_NAME'	: self.session_name,
						    'MEMORY_USAGE'	: self.memory_usage,
						    'MEMORY_NUMBER'	: self.session_number,
						    'ETAT'		: self.etat
						})
		self.suivant()
		return True
	
	##---------------------------------
	## listes des processus Susie
	##---------------------------------	
	def chargeListBoxProcess(self, application_name ) :
		#
		tab_appli = ["OMNIS7.EXE", "WINWORD.EXE", "PRORUN32.EXE"]
		tasklist = TaskList(application_name)
		#print tasklist.getListErreurs() 
		
		if len(tasklist.getListErreurs()) > 0 :
			t_erreur = tasklist.getListErreurs()
			self.addTask(t_erreur[0].encode('latin1'))
			return False
		# vide la listBOx
		
		self.delete(0, Tkinter.END)
		# charge la listBox
		for listObj in tasklist.getListProcessObject() :
			# traitement de la ligne CSV
			self.addTask(listObj.image_name, listObj.pid, listObj.session_name, listObj.memory_usage,
				listObj.session_number, listObj.etat, listObj.username, listObj.titre)
		return True
		
	#------------------------
	# suivant 
	#------------------------
	def suivant(self):
		#
		self.courant += 1
		return self.courant
	#------------------------
	# le courant  
	#------------------------
	def getCourant(self):
		return self.courant
	#------------------------
	# donne Process By Index
	#------------------------
	def getProcessByIndex(self, key):
		#
		return self.db_process[key]
	#
	#------------------------------
	# affiche Infos sur le Process
	#-----------------------------
	def showInfoProcess(self, keys):
		k_pid,  = keys
		lig_process = self.db_process[int(k_pid)]
		
		ligne = ""
		for key, elem in lig_process.items() :
			ligne += "%s %s" % (key, elem)
		return ligne
	#-----------------------------------------------------------------
	# - tuer les process par username (domain/username)
	#-----------------------------------------------------------------
	def killProcessByPid(self, index_listp=None) :
		#
		k_pid,  = index_listp
		PID = self.db_process[int(k_pid)]['PID']
		# ALLUSERSPROFILE =	 C:\Documents and Settings\All Users
		# COMPUTERNAME =	 ASADQUAOUI
		# USERDOMAIN =		 CENTRO
		# self.username = str(os.getenv("username"))
		# launchWithoutConsole("taskkill", ["/F", "/IM", "OMNIS7.exe"])
		# taskkill /F /FI   "USERNAME eq asadquaoui" /IM omnis7.exe
		
		if not PID :
			return False
		
		self.dialog4 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
			message_text = 'Souhaiter-vous arreter cette application ...?',
			buttonboxpos = 'e',
			iconpos = 'n',
			icon_bitmap = 'warning',
			buttons = ('Ok', 'Annuler', 'Close'),
			defaultbutton = 'Close');

		self.dialog4.withdraw()
		# Create some buttons to launch the dialogs.
		result = self.dialog4.activate()
		#print "resultat = %s " % resultat
		
		if (result != 'Ok') :
			return False

		commande_comp 	= "taskkill /F /PID %s " % (PID) 		
		return subprocessLaunchWithoutConsole(commande_comp )	
	
	def quit(self) :
		self.destroy()
		
_TASK_STR_TEMP_1 = \
"""Image Name: %s
PID: %d
Session Name: %s
Session #: %d
Mem Usage: %d K
Etat: %s
Username: %s
Temps process: %s
Titre: %s
"""

_TASK_STR_TEMP = """ %20s %10s %20s %10s %10s Ko %10s %20s %10s %60s """

class clssTask:
	def __init__(self, image_name=None, pid=None, session_name=None, session_number=None,
		 memory_usage=None, etat=None, username=None, tps_process=None, titre=None) :
		#
		self.image_name = image_name
		self.pid = pid
		self.session_name = session_name
		self.session_number = session_number
		self.memory_usage = memory_usage
		self.etat = etat
		self.username = username
		self.tps_process = tps_process
		self.titre = titre
		self.code_erreur = []
		self.message_erreur 	= []
		self.stdout_resultat 	= []
		self.tasklist	= []

	def __eq__(self, pid_or_image_name):
		if isinstance(pid_or_image_name, str):
		    return self.image_name == pid_or_image_name
		elif isinstance(pid_or_image_name, int):
		    return self.pid == pid_or_image_name
		elif isinstance(pid_or_image_name, Task):
		    return self == Task.pid
		else:
		    raise TypeError("must be str, int or Taks")
	
	def __str__(self):
		return _TASK_STR_TEMP % (self.image_name, self.pid, self.session_name, self.session_number,
				     self.memory_usage, self.etat, self.username, self.tps_process, self.titre)

class TaskList:
	_POPEN_ARGS = "tasklist.exe /fo CSV /nh /V"
	
	
	def __init__(self, appliname=None, username=None):
		self.commande = "tasklist.exe /fo CSV /nh /V"
		self.tasks_object = []
		
		if appliname :
			if type(appliname) is str :
				#
				self.commande = 'tasklist.exe /FI "IMAGENAME eq %s" /fo CSV /nh /V' % appliname
		if username :
			if type(username) is str :
				#
				self.commande = 'tasklist.exe /FI "USERNAME eq %s" /fo CSV /nh /V' % username
		
		if username and appliname:
			self.commande = 'tasklist.exe /FI "IMAGENAME eq %s"  /FI "USERNAME eq %s" /fo CSV /nh /V' % (appliname, username)
				
		self.tasks = []
		self.refresh()
	
	def __iter__(self):
		return iter(self.tasks)

	def refresh(self):
		#
		self.code_erreur, self.stdout_resultat, self.message_erreur  = subprocessLaunchWithoutConsole(self.commande)
		#self.message_erreur	= [elem.decode("latin1")  for elem in proc.stderr.readlines()]
		#proc.returncode, stdout , stderr.decode("latin1")
		
		#print self.stdout_resultat
		
		if len(self.message_erreur ) > 0:
			#print self.message_erreur
			return []
		
		#print self.stdout_resultat 
		self.tasklist = self.getListProcessTab()
		try :
			for ligne in self.tasklist :
				if len(ligne) > 8 :
					self.tasks.append(clssTask(ligne[0], int(ligne[1]), ligne[2], int(ligne[3]),
								int(ligne[4][:-2].replace(",","")),
								ligne[5], ligne[6], ligne[7], ligne[8] ))
					#
					self.tasks_object.append(clssTask(ligne[0], int(ligne[1]), ligne[2],
								int(ligne[3]), int(ligne[4][:-2].replace(",","")),
								ligne[5], ligne[6], ligne[7], ligne[8] ))
		except Exception, ValueError :
			#dir(ValueError)
			message =  "erreur sur ligne de self.tasklist %s" % str(ValueError)
			traceLog(message)  
			
		return True
	# --------------------
	# lister les process
	# --------------------
	def getListProcessLigne(self):
		if len(self.tasks) > 0 :
			return 	 self.tasks
		else :
			return []
	# -------------------------
	# lister les object process
	# --------------------
	def getListProcessObject(self):
		if len(self.tasks_object) > 0 :
			return self.tasks_object
		else :
			return []
	# --------------------
	# lister les process
	# --------------------
	def getListProcessTab(self):
		csvList = []
		#----------------------------
		#spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		#tasklist = reader(self.stdout_resultat, delimiter=',')
		csvList = []
		
		for tasklist in self.stdout_resultat :
			if tasklist == "\r\n" :
				continue
			
			
			tasklist = tasklist.strip("\r\n")
			tasklist = tasklist.replace("\"", '')
			tligne = tasklist.split(',')
			
			tligne	= [elem.replace('\xff', '') for elem in tligne]
			tligne 	= [elem.replace('\x90', '') for elem in tligne]
			tligne 	= [elem.replace('\x82', '') for elem in tligne]
			tligne 	= [elem.replace('\x83', '') for elem in tligne]
			tligne 	= [elem.replace('\x8a', '') for elem in tligne]
			 
			#ligne 	= [elem.encode('latin1') for elem in tligne]
			ligne 	= [elem  for elem in tligne]
			if ligne :
				csvList.append(ligne)
			#

		return csvList
		
	# --------------------		
	# lister les process
	# --------------------
	def getListErreurs(self):
		return 	self.message_erreur
	
	# lister les process 
	def getCodeErreurs(self):
		return 	self.code_erreur
	
# An example of a class that would have the strip method.  It inherits
# everything from "list", and adds a method, .strip()
# This is slower than striplist()

class StrippableList(list):
    def __init__(self,l=[]):
        list.__init__(self,l)
    def strip(self,char=None):
        return(StrippableList([x.strip(char) for x in self]))
## end of http://code.activestate.com/recipes/205377/ }}}


# A scrollBar 
#
#

class ScrooledList(Frame) :
	
	def __init__(self, options,  parent=None, label=Tkinter.Label, height=2, width=25, command=None) :
		self.label_info = label
		self.height = height
		self.width = width
		self.macommand =command
		Frame.__init__(self, parent) # attaché a une Frame
		self.pack(expand=YES)
		self.makeWidgets(options) # fabrique widget
	
	def get(self):
		index = self.listbox.curselection()
		return self.listbox.get(index)
			
	def getIndex(self):
		index,  = self.listbox.curselection()
		return index
		
	def handList(self, event):
		#
		index = self.listbox.curselection()
		elem_selectionne = self.listbox.get(index)
		self.listbox.see(index)
		self.runCommand(elem_selectionne)
		return elem_selectionne
		
	def makeWidgets(self, options) :
		self.sbar = Scrollbar(self)
		#
		self.listbox = Listbox(self, relief=SUNKEN, height= self.height, width=self.width, bg="#fff", selectbackground="#f33")
		#listb.config(height=self.height, width=self.width)
		#Associer les ascenseurs
		self.sbar.config(command=self.listbox.yview)
		self.listbox.config(yscrollcommand=self.sbar.set)
		# on affecte self.listbox
		pos = 0
		for elem in options :
			self.listbox.insert(pos, elem)
			pos += 1
			#Associer une command au Double-click 
			# bind pour event double click
			if self.macommand :
				self.listbox.bind('<Double-1>', lambda event:self.macommand(int(self.getIndex())))
			else : 
				self.listbox.bind('<Double-1>', self.handList)
				
		self.afficher()
		
	def afficher(self) :	
		self.sbar.pack(side=RIGHT, fill=Y)
		self.listbox.pack(side=LEFT, expand=NO, fill=BOTH)
	
	def runCommand(self, selection):
		#
		if isinstance(self.label_info, Label):
			print "votre selection %s" % selection
			self.label_info.config( fg='#f00', text="%s" % selection)
		else :
			print "votre selection %s" % selection
		


#================================================================
"""scrolledlist.py: A Tkinter widget combining a Listbox with Scrollbar(s).

  For details, see:
    http://www.nmt.edu/tcc/help/lang/python/examples/scrolledlist/
"""
#----------------------------------------------------------------

#================================================================
# Manifest constants
#----------------------------------------------------------------

DEFAULT_WIDTH   =  "40"
DEFAULT_HEIGHT  =  "25"

class ScrolledListPlus(Frame):
	"""A compound widget containing a listbox and up to two scrollbars.
	
	  State/invariants:
	    .listbox:      [ The Listbox widget ]
	    .vScrollbar:
	       [ if self has a vertical scrollbar ->
		   that scrollbar
		 else -> None ]
	    .hScrollbar:
	       [ if self has a vertical scrollbar ->
		   that scrollbar
		 else -> None ]
	    .callback:     [ as passed to constructor ]
	    .vscroll:      [ as passed to constructor ]
	    .hscroll:      [ as passed to constructor ]
	"""
	

	def __init__ ( self, master=None, options=None, width=DEFAULT_WIDTH,
		height=DEFAULT_HEIGHT, vscroll=1, hscroll=0, callback=None) :
		self.callback = None;
		self.vscroll =None;
		self.hscroll = None;
		self.hScrollbar = None;
		self.width =None;
		self.height = None;
		   
		#-- 1 --
		# [ if self.vscroll ->
		#     self  :=  self with a vertical Scrollbar widget added
		#     self.vScrollbar  :=  that widget ]
		#   else -> I ]
		if  self.vscroll :
		    self.vScrollbar  =  Scrollbar ( self, orient=VERTICAL )
		    self.vScrollbar.grid ( row=0, column=1, sticky=N+S )
		#-- 2 --
		# [ if self.hscroll ->
		#     self  :=  self with a horizontal Scrollbar widget added
		#     self.hScrollbar  :=  that widget
		#   else -> I ]
		if  self.hscroll:
		    self.hScrollbar  =  Scrollbar ( self, orient=HORIZONTAL )
		    self.hScrollbar.grid ( row=1, column=0, sticky=E+W )
		#-- 3 --
		# [ self  :=  self with a Listbox widget added
		#   self.listbox  :=  that widget ]
		self.listbox  =  Listbox ( self, relief=SUNKEN,
		    width=self.width, height=self.height,
		    borderwidth=2 )
		self.listbox.grid ( row=0, column=0 )
		#-- 4 --
		# [ if self.vscroll ->
		#     self.listbox  :=  self.listbox linked so that
		#         self.vScrollbar can reposition it ]
		#     self.vScrollbar  :=  self.vScrollbar linked so that
		#         self.listbox can reposition it
		#   else -> I ]
		if  self.vscroll:
		    self.listbox["yscrollcommand"]  =  self.vScrollbar.set
		    self.vScrollbar["command"]  =  self.listbox.yview
		
		#-- 5 --
		# [ if self.hscroll ->
		#     self.listbox  :=  self.listbox linked so that
		#         self.hScrollbar can reposition it ]
		#     self.hScrollbar  :=  self.hScrollbar linked so that
		#         self.listbox can reposition it
		#   else -> I ]
		if  self.hscroll:
		    self.listbox["xscrollcommand"]  =  self.hScrollbar.set
		    self.hScrollbar["command"]  =  self.listbox.xview
		#-- 6 --
		# [ self.listbox  :=  self.listbox with an event handler
		#       for button-1 clicks that causes self.callback
		#       to be called if there is one ]
		self.listbox.bind ( "<Button-1>", self.__clickHandler)
		#if option charge listbox
		# on affecte self.listbox
		self.options = options
		if self.options :
			pos = 0
			for elem in self.options :
				self.listbox.insert(pos, elem)
				pos += 1

	def __clickHandler ( self, event ):
		"""Called when the user clicks on a line in the listbox.
		"""
		#-- 1 --
		if  not self.callback:
		    return
		#-- 2 --
		# [ call self.callback(c) where c is the line index
		#   corresponding to event.y ]
		lineNo  =  self.listbox.nearest ( event.y )
		self.callback ( lineNo )
		#-- 3 --
		self.listbox.focus_set()

	def count ( self ):
		"""Return the number of lines in use in the listbox.
		"""
		return self.listbox.size()

	def __getitem__ ( self, k ):
		"""Get the (k)th line from the listbox.
		"""
		
		#-- 1 --
		if  ( 0 <= k < self.count() ):
		    return self.listbox.get ( k )
		else:
		    raise IndexError, ( "ScrolledList[%d] out of range." % k )

	def append ( self, text ):
		"""Append a line to the listbox.
		"""
		self.listbox.insert ( END, text )

	def insert ( self, linex, text ):
		"""Insert a line between two existing lines.
		"""
		
		#-- 1 --
		if  0 <= linex < self.count():
		    where  =  linex
		else:
		    where  =  END
		
		#-- 2 --
		self.listbox.insert ( where, text )

	def delete ( self, linex ):
		"""Delete a line from the listbox.
		"""
		if  0 <= linex < self.count():
		    self.listbox.delete ( linex )

	def clear ( self ):
		"""Remove all lines.
		"""
		self.listbox.delete ( 0, END )

		
		
		
class clssOptionsMedia() :
	"""
	"""
	def __init__(self, fichier_source, format_video, format_audio, codec_video,  d_width, d_height) :
		
		self.fichier_source = fichier_source
		self.format_video = format_video
		self.format_video = format_video.strip() 
		
		self.codec_video = codec_video
		self.codec_video = self.codec_video.strip()
		
		self.format_audio = format_audio
		self.format_audio = format_audio.strip() 
	
		#  definition saisi
		 
		self.d_width = d_width
		self.d_height =  d_height
		
		
	def getCommande(self) :
		#
		base_name 	= os.path.basename(self.fichier_source)
		rep_source 	= os.path.dirname(self.fichier_source)
		nom_video  	= os.path.splitext(base_name)[0]
		#
		fic_out = self.formate_nomfichier(base_name)
		
		
		if mswindows :
			cc = Converter("c:/bin/ffmpeg.exe", "c:/bin/ffprobe.exe")
		else :
			cc = Converter("/usr/bin/ffmpeg", "/usr/bin/ffprobe")
		#--------------------
		options = cc.getOptions(self.fichier_source , fic_out , {
			'format': self.format_video,
			'audio': {
			    'codec': 	self.format_audio,
			    'samplerate': 11025,
			    'channels': 2
			},
			'video': {
			    'codec'	: self.codec_video,
			    'width'	: self.r_width,
			    'height'	: self.r_height,
			    'fps'	: 15,
			    'mode' 	: '16:9',
			}})
		
		cmdes = cc.ffmpeg.getCommande(self.fichier_source , fic_out , options)
		print options
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
		print commande
		
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
		definition_video = self.definitionSauve.get()
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
			    'width'	: r_width,
			    'height'	: r_height,
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