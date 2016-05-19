from xml.etree import ElementTree
import csv
import io
import os
import re
import mechanize
import cookielib
from bs4 import BeautifulSoup

diretorio = 'mets/'
files = []
for file in os.listdir(diretorio):
    if file.endswith(".xml"): 
        files.append(file)

def escrever_arquivo(array):
		with io.open ('listaBDTD.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)
naoenc = []
naotese = []
tags = []
for filexml in files:
	with open(diretorio + filexml, 'rt') as f:
	    tree = ElementTree.parse(f)
	    root = tree.getroot()
	    array = ['' for x in range(0,8)]
	    contrib = []
	    ehtese = False
	    tese = False
	    ehautor = False
	    for indentifier in root.findall("{http://www.loc.gov/METS/}identifier"):
	    	id = indentifier.text[23:]
	    	id = id.replace('-','/')

	    #verifica no oai.agregador se e tese ou dissertacao
	    mech = mechanize.Browser()
	    url = "http://oai.agregador.ibict.br/request?verb=GetRecord&identifier=oai:agregador.ibict.br." + id + "&metadataPrefix=oai_dc"
	    page = mech.open(url)
	    html = page.read()
	    soup = BeautifulSoup(html)
	    for i in soup.findAll('dc:type'):
	    	tese = True
	    	if ('master' or 'doctoral') in i.text:
	    		ehtese = True
	    		print url
	    		print filexml
	    if not tese:
	    	naotese.append(id)

	    #caso seja tesa ou dissertacao continua a execucao
	    if ehtese:
	    	for records in root.findall('{http://www.loc.gov/METS/}dmdSec'):
		    	for child in records:
		    		for child in child.getchildren():
		    			for i,child in enumerate(child.getchildren()):
		    				#formato 1
		    				if child.tag == '{http://www.loc.gov/mods/v3}mods':
		    						for child in child.getchildren():
		    							if child.tag == '{http://www.loc.gov/mods/v3}name':	
					    					for n,child in enumerate(child.getchildren()):
					    						if child.tag == '{http://www.loc.gov/mods/v3}role':
					    							for child in child.getchildren():
					    								if (child.text == 'author'):
					    									ehautor = True
					    								else:
					    									ehautor = False
					    									contrib.append(['' for x in range(0,3)])
					    						elif child.tag == '{http://www.loc.gov/mods/v3}namePart':
					    							if child.text != None:
					    								texto = child.text.encode('utf-8').split(',')
					    								texto.reverse()
					    								if len(texto) > 1:
					    									t1 = texto[0][1:] + ' ' + texto[1]
					    								else:
					    									t1 = texto[0]
					    								if ehautor:
					    									array[0] = t1
					    								else:
					    									contrib[len(contrib) - 1][0] = t1
					    						else:
					    							tags.append(child.tag)
					    							print 'aqui' , child.tag

					    				if child.tag == '{http://www.loc.gov/mods/v3}titleInfo':
					    					for child in child.getchildren():
						    					if child.text != None:
						    						if (array[3] == ''):
						    							array[3] = child.text.encode('utf-8')

					    				if child.tag == '{http://www.loc.gov/mods/v3}extension':
					    					for child in child.getchildren():
					    						if child.tag == '{http://www.loc.gov/mods/v3}dateSubmitted':
					    							if child.text != None:
					    								array[5] = child.text.encode('utf-8')

					    	#formato 2
		    				if child.tag == '{http://www.loc.gov/mods/v3}name':	
		    					for n,child in enumerate(child.getchildren()):
		    						if child.tag == '{http://www.loc.gov/mods/v3}role':
		    							for child in child.getchildren():
		    								if (child.text == 'author'):
		    									ehautor = True
		    								else:
		    									ehautor = False
		    									contrib.append(['' for x in range(0,3)])
		    						elif child.tag == '{http://www.loc.gov/mods/v3}namePart':
		    							if child.text != None:
		    								texto = child.text.encode('utf-8').split(',')
		    								texto.reverse()
		    								if len(texto) > 1:
		    									t1 = texto[0][1:] + ' ' + texto[1]
		    								else:
		    									t1 = texto[0]
		    								if ehautor:
		    									array[0] = t1
		    								else:
		    									contrib[len(contrib) - 1][0] = t1
		    						else:
		    							tags.append(child.tag)
		    							print 'aqui' , child.tag

		    				if child.tag == '{http://www.loc.gov/mods/v3}titleInfo':
		    					if child.text != None:
		    						array[3] = child.text.encode('utf-8')

		    				if child.tag == '{http://www.loc.gov/mods/v3}extension':
		    					for child in child.getchildren():
		    						if child.tag == '{http://www.loc.gov/mods/v3}dateSubmitted':
		    							if child.text != None:
		    								array[5] = child.text.encode('utf-8')

		    
		    

	    	array[7] = id
	    	for i in soup.findAll('dc:source'):
	    		if ('instname') in i.text:
	    			t = i.text.split(':')
	    			array[6] = t[1]
	    	for i in contrib:
		    	for j in i:
		    		array.append(j)

		escrever_arquivo(array)