# -*- coding: iso8859_1 -*-
# module local
from clss_helpers import *
from commun_helpers import *
import re
#import _winreg

class ClssConvertor() :
	"""
	Convertor Convertor
	"""
	
	def __init__(self) :
		self.debug	= True
		self.fs_trace 	= None
		self.connection = None
		self.tabErreur 	= []
		self.var_environnement  = {}
		self.tab_entry 	= {}
		self.tabDico 	= {}
		self.resume 	= {}
		self.stop 	= False
		self.ROOT 	= ""
		self.erreurs 	= []
		self.info_db 	= {}
		self.username = str(os.getenv("USERNAME"))
		self.var_environnement['TRACE'] = "trace.log"

		
		
		self.getParametresDefault()


	def chargeEnvironnement(self) :
		#------------------------------------------------------------------------------------------------------------------
		# 1- charge les variables environnement si il nexiste pas on charge le default "param_default.xml"
		# si param.xml et  "param_default.xml" ne sont pas presents lors de la 1er install  :
		# * on recupere la precedente config installée sur poste via (itcole, susiv4.log , env ...) sinon on charge une par default
		#--------------------------------------------------------------------------------------------------------------------------
		filename = os.getcwd() + "/config/param.xml"
		self.username = str(os.getenv("USERNAME"))
		# 1.1 si param.xml n'exite pas 
		if( not os.path.isfile(filename) or os.path.getsize(filename) == 0):
			self.saveParametresNewUsers("default")
			self.chargeFichierXmlParam("default") # charge le parametrage utilisateur enregistré
		# 1.2 param.xml exist et enreg username n'existe pas 
		elif not searchConfigUserFromFileXml(self.username):
			# si malgré tout il n ya pas de param default on le creer
			if not searchConfigUserFromFileXml("default"):
				self.saveParametresNewUsers("default")
			# sinon on le charge
			self.chargeFichierXmlParam("default")
		# 1.3 param.xml exist et enreg username n'existe pas 
		else :
			self.chargeFichierXmlParam(self.username)
		#
		return True
		
	
	#----------------------------
	# tracage des message erreur
	#----------------------------
	def traceAppli(self, msg='') :
		#----------------------------
		# fichier de trace appli log
		#----------------------------
		if (self.debug == True) :
			try :
				filename = "trace.log"
				self.fs_trace = open(filename, 'a', encoding='latin1') ## Ouvrir fichier liste
				
			except ValueError: 
				## Message Alert 
				tkMessageBox.showerror("Erreur ", u'impossible de creer le fichier trace.log')

			mess_trace = msg
			
			#
			self.fs_trace.write(mess_trace + '\n')
			self.fs_trace.close()
			return True
		
		return False
	
	#----------------------------------------------------------
	# sauvegarde de la config pour un nouveau utilisateur
	#----------------------------------------------------------
	def saveParametresNewUsers(self, x_username=None) :
		#
		maintenant = datetime.now()
		date_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
		t_timestamp =  long(time.time())
		t_id = "PM_" + str(t_timestamp)
		
		#----------------------------------------------------------------------------
		# 2- creer l'entete si le fchier n'existe pas sinon on recharge fichierData
		#---------------------------------------------------------------------------		
		fichierData = os.getcwd() + "/config/param.xml"
		if not os.path.isfile(fichierData) :
			#--------------------------------------------------------------------
			# si le fichier param n'existe pas je le creer avec une entete xml 
			#-----------------------------------------------------------------
			xfout  = open(fichierData, 'w', 'utf-8')
			enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
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

		#----------------------------------------------------------------------------
		# 4- charge les Parametres par Default
		#---------------------------------------------------------------------------	
		vars_susie_default =  self.getParametresDefault()
		
		# sauvegarde xml des parametre default
		#self.saveParametresDefault(vars_susie_default)
			
			#
		for elem in self.var_environnement_default.keys() :
			## ajout d'une sequence a la racine
			ind = ind + 1
			valeur_input = self.var_environnement_default[elem] 
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
		#self.chargeFichierXmlParam()
		
		return True
	
	#-------------------------------------------------------------------
	# si on trouve rien on charge une config par par default standard
	#-----------------------------------------------------------------
	def getParametresDefault(self) :
		 # si on trouve rien on charge une config par par default standard
		self.traceAppli(r"Erreur %s : on ne trouve pas d'ancienne installation dans l'environnement on charge config par default  ! " %   getDateNow())
		
		self.var_environnement_default  = {
				'HOMEAPP' 	: 	os.path.dirname(os.path.abspath(__file__)),
				'DIRDEST'	: 	os.path.dirname(os.path.abspath(__file__))  + "/out",
				'DIRSRC'	: 	os.path.dirname(os.path.abspath(__file__)),
				'TRACE'		: 	os.path.dirname(os.path.abspath(__file__)) + "/out",
					
		}
		
		#************************************
		# a partir de l'environnment 
		self.var_environnement_default["PATH"] 			= str(os.getenv('PATH'))
		self.var_environnement_default["USERNAME"] 		= str(os.getenv("USERNAME"))
		
		# retour 
		return self.var_environnement_default

	#---------------------------------------
	# sauvegarde de la config default 
	#---------------------------------------
	def saveParametresDefault(self, var_environnement_default) :
		#---------------------------------------------------------------------------------------------------
		# enregitrement des variable defaut de l'install standard dans un fichier config/param_default.xml
		#---------------------------------------------------------------------------------------------------
		fout  = open(os.getcwd() + "/config/param_default.xml", 'w') ## Ouvrir fichier liste 
		tabTotal = []
		# transformation en XML
		enteteXML = "<?xml version='1.0' encoding='ISO-8859-1'?><ROOT></ROOT>"
		xml_impl = minidom.getDOMImplementation();
		xmldoc = xml_impl.createDocument("<?xml version='1.0' encoding='ISO-8859-1'?>", 'ROOT', None);
		root = xmldoc.getElementsByTagName("ROOT")
		top_elem = xmldoc.documentElement
		ind = 0		 
		## ajout d'une ligne xml
		#if not( self.tab_entry.has_key(cle)) :
		cles = self.tab_entry.keys()
		ligne = ""

		
		for elem in var_environnement_default.keys() :
			## ajout d'une sequence a la racine
			ind = ind + 1
			valeur_input = var_environnement_default[elem] 
			#Replace les slash en fin de chaine
			valeur_input = valeur_input.rstrip('/')
			valeur_input = valeur_input.rstrip('\\')
			
			#self.tab_entry['HOME0'].delete(0,"end")
			#self.tab_entry['HOME0'].insert(0, home_0)
			
			# remplacer les \ par "/"
			valeur_input = valeur_input.replace('\\', '/')
			ligne = createElemntXml(xmldoc, elem, valeur_input)
			# Ajout de la ligne a la racine
			root[0].appendChild(ligne)

		contenueXml = xmldoc.toxml()
		# save contenu en fichier
		fout.write(contenueXml)
		## fermeture des flux fichiers
		fout.close()
		 
		return True
	
	def chargeFichierXmlParam(self, username=None):
		#
		"""
		1 == ELEMENT_NODE, 2 == ATTRIBUTE_NODE, 3 == TEXT_NODE, 4 == CDATA_SECTION_NODE, 5 == ENTITY_NODE, 6 == PROCESSING_INSTRUCTION_NODE, 7 == COMMENT_NOD
		"""
		# on recupere username
		if not username  : # 
			username = str(self.username)

		
		# on recupere fichier param
		filename = os.getcwd() + "/config/param.xml"
		if( not os.path.isfile(filename) or os.path.getsize(filename) == 0) :
			messages = "Erreur : Attention le fichier de parametrage est innexistant ou vide, recharger le !! " + filename
			tkMessageBox.showerror(messages)
			self.traceAppli(messages)
			return False
		
		

		# en recupere l'enreg xml du user
		user_courant = searchConfigUserFromFileXml(username) 
		if user_courant :
			ligne = user_courant.firstChild # ok si on trouve on recupere l'entete user
			
		else :
			#on charge user default
			user_courant = searchConfigUserFromFileXml("default")
			if not user_courant :
				messages = "Erreur : aucun parametrage par defaut trouvé  !! "  
				tkMessageBox.showerror(messages)
				self.traceAppli(messages)
				return False
			
		
		ligne = user_courant.firstChild # ok si on trouve on recupere l'entete user
		#ligne = top_ligne
		#
		
		
		ligneXml_dico = {}
		# ligne.firstChild.nodeType == 3 === type text
		# ligne.firstChild.nodeType == 1 === type Noeux
		while (ligne and ligne.nodeType == 1) :
			#-------------------------------------------------------
			#on charge la donnée de la balise correspondant au noeux
			#-------------------------------------------------------
			if(ligne.hasChildNodes() and ligne.firstChild.nodeType == 3) :
				#print "\n nom name = %s \t type du fils = %s" % (ligne.nodeName, ligne.firstChild.nodeType)
				valeur_key_env = ligne.firstChild.data;
				key_var_env = ligne.nodeName
				self.var_environnement[key_var_env] = valeur_key_env
				#print "*************  key = %s" % valeur_key_env
			
			if ligne.nodeName == 'CONNEXION' :
				noeuds = ligne
				x = noeuds.firstChild;
				self.var_environnement['CONNEXION'] = {'TNSNAME':'', 'PORT':'', 'SID':'', 'HOST':''}
				while (x and x.nodeType == 1 and x.hasChildNodes()) :
					#
					self.var_environnement['CONNEXION'][x.nodeName] = x.firstChild.data
					#print "\n nom name = %s \t type du fils = %s" % (x.nodeName, x.firstChild.nodeType)
					x=x.nextSibling;
						 
				
				
			## ligne Suivant
			# suivant 
			ligne = ligne.nextSibling

		return self.var_environnement
	
	#-----------------------------
	# controle parametres
	#-----------------------------		
	def controleParametres(self) :
		# ---------------------
		msg = ""
		
		self.erreurs = []
		
		# test l'existance des chemin et localisation defini :
		cle_localisaton = [ 'DIRDEST', 'HOMEAPP', 'DIRSRC', 'TRACE'  ]
		# j'exclus 'R2IVPANTHER' du controle pas blocant si pas d'install logidial 
		
		for  cle in cle_localisaton :
			#
			localisation = str(self.var_environnement[cle])
			
			if not os.path.isdir(localisation) :
				msg = r"Ce répertoire '%s' indiqué dans le paramétrage cle=%s n'existe pas !" % (localisation, cle)
				self.erreurs.append(msg)
			
		messages = "Erreur :"
		if len(self.erreurs) > 0:
			for ligne in self.erreurs :
				messages += ligne 
			messages="Erreur %s : %s " %(getDateNow(), messages)
			tkMessageBox.showerror(messages)
			self.traceAppli(messages)
			return False
		else :
			##Pmw.MessageDialog(None, title='paramètrage',  message_text= "Controle Ok ")
			return True
		
		return True
	