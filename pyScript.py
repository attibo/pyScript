#! /usr/bin/env python
# coding: utf-8
# pyScript.py
# progetto di utility per la gestione degli script di backup (.sh)
# Attilio Bongiorni - maggio 2017
#--------------------------------
import os
import shutil
import commands
import string
import subprocess
import datetime
import getpass

# funzione writelog(operazione,logfile,dt,ev)
# scrive una stringa in un file di log
# parametri-------------------------- 
# operazione: stringa da scrivere 
# logfile: nome del file log per default (se logfile="") è logpyback.log 
# dt: se dt= 1 inserisce data e ora dell'operazione, 
# ev: se ev=1 evidenza, premette il simbolo (!)
# Attilio Bongiorni - maggio 2017

def writelog(operazione,logfile,dt,ev):
	
	if logfile == "":
		logfile = "logpyback.log"	
	
	# se il file non esiste lo crea
	if not os.path.exists(logfile):
		fileHandle = open(logfile, "w")
		now=datetime.datetime.now()
		fileHandle.write("*Pyback - file di log creato il "+now.strftime("%Y-%m-%d %H:%M")+"\n")
		# chiude il file e lo riapre in mod. append
		fileHandle.close()
		
	fileHandle = open(logfile, "a")
	now=datetime.datetime.now()
	if ev==1:
		operazione = "(!)"+operazione
	if dt==1:
		operazione = now.strftime("%Y-%m-%d %H:%M") + "-" +operazione
		fileHandle.write(operazione + "\n")
		fileHandle.close()
			
	return


# getFile() Acquisisce in archivio un file script (.sh)
# il nome del file viene registrato in elencoFiles.txt
# catalogo = nome del file archivio degli script nomefile= nome del file da registrare (completo di path)
# in caso di errore ritorna 0
# Attilio Bongiorni - maggio 2017

def getFile(nomefile, catalogo):
	
	if os.path.exists(nomefile):
		handle = open(catalogo,"a")
		handle.write(nomefile+"\n")
		vr=1
	else:
		print "File non esistente" + "\n"
		vr=0
	return vr

# funzione getComment()
# legge uno script bash e ricava i commenti, serve per pyback in modo da visualizzare
# sullo schermo le informazioni sullo script
# Attilio Bongiorni - maggio 2017

def getComment(nomefile):
	
	commenti=[]
	if os.path.exists(nomefile):
		fileHandle = open(nomefile, "r")	
		
		for linea in fileHandle:
			if linea[0]=="#":		
				commenti.append(linea)
			
				
		fileHandle.close()
			
	return commenti		

# showFile() Visualizza l'elenco dei files script in archivio 
# catalogo = nome del file archivio degli script 
# ritorna il dizionario con i dati degli script
# es. dizScript[1] --> script1.sh ecc.
# oppure: dizMount[1] =  1 - Windows anagrafe,"Attilio Bongiorni","//192.168.1.26/Users/Attilio Bongiorni/",/mnt/pyback
# Attilio Bongiorni - maggio 2017
# giugno 2017:
# nuova versione, gestisce le righe commentate e crea i cataloghi se non ci sono

def showFiles(catalogo):

	n = 0
	now=datetime.datetime.now()
	#creiamo un dizionario per gli script
	dicScript = dict()
	if os.path.exists(catalogo):
		handle = open(catalogo, "r")
		archivio=handle.readlines()
		handle.close()
		if len(archivio) == 0:
			print "Archivio script vuoto! \n"
			vr = 0
		else:
			for script in archivio :
				if not script.startswith("#"):
					n=n+1
					print repr(n) + " - " + script.rstrip()
					dicScript[n] = script.rstrip()
					vr = 1
	else:
		print "File catalogo inesistente, viene creato! \n"
		handle=open(catalogo,"w")
		if catalogo=="catalogo.txt":
			handle.write("#file catalogo creato il "+ now.strftime("%Y-%m-%d %H:%M")+"\n")
			handle.close()
		elif catalogo=="cifsarc.txt":
			handle.write("# file cifsarc.txt creato il: "+ now.strftime("%Y-%m-%d %H:%M")+"\n")
			handle.write("# struttura dell'archivio di mountpoint cifs:\n")
			handle.write("# descrizione,username,percorso_di_rete,punto di mount\n")
			handle.write("# esempio: descrizione,\"Username Windows\",\"//192.168.1.100/Users/Nome Utente Windows/\",/mnt/mountpoint\n")
			handle.write("# la password viene richiesta al momento del mount<br>")
			handle.close()
		else:
			handle.write("#file catalogo creato il "+ now.strftime("%Y-%m-%d %H:%M")+"\n")
			handle.close()
		vr=0
	
	return dicScript	
#######################################################################
# MJoin
# Copyright (C) 2008  Simone Cansella (aka checkm)
#                       <matto.scacco@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

def color (string):
    colors = {"default":0, "black":30, "red":31, "green":32, "yellow":33,
          "blue":34,"magenta":35, "cyan":36, "white":37, "black":38,
          "black":39} #33[%colors%m
    
    for color in colors:
        color_string = "\033[%dm\033[1m" % colors[color]
        string = string.replace("<%s>" % color, color_string).replace("</%s>" % color, "\033[0m")
    
    return string
	
	
# elimina i doppi spazi tra una parola e l'altra
# lasciandone uno solo
# Attilio Bongiorni - Maggio 2017

def nodoppispazi(stringa):

	parsed = ""
	flagspazi = 0
	n = 0

	for token in stringa:
		if token <>" ":
			parsed=parsed+token
			flagspazi = 0
		elif token == " " and flagspazi == 0 :
			flagspazi = flagspazi +1
			parsed = parsed + token
	
	return parsed	

# archivia(nomescript,nomearchivo)
# copia lo script nomescript e lo appende all'archivio nomearchivio
# serve per archiviare il codice degli script più importanti e complicati
# in un archivio .txt
# progetto di utility per la gestione degli script di backup (.sh)
# Attilio Bongiorni - maggio 2017
#--------------------------------
def archivia(nomescript, nomearchivio):
	
	# valore ritornato dalla funzione
	vr = 0
	
	# per default è scriptarc.txt
	if nomearchivio == "":
		nomearchivio = "scriptarc.txt"
		
	# se esiste lo script sh 	
	if os.path.exists(nomescript):
		scriptHandle = open(nomescript,"r")
		
		# se l'archvio script non esiste lo crea
		# altrimenti lo apre
		if os.path.exists(nomearchivio):
			arcHandle = open(nomearchivio,"a")
		else:
			arcHandle = open(nomearchivio,"w")
			now=datetime.datetime.now()
			arcHandle.write("# archivio script creato il "+ now.strftime("%Y-%m-%d %H:%M")+"\n")			

		now=datetime.datetime.now()
		arcHandle.write("# ----------------------------------------\n")
		arcHandle.write("# "+ now.strftime("%Y-%m-%d %H:%M")+"\n")
		arcHandle.write("# script archiviato: " + nomescript + "\n")
		arcHandle.write("# ----------------------------------------\n")		
		
		for linea in scriptHandle:
			if linea.startswith("#! /bin/bash"):
				arcHandle.write("# shebangs omessa per sicurezza \n")
			else:
				arcHandle.write(linea)
				
	else: # se esiste lo script sh
		print("lo script "+ nomescript + " non esiste")	
		vr = 1
										
	arcHandle.close()
	scriptHandle.close()
		
	return vr


# shpymenu(listaMount)
# visualizza il menu
# il parametro listaMount è una lista python dei punti di mount che 
# risultano montati in quel momento, così vengono visualizzati
# progetto di utility per la gestione degli script di backup (.sh)
# Attilio Bongiorni - giugno 2017
#--------------------------------
def shpymenu(listaMount):
	print color("<yellow>Shpy 1.7 - Attilio Bongiorni - 2017</yellow>")
	print color("<yellow>--- COMANDI ---</yellow>")
	if len(mntList)>0:
		for dischi in listaMount:
			print color("<blue>(!) "+dischi+"</blue> ")
	print color("<yellow>agg</yellow> = refresh elenco files in catalogo")
	print color("<yellow>rem [numero] </yellow> = vedi i commenti di uno script")
	print color("<yellow>add [file e percorso completo]</yellow>  = aggiunge uno script a quelli già gestiti")
	print color("<yellow>sto [numeri separati da virgole] </yellow> = es.sto 1,2,5 archivia gli script n.1,2 e 5")
	print color("<yellow>edi</yellow> = edit manuale del catalogo degli script")
	print color("<yellow>eds [numero]</yellow> = modifica uno script in catalogo" )
	print color("<yellow>exe [numeri separati da virgole] </yellow> = es. exe 1,2,5 esegue gli script n.1,2 e 5")
	print color("<yellow>log </yellow> = visualizza il log di sistema")
	print color("<yellow>vih </yellow> = principali comandi dell'editor Vim")
	print color("<yellow>mnt </yellow> = elenco dei mount cifs")
	print color("<yellow>mnn [numero]</yellow> monta il disco cifs n.")
	print color("<yellow>umn [numero]</yellow> smonta il disco cifs n.")
	print color("<yellow>mne</yellow> edit manuale catalogo dei mount")
	print color("<yellow>men</yellow> visualizza il menu")
	print color("<yellow>end</yellow> = uscita")
	print "\n" 

	return
	
#=====================================	
#-------fine funzioni-----------------
#=====================================

print "Elenco script gestiti"
print "---------------------"
dizScript=showFiles("catalogo.txt")
print "---------------------"
comando =""
mntList=[]
while comando <> "end":
	# visualizzazione menu!
	
	shpymenu(mntList)
	# nota: dizScript è il dizionario generato dal showfiles()
	# mentre regoList è la stringa di comando inserito dall'operatore
	regolare = nodoppispazi(comando)
	regoList = regolare.split(" ")

	if regolare.startswith("agg"):
		showFiles("catalogo.txt")
		
	elif regolare.startswith("rem"):
		# len(regolist)> 1 vuol dire che ha dato anche un numero e non solo il comando
		if len(regoList)>1:
			#recupera il file dal dizionario ritornato da showfiles()
			#regolist è una lista che contiene comando e parametro es. rem 1
			nomeScript=dizScript[int(regoList[1])]
			righerem = getComment(nomeScript)
			print("Righe commentate per il file script: "+ nomeScript)
			print ("-------------")
			for rem in righerem:
				print rem.rstrip()
				
	elif regolare.startswith("add"):
		if len(regoList)>1:
			#recupera il nome del file inserito dall'operatore
			# dopo il comando rem ma qui non occorre l'int() perchè
			# non è un numero del menu ma un nome di file
			# e non deve attingere al dizionario ma solo al comando inserito
			nomeScript=regoList[1]
			if getFile(nomeScript, "catalogo.txt")>0:
				print "Inserimento effettuato correttamente \n"
				writelog("archiviato script"+nomeScript,"logpyback.log",1,0)
				dizScript=showFiles("catalogo.txt")
			else:
				print color("<red>Errore!</red> Il file che hai cercato di inserire non esiste")
				
	elif regolare.startswith("edi"):
		writelog("Inizio edit manuale catalogo", "logpyback.log",1,0)
		subprocess.call(['vim catalogo.txt'], shell=True)
		writelog("Fine edit manuale catalogo", "logpyback.log",1,0)
	
	elif regolare.startswith("eds"):
		# len(regolist)> 1 vuol dire che ha dato anche un numero e non solo il comando
		if len(regoList)>1:
			#recupera il file dal dizionario ritornato da showfiles()
			#regolist è una lista che contiene comando e parametro es. rem 1
			nomeScript=dizScript[int(regoList[1])]
			if os.path.exists(nomeScript):
				edit_call = [ "vim", nomeScript]
				writelog("vim "+ nomeScript,"logpyback.log",1,0)
				#funzionaaaa!
				edit = subprocess.call(edit_call)
				# se c'è stato un errore mette l'evidenza nel log (!)
				if edit>0:
					evidenza = 1
				else:
					evidenza = 0
				writelog("error code="+repr(edit),"logpyback.log",1,evidenza)
			else:
				print color("<red>Il file non esiste, è stato spostato o rimosso e il catalogo non è stato aggiornato</red>")
	
	elif regolare.startswith("exe"):
		# len(regolist)> 1 vuol dire che ha dato anche un numero e non solo il comando
		if len(regoList)>1:
			todo = regoList[1]
			todoList = todo.split(",")
			# inizio ciclo esecuzione multipla
			for daeseguire in todoList:
			# daeseguire è una stringa numerica
				try:
  					Ndaeseguire = int(daeseguire)
  				# blocco try except	
					nomeScript=dizScript[int(daeseguire)]
					if os.path.exists(nomeScript):
						writelog("esecuzione di "+ nomeScript,"logpyback.log",1,0)
						edit = subprocess.call(nomeScript)
						if edit>0:
							evidenza = 1
						else:
							evidenza = 0
						writelog("error code="+repr(edit),"logpyback.log",1,evidenza)
					else: #path exists
						writelog("File script: "+nomeScript+" inesistente","",1,1)
						print color("<red>Il file non esiste, è stato spostato o rimosso e il catalogo non è stato aggiornato</red>")
					# fine ciclo esecuzione multipla	
 				# blocco try except - fine  					
				except ValueError:
					cmderror = "I valori inseriti sono errati"
					writelog ("Comando errato :"+comando, "",1,1)
  					print('I valori inseriti non sono numerici o sono incongruenti')
	
	elif regolare.startswith("sto"):
		# len(regolist)> 1 vuol dire che ha dato anche un numero e non solo il comando
		if len(regoList)>1:
			todo = regoList[1]
			todoList = todo.split(",")
			# inizio ciclo archiviazione multipla
			for daeseguire in todoList:
			# daeseguire è una stringa numerica
				try:
  					Ndaeseguire = int(daeseguire)
  				# blocco try except	
					nomeScript=dizScript[int(daeseguire)]
					if os.path.exists(nomeScript):
						writelog("archiviazione di "+ nomeScript,"logpyback.log",1,0)
						# per default il nome dell'archivio è scriptarc.txt
						edit = archivia(nomeScript,"")
						if edit>0:
							evidenza = 1
						else:
							evidenza = 0
						writelog("error code="+repr(edit),"logpyback.log",1,evidenza)
					else: #path exists
						writelog("File script: "+nomescript+" inesistente","",1,1)
						print color("<red>Il file non esiste, è stato spostato o rimosso e il catalogo non è stato aggiornato</red>")
					# fine ciclo archiviazione multipla	
 				# blocco try except - fine  					
				except ValueError:
					cmderror = "I valori inseriti sono errati"
					writelog ("Comando errato :"+comando, "",1,1)
  					print('I valori inseriti non sono numerici o sono incongruenti')

	elif regolare.startswith("log"):
		if os.path.exists("logpyback.log"):
			edit_call = [ "vim", "logpyback.log"]
			edit=subprocess.call(edit_call)
	
	elif regolare.startswith("vih"):
		if os.path.exists("vimhelp.txt"):
			edit_call = ["vim", "vimhelp.txt"]
			edit = subprocess.call(edit_call)
		else:
			print("Il file vimhelp.txt non è presente")
	
	elif regolare.startswith("mnt"):
		showFiles("cifsarc.txt")
		
	elif regolare.startswith("mnn"):
		dizMount=showFiles("cifsarc.txt")
		
		# len(regolist)> 1 vuol dire che ha dato anche un numero e non solo il comando
		if len(regoList)>1:
			#recupera i dati del mount dal dizionario ritornato da showfiles()
			#regolist è una lista che contiene comando e parametro es. rem 1
			# pro memoria struttura del file cifsarc.txt:
			# descrizione,username,percorso_di_rete,punto di mount
			
			# controllo se ha inserito un valore out of range
			if int(regoList[1])<=len(dizMount): 			# parametro comando out of range ?
				mountPack=dizMount[int(regoList[1])]
				mount = mountPack.split(",")
				cifsDesc=mount[0]
				cifsUser=mount[1]
				cifsPath=mount[2]
				cifsMoun=mount[3]
				pwdMount=getpass.getpass("Password di rete: ")
				# esempio di un cifs mount:
				# sudo mount -t cifs -o username="Attilio Bongiorni",password=password "//192.168.2.26/Users/Attilio Bongiorni/" /mnt/pyback
				# NOTA: non è necessario mettere le virgolette nella concatenazione della stringa
				# perchè python le mette automaticamente non riesco a capire come faccia perchè nel caso di "password=+"pwdMount non la mette
				# mentre negli altri casi dove servono sì
				comando_mount = "sudo mount -t cifs -o username="+ cifsUser+",password="+pwdMount+" "+cifsPath +" " +cifsMoun
				
				# riattivare la linea seguente per un debug del comando
				# print("comando di mount generato: "+comando_mount)
				
				writelog("mount "+ cifsDesc,"logpyback.log",1,0)
				edit = subprocess.call(comando_mount, shell=True)
				#se c'è stato un errore mette l'evidenza nel log (!)
				if edit>0:
					evidenza = 1
					writelog("error code="+repr(edit),"logpyback.log",1,evidenza)
				else:
					mntList.append(cifsMoun)
					evidenza = 0
			else: 												# parametro comando out of range
				print color("<red>Numero mount inesistente!</red>")

	elif regolare.startswith("umn"):	
		dizMount=showFiles("cifsarc.txt")
		
		# len(regolist)> 1 vuol dire che ha dato anche un numero e non solo il comando
		if len(regoList)>1:
			#recupera i dati del mount dal dizionario ritornato da showfiles()
			#regolist è una lista che contiene comando e parametro es. rem 1
			# pro memoria struttura del file cifsarc.txt:
			# descrizione,username,percorso_di_rete,punto di mount
			
			# controllo se ha inserito un valore out of range
			if int(regoList[1])<=len(dizMount): 			# parametro comando out of range ?
				mountPack=dizMount[int(regoList[1])]
				mount = mountPack.split(",")
				cifsDesc=mount[0]
				cifsUser=mount[1]
				cifsPath=mount[2]
				cifsMoun=mount[3]
				comando_umount = "sudo umount "+cifsMoun
				writelog("umount "+ cifsDesc,"logpyback.log",1,0)
				edit = subprocess.call(comando_umount, shell=True)
				#se c'è stato un errore mette l'evidenza nel log (!)
				if edit>0:
					evidenza = 1
					writelog("error code="+repr(edit),"logpyback.log",1,evidenza)
				else:
					cancMount = mntList.index(cifsMoun)
					del mntList[cancMount]
					evidenza = 0
			else: 												# parametro comando out of range
				print color("<red>Numero mount inesistente!</red>")
		
	elif regolare.startswith("mne"):
		writelog("Inizio edit manuale catalogo punti di mount", "logpyback.log",1,0)
		subprocess.call(['vim cifsarc.txt'], shell=True)
		writelog("Fine edit manuale catalogo punti di mount", "logpyback.log",1,0)
		
	elif regolare.startswith("men"):
		shpymenu(mntList)

	
	#--------input------------
	comando = raw_input("comando ---> ")
	
             

	
	
	