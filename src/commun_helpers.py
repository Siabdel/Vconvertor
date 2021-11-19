# -*- coding: utf-8 -*-
import Pmw
from Tkinter import *
import Tkinter
import tkMessageBox
import threading
from tkFileDialog import *
import time
from time import (strftime, mktime)
import shutil, errno
from math import fmod, fabs
import os, sys, stat
from xml.dom import minidom
import xml.parsers.expat
import shutil
from datetime import datetime
from codecs import open
import subprocess
from string import *
import re
import pdb
import time


sys.path.append("C:\Python26\Lib")
sys.path.append("C:\Python26\Lib\site-packages")
sys.path.append("C:\Python26\Lib\site-packages\Lib")
sys.path.append("C:\Python26\Lib\site-packages\win32\lib")
#import pywintypes
#import win32com
#import win32com.client
from subprocess import PIPE, Popen, CalledProcessError

def supercopy(src, dst):
	try:
		shutil.copytree(src, dst)
		
	except OSError as exc : # python >2.5
		#Pmw.MessageDialog(None, title='Message', message_text="Erreur system %s lors de la supercopy src=%s dest= %s " % (str(exc.errno), src, dst))
		tkMessageBox.showerror("Erreur ", u"Erreur system %s lors de la supercopy src=%s dest= %s " % (str(exc.errno), src, dst))
		if exc.errno == errno.ENOTDIR:
			shutil.copy(src, dst)
	else:
		pass;

def arrondi(mon_float, nb_apres_virgule):
    """
    arrondi des flottant
    """
    multiplicateur = power(10,nb_apres_virgule)
    nombre = mon_float*multiplicateur
    return nombre/mulitplicateur

#---------------------------------
# charger les transactions XML
#---------------------------------	
def chargeScenariosXml(s_default=False) :
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
				options_transaction_xml['TEMPO'] 	= transaction.getElementsByTagName('TEMPO')[0].firstChild.data
				options_transaction_xml['CYCLE'] 	= transaction.getElementsByTagName('CYCLE')[0].firstChild.data
				
				if( transaction.getElementsByTagName('ARGUMENT1') and transaction.getElementsByTagName('ARGUMENT1')[0].hasChildNodes()) : 
					options_transaction_xml['ARGUMENT1'] 	= transaction.getElementsByTagName('ARGUMENT1')[0].firstChild.data
								
				if( tac.getElementsByTagName('COMMENT')[0].hasChildNodes()) : 
					options_transaction_xml['COMMENT'] = tac.getElementsByTagName('COMMENT')[0].firstChild.data
				else :
					options_transaction_xml['COMMENT'] = ""
				
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

def getTransactionsScenario(scenario_id):
	##(scenario_id.value, created.value) : spool_transactions_xml}
	##
	tab_transactions = chargeScenariosXml()
	#print id, data[0]['NAME']
	list_trans = []
	for elem in tab_transactions  :
		for id, data in  elem.items() :
			if id == scenario_id :
				for transaction in data :
					list_trans.append(transaction['NOM'])
				break;
			
	return list_trans


def getListScenarios():
	##(scenario_id.value, created.value) : spool_transactions_xml}
	##
	tab_transactions = chargeScenariosXml()
	#print id, data[0]['NAME']
	list_scenario = []
	for elem in tab_transactions  :
		for id_scenario, data in  elem.items() :
			list_scenario.append(id_scenario)
			
			
	return list_scenario


def getDataScenario(scenario_id):
	##(scenario_id.value, created.value) : spool_transactions_xml}
	##
	tab_transactions = chargeScenariosXml()
	for elem in tab_transactions  :
		for id, data in  elem.items() :
			if id == scenario_id :
				return data
				#print id, data[0]['NAME']

# (IMHO) the simplest approach:
def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

# an alternative implementation, which
# happens to run a bit faster for large
# dictionaries on my machine:
def sortedDictValues2(adict):
    keys = adict.keys()
    keys.sort()
    return [dict[key] for key in keys]

# a further slight speed-up on my box
# is to map a bound-method:
def sortedDictValues3(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)

def dictSort(d):
    """ returns a dictionary sorted by keys """
    our_list = d.items()
    our_list.sort()
    k = {}
    for item in our_list:
        k[item[0]] = item[1]
    return k

def sort_dict(dictionary, field): 
	tmp_list = [] 
	for key, value in dictionary.items(): 
		tmp_list.append([key, value]) 
		tmp_list.sort(key=lambda x:x[field]) 
	return tmp_list

def mod_dix_old(k, modulo=10):
	mm = fmod(k, modulo)
	x = (k-mm) + mm / modulo
	return x

def mod_dix(k, modulo=10):
	l_abs = long(k)
	l_abs = l_abs / modulo + modulo
	mm = fmod(k, l_abs)
	x = l_abs + mm / modulo
	return x

def tab_modulo_dix(mtab, modulo=10) :
    #
    return  [mod_dix(key, modulo) for key in mtab]
    
def getDataScenarioDefault():
	##(scenario_id.value, created.value) : spool_transactions_xml}
	##
	tab_transactions = chargeScenariosXml(True)
	for elem in tab_transactions  :
		for id, data in  elem.items() :
			return data
			#print id, data[0]['NAME']


def getListScenariosDefault():
	##(scenario_id.value, created.value) : spool_transactions_xml}
	##
	tab_transactions = chargeScenariosXml(True)
	#print id, data[0]['NAME']
	list_scenario = []
	for elem in tab_transactions  :
		for id_scenario, data in  elem.items() :
			list_scenario.append(id_scenario)
			
			
	return list_scenario

def getListScenarios():
	##(scenario_id.value, created.value) : spool_transactions_xml}
	##
	tab_transactions = chargeScenariosXml()
	#print id, data[0]['NAME']
	list_scenario = []
	for elem in tab_transactions  :
		for id_scenario, data in  elem.items() :
			list_scenario.append(id_scenario)
			
			
	return list_scenario

def getListTransactionsDefault():
	##(scenario_id.value, created.value) : spool_transactions_xml}
	##
	tab_transactions = chargeScenariosXml(True)
	
	list_trans = []
	for elem in tab_transactions  :
		for id, data in  elem.items() :
			for transaction in data :
				list_trans.append(transaction['NOM'])
			
			
	return list_trans
				
#-------------------------------------------------------------------
# enregitrement data scenario transations 
#------------------------------------------------------------------
def saveXmlTransctionScenario(scenario_list_transactions = []) :
	#print scenario_list_transactions
	fichierData = os.getcwd() + "/out/transactions_performance.xml"

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
	
	new_scenario	= createElemntXml(xmldoc, 'SCENARIO')
	 
	 
	scenario_id = xmldoc.createAttribute('ID')
	scenario_id.nodeValue = str(t_id)
	new_scenario.setAttributeNode(scenario_id)
	
	scenario_created = xmldoc.createAttribute('CREATED')
	scenario_created.nodeValue = str(date_complet)
	new_scenario.setAttributeNode(scenario_created)
	
	 
	for transaction in scenario_list_transactions :
		 
		for item, options in transaction.items() :
			#---------------------------------
			# Creer les noeux de transactions
			#---------------------------------
			t_function 	= options['fonction']
			t_cycle 	= options['cycle']
			t_tempo 	= options['tempo']
			t_comment 	= options['comment']
		
		new_transaction	= createElemntXml(xmldoc, 'TRANSACTION')
		# Ajout de la ligne a la racine de Transaction
		x_name			= createElemntXml(xmldoc, 'NOM', 	item)
		x_tempo			= createElemntXml(xmldoc, 'TEMPO', 	str(t_tempo))
		x_function		= createElemntXml(xmldoc, 'FONCTION', t_function)
		x_cycle 		= createElemntXml(xmldoc, 'CYCLE', 	str(t_cycle))
		x_comment		= createElemntXml(xmldoc, 'COMMENT', 	t_comment)
		#on ajoute option transaction
		new_transaction.appendChild(x_name)
		new_transaction.appendChild(x_function)
		new_transaction.appendChild(x_tempo)
		new_transaction.appendChild(x_cycle)
		new_transaction.appendChild(x_comment)
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
	 

	
#-------------------------------------------------------------------
# enregitrement data times des acces chronos patient en fichier
#------------------------------------------------------------------
def saveXmlOneDeltaTime(action='INCONNU',  delta='0.0', message_erreur='', seule_chrono = None) :

	if seule_chrono :
		fichierData = os.getcwd() + "/out/delta_tchrono.xml"
	else :
		fichierData = os.getcwd() + "/out/delta_mesure_performance.xml"

	maintenant = datetime.now()
	maint_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
	hdate = str(maintenant.strftime("%H.%M%S"))
	t_timestamp =  time.time()
	
	if not os.path.isfile(fichierData) :
	    xfout  = open(fichierData, 'w', 'utf-8')
	    enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
	    xfout.write(enteteXML)
	    #on clos
	    xfout.close()
	    #---------------------------------

	#---------------------------------
	xmldoc = minidom.parse(fichierData)
	root = xmldoc.getElementsByTagName("ROOT")
	
	#---------------------------------
	# Creer les noeux de transactions
	#---------------------------------
	new_transactions= createElemntXml(xmldoc, 'TRANSACTIONS')
	 
	ligne = str(hdate) + "\t" + str(delta) + "\n"
	fdix_delta = mod_dix(float(delta))
	x_action	= createElemntXml(xmldoc, action)
	
	# Ajout de la ligne a la racine
	x_action	= createElemntXml(xmldoc, 'ACTION', 	action)
	x_timestramp	= createElemntXml(xmldoc, 'T_TIMESTAMP', 	str(t_timestamp))
	x_delta		= createElemntXml(xmldoc, 'T_DELTA', 		str(delta))
	x_adate		= createElemntXml(xmldoc, 'T_DATE', 		str(maint_complet))
	x_heure		= createElemntXml(xmldoc, 'T_HEURE', 		str(hdate))
	 
	message 	= createElemntXml(xmldoc, 'MESSAGE', 		str(message_erreur))
	
	#on ajoute au  balise transaction
	new_transactions.appendChild(x_action)
	new_transactions.appendChild(x_adate)
	new_transactions.appendChild(x_delta)
	new_transactions.appendChild(x_heure)
	new_transactions.appendChild(x_timestramp)
	new_transactions.appendChild(message)
	 
	root[0].appendChild(new_transactions)
	#print "saveXmlOneDeltaTime ... , plantage %s \n" % message_erreur
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
# enregitrement en fichier xml des transactions 
#------------------------------------------------------------------
def saveFileXmlCampagne(campagne_transactions = {}, id_scenario=0, nb_cycle=1, version_word='Word2003') :
	if len(campagne_transactions) == 0 :
		return False
	
	fichierData = os.getcwd() + "/data/data_campagne.xml"
	maintenant = datetime.now()
	maint_complet = str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
	hdate = str(maintenant.strftime("%H.%M%S"))
	t_timestamp =  long(time.time())
	t_timestamp =  str(t_timestamp) 
	
	if not os.path.isfile(fichierData) :
	    xfout  = open(fichierData, 'w', 'utf-8')
	    enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
	    xfout.write(enteteXML)
	    #on clos
	    xfout.close()
	
	#---------------------------------
	xmldoc = minidom.parse(fichierData)
	root = xmldoc.getElementsByTagName("ROOT")
	
	#---------------------------------
	# Creer les noeux de transactions
	#---------------------------------
	new_campagne = createElemntXml(xmldoc, 'CAMPAGNE')
	id 		= xmldoc.createAttribute("ID")
	date_created 	= xmldoc.createAttribute("CREATED")
	scenario_id 	= xmldoc.createAttribute("SCENARIO_ID")
	x_nb_cycle 	= xmldoc.createAttribute("NB_CYCLE")
	x_version_word 	= xmldoc.createAttribute("VERSION_WORD")
	
	
	
	id.nodeValue 		= t_timestamp
	date_created.nodeValue 	= maint_complet
	scenario_id.nodeValue 	= str(id_scenario)
	x_nb_cycle.nodeValue 	= str(nb_cycle)
	x_version_word.nodeValue = version_word
	
	new_campagne.setAttributeNode(id)
	new_campagne.setAttributeNode(date_created)
	new_campagne.setAttributeNode(scenario_id)
	new_campagne.setAttributeNode(x_nb_cycle)
	new_campagne.setAttributeNode(x_version_word)
	
	
	for transaction in campagne_transactions  :
		#
		ligne = transaction['TRANSACTIONS']
		new_transactions= createElemntXml(xmldoc, 'TRANSACTIONS')

		for key, val_elem in ligne.items():
			# Ajout de la ligne a la racine
			x_action = createElemntXml(xmldoc, key,	str(val_elem))
			new_transactions.appendChild(x_action)
		# ajout de la transaction a la campagne 
		new_campagne.appendChild(new_transactions)
	
	root[0].appendChild(new_campagne)
		
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
# remise a zero du fichier delta_tchrono.xml
#------------------------------------------------------------------
def resetFileXmlDeltaTimes(xml_total = False) :
	
	
	tab_fichierData = ["/out/delta_tchrono.xml", "/out/delta_mesure_performance.xml"]
	
	if xml_total == False :
		fichierData =  os.getcwd() + "/out/delta_tchrono.xml"
		if os.path.isfile(fichierData) :
			xfout  = open(fichierData, 'w', 'utf-8')
			enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
			xfout.write(enteteXML)
			#on clos
			xfout.close()
			
	else :
		
		for fichierData in tab_fichierData :
			fichier = os.getcwd() + fichierData
			if os.path.isfile(fichier) :
				xfout  = open(fichier, 'w', 'utf-8')
				enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
				xfout.write(enteteXML)
				#on clos
				xfout.close()
		
#-------------------------------------------------------------------
# enregitrement des data times des acces chronos patient en fichier
#------------------------------------------------------------------
def saveXmlDeltaTimes(dataDeltaTime) :

	fichierData = os.getcwd() + "/out/delta_tchrono.xml"
	
	
	if not os.path.isfile(fichierData) :
		xfout  = open(fichierData, 'w', 'utf-8')
		enteteXML = """<?xml version="1.0" encoding="ISO-8859-1"?><ROOT></ROOT>"""
		xfout.write(enteteXML)
		#on clos
		xfout.close()
	#---------------------------------
	#---------------------------------
	xmldoc = minidom.parse(fichierData)
	root = xmldoc.getElementsByTagName("ROOT")
	
	#---------------------------------
	# Creer les noeux de transactions
	#---------------------------------
	new_transactions= createElemntXml(xmldoc, 'TRANSACTIONS')
	if len (dataDeltaTime) == 0 :
		return False
	
	for  adate, delta in dataDeltaTime :
		ligne = str(adate) + "\t" + str(delta) + "\n"
		fdix_delta = mod_dix(float(delta))
		action	= createElemntXml(xmldoc, 'MODIFICATION_CHRONO')
		
		# Ajout de la ligne a la racine
		x_adate	= createElemntXml(xmldoc, 'T_DATE', str(adate))
		action.appendChild(x_adate)
		x_delta	= createElemntXml(xmldoc, 'T_DELTA', str(delta))
		action.appendChild(x_delta)	
		new_transactions.appendChild(action)			
		root[0].appendChild(new_transactions)
	
	# ------------------------
	# save contenu en fichier
	# ------------------------
	contenueXml = xmldoc.toxml()
	# save contenu en fichier
	
	afout  = open(fichierData, 'w', 'utf-8')
	afout.write(contenueXml)
	#on clos 
	afout.close()



#---------------------------------
# charger les transactions XML
#---------------------------------	
def chargeTransactionsXmlCampagne(total=None) :
	"""
	"""
	dico_taches_xml = {}
	spool_transactions_xml = []
	if total :
		fichierData = os.getcwd() + "/data/data_campagne.xml"
	else :
		fichierData = os.getcwd() + "/data/delta_tchrono.xml"
	
	xmldoc = minidom.parse(fichierData)
	root = xmldoc.getElementsByTagName("CAMPAGNE")
	
	top = root[0]
	tac = top.firstChild
	
	if (top.firstChild == top.lastChild) : 
		return []
	#last = self.getLastchild(top)		

	if(tac == None) : 
		return []

	while (tac and tac.nodeType == 1) :

		# init 
		dico_taches_xml = {}
	
		if(tac.hasChildNodes()) : 
			t_action =  tac.getElementsByTagName('ACTION')[0].firstChild.data
			dico_taches_xml["ACTION"] = t_action
	
			t_delta	= tac.getElementsByTagName('T_DELTA')[0].firstChild.data
			dico_taches_xml['T_DELTA'] = t_delta
			
			t_timestamp = tac.getElementsByTagName('T_TIMESTAMP')[0].firstChild.data
			dico_taches_xml['T_TIMESTAMP'] = t_timestamp
			
			t_heure	= tac.getElementsByTagName('T_HEURE')[0].firstChild.data
			dico_taches_xml['T_HEURE'] = t_heure
	
			d_source = tac.getElementsByTagName('T_DATE')[0].firstChild.data
			dico_taches_xml['T_DATE'] = d_source
			
			if( tac.getElementsByTagName('MESSAGE')[0].hasChildNodes()) : 
			    message =  tac.getElementsByTagName('MESSAGE')[0].firstChild.data
			    dico_taches_xml['MESSAGE'] = message
	
		## la liste des tache 
	
		# ajout 
		spool_transactions_xml.append(dico_taches_xml)
		# 
		if (tac == top.lastChild) :
			break;
		# suivant 
		tac = tac.nextSibling;
		#print spool_transactions_xml
		#print "\n tache  = %-20s source = %20s" % (titre, source) 

	## fermeture des flux fichiers
	return spool_transactions_xml
#-----------------------------------------------
# ajout d'une sequence dans le pooler xml
#----------------------------------------------
def createElemntXml( xmldoc, lib_balise, texte=None, attrib=None, attrib_Value=None) :
	
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
def getDeltaTimestamp(t1):
    #
    t2 = time.time()
    return  t2 - t1

def getListIdCampagnes() :
	"""
	"""
	options_transaction_xml = {}
	list_Campagne_xml = []
	  
	fichierData = os.getcwd() + "/data/data_campagne.xml"
	if not os.path.isfile(fichierData) :
		return False
	
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
			options = dict(
				campagne_id 	= cap.attributes['ID'].value,
				created 	= cap.attributes['CREATED'].value,
				scenario_id 	= cap.attributes['SCENARIO_ID'].value
			)
			
			# add
			list_Campagne_xml.append(options)
			#suivant 
			cap = cap.nextSibling
	
	#print list_Campagne_xml
	return list_Campagne_xml	
##------------------------------
#--- fonction ouverture fichier
##------------------------------
def ouvrirFichierData(self, options = {}) :
	# MessageBeep(1)
	nomFic = self.askopenfile()
	if nomFic :
		self.entFicData.delete(0, "end")
		self.entFicData.insert(0, nomFic.name)

		return nomFic
	else :
		return None	

def askopenfile(self):
	"""Returns an opened file in read mode."""

	#return tkFileDialog.askopenfile(mode='r', **self.options)
	return askopenfile(mode='r', **self.options)

##------------------------------
#--- fonction ouverture fichier
##------------------------------
def ouvrirFichierStandard(self, entFichier) :

	nomFic =  askopenfile()
	if nomFic :
		entFichier.delete(0, "end")
		entFichier.insert(0, nomFic.name)

		return nomFic
	else : return None
	
	
	
	
def formatLigneHtml(self, lib, data) :
	#
	##  ----
	resume = "<div class='myForm'> \n";
	resume += " \n<dl><dt>" +  lib + "</dt><dd class>" + str(data) + "</dd> </dl>" 
	resume += "</div> \n";


	return  resume

#---------------------------
#- ecrtiture helper ligne
#---------------------------
def formatLigneHtml2(self, lib, data) :
	#
	##  ----
	resume = "<tbody> \n";
	resume += " \n<tr><dd>" +  lib + "</dd><dd>" + str(data) + "</dd></tr>" 
	resume += "</tbody> \n";
	return  resume
#---------------------------
#- ecrtiture de bas HTML
#---------------------------
def ecrireEndHtml(self, fdout) :

	endHTML = "</body></html>\n";
	fdout.write(endHTML);
	return True


def chmod_rep(self): 
		import os, stat
		
		os.chmod(ur"file_path_name", stat.S_IWRITE)
		for root, dirs, files in os.walk(ur'root_dir'):
			for fname in files:
				full_path = os.path.join(root, fname)
				os.chmod(full_path ,stat.S_IWRITE)
		# ou
		if os.path.exists(target) :
			subprocess.check_call(('attrib -R ' + target + '\\* /S').split())
			shutil.rmtree(target)


def update(self, event, cle):
	#
	rubrique_jumeaux_1 = ['R2IVSV4','R2IVLOGIDIAL','R2INORMALDOT']
	rubrique_jumeaux_2 = ['R2IVWORD','R2IVNORMALDOT']

	success=True
	try:
	    x_saisi = str(self.tab_entry[cle].get())

	except ValueError: success=False
	if success:
		if cle == 'HOMEAPP' :
			for elem in rubrique_jumeaux_1:
				self.tab_entry[elem].config(state = "normal")
				self.tab_entry[elem].delete(0,"end")
				self.tab_entry[elem].insert(0, "%s" % x_saisi)
				self.tab_entry[elem].config(state = "readonly")

		if cle == 'HOMETTX':
			for elem in rubrique_jumeaux_2 :
				self.tab_entry[elem].config(state = "normal")
				self.tab_entry[elem].delete(0,"end")
				self.tab_entry[elem].insert(0, "%s" % x_saisi)
				self.tab_entry[elem].config(state = "readonly")
def every_x_secs(x):
		"""
		Returns a function that will generate a datetime object that is x seconds
		in the future from a given argument.
		"""
		return lambda last: last + datetime.timedelta(seconds=x)

def every_x_mins(x):
	"""
	Returns a function that will generate a datetime object that is x minutes
	in the future from a given argument.
	"""
	return lambda last: last + datetime.timedelta(minutes=x)

def daily_at(time):
	"""
	Returns a function that will generate a datetime object that is one day
	in the future from a datetime argument combined with 'time'.
	"""
	return lambda last: datetime.datetime.combine(last + datetime.timedelta(days=1), time)


def add_td(data=None, style_class='') :
	#
	"""
	renvoie une format <td>
	"""
	return "<td class='%s'>%s</td>" % ( style_class, data)
	
	
def add_tr(data=None, style_class='') :
	#
	"""
	renvoie une format <tr>
	"""
	return "<tr class='%s'>%s</tr>" % (style_class, data)

	
def gadget() :
	#C
	root = Tkinter.Tk()
	root.title("gadget ...")
	 
	#print "toto .... toto ..."
	buttonBox = Pmw.ButtonBox(root)
	buttonBox.add('Quitter', width=30, command = root.destroy)
	buttonBox.pack(side='bottom')
	root.mainloop()

def captureAsImageJpeg(win1) :
	"""
	on capture l'image de la fenetre en cours
	"""
	
	#--------------------
	#win1 = app.window_(title_re = ".*SUSIEV4")
	try :
		pp = win1.WrapperObject()
	except Exception, ValueError:
		# on ajoute un enregistrement xml planatge
		#print traceback.extract_stack() 
		msg_erreur =  "except lors capture image %s"  % str(ValueError)
		print msg_erreur 
		return False

	img = pp.CaptureAsImage()
	s_timestamp =  str(time.time())
	fic_img = "d:/temp/test_img_" + s_timestamp + ".jpg"
	img.save(fic_img, 'JPEG')
	# on peut afficher image
	#img.show()


# ******************************************
# Creation des repertoires utilisateurs
# ***************************************
def creerRepertoire( repertoire):
	#
	if not os.path.isdir(repertoire)  :
		try :
			os.mkdir(repertoire) # cree le repertoir usersusie
		except Exception, ValueError:
			#print Exception, ValueError
			tkMessageBox.showerror("Erreur ", u"Erreur system %s"  % str(ValueError))


	return True
# ******************************************
# Suppression Repertoire
# ***************************************
def suppressionRepertoire(repertoire) :
	errors = []
	if os.path.isdir(repertoire) :

		#os.unlink(rep_user_susie)
		os.chmod( repertoire, stat.S_IWRITE )

		#os.unlink(rep_user_susie)
		#os.mkdir(rep_susie) # suppression
		shutil.rmtree(repertoire, True)

		"""
		try:
			os.remove(repertoire)

		except OSError, why:
			if WindowsError is not None and isinstance(why, WindowsError):
				# Copying file access times may fail on Windows
				pass
			else:
				errors.extend((src, dst, str(why)))
		if errors:
			raise Error, errors
		"""
	else :
		#pass 
		tkMessageBox.showerror("Erreur ", u"Suppression impossible ce réperoire %s n'existe pas !"  % str(repertoire))

	return 	True
	

#------------------------------------
# isdirectory test l'existane du rep
#-----------------------------
def isDirectory(repertoire) :
	#
	r_dir = repertoire.replace("\\", "/")
	#print r_dir
	return  os.path.isdir(r_dir) 


#------------------------------------
# isdirectory test l'existane du rep
#-----------------------------
def isFileExist(fichier) :
	#
	r_fic = fichier.replace("\\", "/")
	#print r_fic
	return os.path.exists(r_fic)
	
# ******************************************
# Suppression Repertoire
# ***************************************
def suppressionRepertoire(repertoire) :
	errors = []
	if os.path.isdir(repertoire) :
		try :
			#os.unlink(rep_user_susie)
			os.chmod( repertoire, stat.S_IWRITE )
			#os.unlink(rep_user_susie)
			#os.mkdir(rep_susie) # suppression
			shutil.rmtree(repertoire, True)
		
			"""
			try:
				os.remove(repertoire)
				
			except OSError, why:
				if WindowsError is not None and isinstance(why, WindowsError):
					# Copying file access times may fail on Windows
					pass
				else:
					errors.extend((src, dst, str(why)))
			if errors:
				raise Error, errors
			"""
		except OSError:
			messages = r"Erreur %s : Suppression impossible ce réperoire %s !"  % (getDateNow(), str(OSError))
			self.traceAppli(messages)
			
	else :
		#pass
		messages = r"Erreur %s : Suppression impossible ce réperoire %s n'existe pas !"  % (getDateNow(), str(repertoire))
		tkMessageBox.showerror("Erreur ", messages)
		
		self.traceAppli(messages)
	
	return 	True

	
#---------------------------------------
# suppression Transaction From File DataXml
#---------------------------------------	
def deleteConfigUserFromFileXml(username) :
	#-------------------------------------------------------
	# on charge le fichier data xml en xmldoc
	#-------------------------------------------------------
	fichierData = os.getcwd() + "/config/param.xml"
	if not os.path.isfile(fichierData) :
		return False
	
	xmldoc = minidom.parse(fichierData)
	root = xmldoc.getElementsByTagName("ROOT")
	top = root[0]
	les_usernames = top.getElementsByTagName('PARAM')
	
	for user_courant in les_usernames :
		#
		x_nom = user_courant.getElementsByTagName('USERNAME')[0]
		if username == x_nom.firstChild.data :
			# suppression element
			top.removeChild(user_courant)
			# ------------------------
			# save contenu en fichier
			# ------------------------
			contenueXml = xmldoc.toxml()
			# save contenu en fichier
			afout  = open(fichierData, 'w', 'utf-8')
			afout.write(contenueXml)
			#on clos 
			afout.close()
			#print "username supprimmer %s " % (username )
			return True
	return False
		
#-----------------------------------------------
# mise a jour balise xml
#----------------------------------------------	
def updateBaliseXml(xmldoc, elem, data_value) :
	#
	if( elem.hasChildNodes()) :
		elem.firstChild.data =  data_value
	else :	
		# 
		text_xml= xmldoc.createTextNode(data_value)
		elem.appendChild(text_xml)
	return elem

#---------------------------------------
# suppression Transaction From File DataXml
#---------------------------------------	
def searchConfigUserFromFileXml(username) :
	# on charge le fichier data xml en xmldoc
	fichierData = os.getcwd() + "/config/param.xml"
	
	if not os.path.isfile(fichierData) :
		return False
	
	xmldoc = minidom.parse(fichierData)
	root = xmldoc.getElementsByTagName("ROOT")
	top = root[0]
	les_usernames = top.getElementsByTagName('PARAM')
	
	for user_courant in les_usernames :
		#
		x_nom = user_courant.getElementsByTagName('USERNAME')[0]
		if username == x_nom.firstChild.data :
			# element trouver
			#print "username trouver ... %s " % (username )
			return user_courant
	return False
		

	
#-----------------------------------------------
# recherche en expression regulieres
#----------------------------------------------					
def rechercheREG() :
			
	pattern = """^		# beginning of string M{0,4}
				# thousands - 0 to 4 M's(CM|CD|D?C{0,3})
				# hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
				#or 500-800 (D, followed by 0 to 3 C's)
				(XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
				#        or 50-80 (L, followed by 0 to 3 X's)(IX|IV|V?I{0,3})
				# ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
				#        or 5-8 (V, followed by 0 to 3 I's) $
				# end of string"
				"""
	## re.search(pattern, 'M', re.VERBOSE)    

	chaine = "Les valeurs sont 10, 56 et enfin 38."
	chaine = "730780111M060010090140110012      saiz@free.fr     060120101401 support@softwaymedical.fr 2010270319402384001060120108 14002201011110003401           Z501    A966    M1701 2110011"; 

	#re_mon_expression = re.compile(r"\D*(\d+)\D*(\d+)\D*(\d+)", re.I)
	re_mon_expression = re.compile(r"\W*([a-z]+[@]\D+[.]\D{2,3})\W*", re.I)
	#re_mon_expression = re.compile(r"\W*([Z]\d+)\W*", re.I)
	resultat = re_mon_expression.search(chaine)
	# resultat = re.search("^[a-zA-Z].+", ligne );

	liste = resultat.groups()
	for une_valeur in liste  :
		#print une_valeur
		msg = une_valeur
	return iste
	
def getDateNow() :
	"""
	return la date-heure maintenant 
	"""
	maintenant = datetime.now()
	return str(maintenant.strftime("%d-%m-%Y %H:%M:%S"))
#-----------------------------------------------
# lancer subprocess sans fenetre dos
#----------------------------------------------

def subprocessLaunchWithoutConsole(commande):
	"""Launches 'command' windowless and waits until finished"""
	#startupinfo = subprocess.STARTUPINFO
	#startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	code_erreur 	= "erreur"
	data 		= "data"
	erreur 		= "erreur"
	#traceLog("\n la commande = %s " %  commande)
	#proc = subprocess.Popen(["/usr/bin/ffmpeg -i /home/aziz/dev/python/convertor/in/AlienTheory.avi -deinterlace -sameq outputfile.avi"], shell=True)
	
		
	try:
		proc = subprocess.Popen([commande],  shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
		#proc = subprocess.Popen(["/usr/bin/ffmpeg -i /home/aziz/dev/python/convertor/in/AlienTheory.avi -
		#deinterlace -sameq out/outputfile.avi"], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
		#stdout, stderr = proc.communicate(str.encode('latin1'))
		if proc.returncode :
			code_erreur 	= proc.returncode
		if proc.stdout :
			data 	= proc.stdout.readlines()
		if  proc.stderr :
			erreur	= proc.stderr.readlines()

		return (proc.returncode, data , erreur)
		
	except Exception, message :
		#messages = "Exception %s: subprocessLaunchWithoutConsole %s" %(ex.errno, ex.strerror)
		text_messages = "Exception ***: subprocessLaunchWithoutConsole %s" %(message)
		tkMessageBox.showerror("Exception:", text_messages)
		return ("", "", str(message))

#-----------------------------------------------
# lancer subprocess sans fenetre dos
#----------------------------------------------	
def launchWithoutConsole(command, args):
	"""Launches 'command' windowless and waits until finished"""
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	#
	return subprocess.Popen([command] + args, startupinfo=startupinfo).wait()


## {{{ http://code.activestate.com/recipes/205377/ (r3)
# striplist.py

# Take a list of string objects and return the same list
# stripped of extra whitespace.

def striplist(l):
    return([x.strip() for x in l])

# This may look a bit more elegant, but it is significantly slower than
# striplist(). This may be dur to the fact that it's using the string.strip()
# method.

from string import strip
def inefficient(l):
    return(map(strip, l))
del strip
# Another version of inefficient() using builtin strip()
def inefficient_as_well(l):
    return(map(lambda x: x.strip(), l))

# This is only slightly slower than or comparable to striplist()
def comparable(l) :
    for x in xrange(len(l)):
        l[x] = l[x].strip()
    return(l)

# This is also on the same order as both comparabale() & striplist()
def comparable_as_well(l) :
    tmp = []
    for x in len(l):
        tmp.append(x.strip())
    return(tmp)

#----------------------------
# tracage des message erreur
#----------------------------
import logging
def traceLog(msg='', type=logging.INFO) :
	"""
	:param msg:
	:return: logging.info

	if type == INFO:
		return logging.info("erreur = {}".format(msg))
	if type == ERROR:
		return logging.error("erreur = {}".format(msg))
	if type == DEBUG:
		return logging.debug("erreur = {}".format(msg))
	"""
	pass


def getChildProcess(process_pid):
	#
	wmi=win32com.client.GetObject('winmgmts:')
	process_fils = []
	#
	for p in wmi.InstancesOf('win32_process'):
		#
		if p.ProcessId == process_pid :
			#print p.Name, p.Properties_('ProcessId'), int(p.Properties_('UserModeTime').Value)+int(p.Properties_('KernelModeTime').Value)
			children = wmi.ExecQuery('Select * from win32_process where ParentProcessId=%s' %p.Properties_('ProcessId'))
			for child in children:
				#print '\t', child.Name, child.Properties_('ProcessId'), int(child.Properties_('UserModeTime').Value)+int(child.Properties_('KernelModeTime').Value)
				process_fils.append(child.Properties_('ProcessId'))
			#
			if len (process_fils) > 0 : 
				return process_fils
			
	return None
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    re.sub('[-\s]+', '-', value)

def ajouterRepertoires():
	"""
	Ouvrir plusieur dossiers a la fois en utilisant
	askopendirectory
	"""
	options = {}
	#options['initialdir'] = os.path.dirname(os.path.abspath(__file__))
	options['initialdir'] = self.var_environnement_default['LOCAL_DIR']
	options['title'] = 'Choisissez un repertoire'
	#options['multiple'] = 1
	
	#folders = askdirectory( **options )
	#
	dirs = []
	title = 'Choose Directory'
	while True:
		dir = askdirectory(title=title)
		if not dir:
			break
			title = 'saisir %s. autre répértoire' % dirs[-1]
	return dir
	