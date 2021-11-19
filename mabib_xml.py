# -*- coding: iso8859_1 -*-
# module local
import os, sys
import re
import tkMessageBox
from tkFileDialog import askopenfile
from xml.dom import minidom
import xml.parsers.expat
from datetime import datetime
from codecs import open
from string import Template



def chargeFichierParam():
		#
		"""
		1 == ELEMENT_NODE, 2 == ATTRIBUTE_NODE, 3 == TEXT_NODE, 4 == CDATA_SECTION_NODE, 5 == ENTITY_NODE, 6 == PROCESSING_INSTRUCTION_NODE, 7 == COMMENT_NOD
		"""
			
		# on recupere fichier param
		filename = os.getcwd() + "/config/param.xml"
		if( not os.path.isfile(filename) or os.path.getsize(filename) == 0) :
			messages = "Erreur : Attention le fichier de parametrage est innexistant ou vide, recharger le !! " + filename
			tkMessageBox.showerror(messages)
			#self.traceAppli(messages)
			return False
		
		
		ligne = user_courant.firstChild # ok si on trouve on recupere l'entete user
		#ligne = top_ligne
		#
		
		
		ligneXml_dico = {}
		# ligne.firstChild.nodeType == 3 === type text
		# ligne.firstChild.nodeType == 1 === type Noeux
		while (ligne and ligne.nodeType == 1) :
			#-------------------------------------------------------
			#on charge la donnÃ©e de la balise correspondant au noeux
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
		


#-------------------------------------------------------------------
# enregitrement data scenario transations
#------------------------------------------------------------------
def saveFileDataXml() :
        #print scenario_list_transactions
        dialog3 = Pmw.MessageDialog(self.parent, title= 'Confirmation',
                message_text = 'Souhaiter-vous Enregistrer ce scenario ?',
                buttonboxpos = 'e', iconpos = 'n', icon_bitmap = 'warning',
                buttons = ('Ok', 'Annuler', 'Close'),
                defaultbutton = 'Close')
        dialog3.withdraw()
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

        xmldoc = minidom.parse(fichierData)
        root = xmldoc.getElementsByTagName("ROOT")
        
        new_scenario    = createElemntXml(xmldoc, 'SCENARIO')
        scenario_id     = xmldoc.createAttribute('ID')
        scenario_id.nodeValue = str(t_id)
        new_scenario.setAttributeNode(scenario_id)
        
        scenario_created = xmldoc.createAttribute('CREATED')
		scenario_created.nodeValue = str(date_complet)
		new_scenario.setAttributeNode(scenario_created)
		
		for  options in self.db_transactions[self.id_scenario_courant] :
                #---------------------------------
                # Creer les noeux de transactions
                #---------------------------------
                t_nom 	= options['nom'].split(':')
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
		

	