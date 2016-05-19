from xml.etree import ElementTree
import csv
import io
import os
import re
import mechanize
from bs4 import BeautifulSoup


diretorio = 'xoai/'
files = []
for file in os.listdir(diretorio):
    if file.endswith(".xml"):
        files.append(file)

def escrever_arquivo(array):
		with io.open ('listaBDTD.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)

pesquisadores = []

naoenc = []
naotese = []
tagnaoenc = []
intials = ['Autor' , 'CPF' , 'Lattes' , 'Titulo' , 'Programa' , 'Data defesa' , 'Intituicao' , 'Identificador' , 'Contribuidor Nome' , 'Contribuidor CPF' , 'Contribuidor Lattes', 'Contribuidor Nome' , 'Contribuidor CPF' , 'Contribuidor Lattes']
escrever_arquivo(intials)

for filexml in files:
	with open(diretorio + filexml, 'rt') as f:
	    tree = ElementTree.parse(f)

	root = tree.getroot()
	ehtese = False
	tese = False

	#verifica no oai.agregador se e tese ou dissertacao
	for indentifier in root.findall("{http://www.lyncode.com/xoai}identifier"):
		id = indentifier.text[23:]
		mech = mechanize.Browser()
		url = "http://oai.agregador.ibict.br/request?verb=GetRecord&identifier=oai:agregador.ibict.br." + id + "&metadataPrefix=oai_dc"
		try:
			page = mech.open(url)
			html = page.read()
			soup = BeautifulSoup(html)
			for i in soup.findAll('dc:type'):
				tese = True
				if ('master' or 'doctoral') in i.text:
					ehtese = True
					print filexml
			if not tese:
				naotese.append(id)
		except:
			naoenc.append(id)

	#caso seja tesa ou dissertacao continua a execucao
	if ehtese:
		array = ['' for x in range(0,8)]
		autorv  = ['' for x in range(0,5)]
		contrib = []
		
		inseridos = dict()
		index = 0
		autorf = False
		num = []
		possuiC = False
		for records in root.findall('{http://www.lyncode.com/xoai}element'):
			for child in records:
				for r in child.findall("[@name='title']"):
					for child in r.getchildren():
						for child in child.getchildren():
							if child.text != None and child.attrib != {'name': 'eng'}:
								array[3] = child.text.encode('utf-8')

				for r in child.findall("[@name='publisher']"):
					for child in r.getchildren():
						if child.attrib == {'name': 'program'}: 
							for child in child.getchildren():
								for child in child.getchildren():
									if child.text != None:
										array[4] = child.text.encode('utf-8')

						if (child.attrib == {'name': 'por'} or child.attrib == {'name': 'none'} or child.attrib == {'name': 'pt_BR'}) : 
							for child in child.getchildren():
								if child.text != None:
										array[6] = child.text.encode('utf-8')

				#Pra captura o campo programa da UNESP
				for r in child.findall("[@name='graduateProgram']"):
					for child in r.getchildren():
						for child in child.getchildren():
								if child.text != None:
									array[4] = child.text.encode('utf-8')

				for r in child.findall("[@name='degree']"):
					for child in r.getchildren():
						if child.attrib == {'name': 'program'}: 
							for child in child.getchildren():
								for child in child.getchildren():
									if child.text != None:
										array[4] = child.text.encode('utf-8')

						if (child.attrib == {'name': 'granto'}) : 
							for child in child.getchildren():
								if child.text != None:
										array[6] = child.text.encode('utf-8')



				for r in child.findall("[@name='date']"):
					for child in r.getchildren():
						if child.attrib == {'name': 'issued'}: 
							for child in child.getchildren():
								for child in child.getchildren():
									if child.text != None:
										array[5] = child.text.encode('utf-8')

			

				for r in child.findall("[@name='creator']"):
					autorf = True
					for child in r.getchildren():
						if (child.attrib == {'name': 'ID'} or child.attrib == {'name': 'id'}):
							index = 1
						elif (child.attrib == {'name': 'Lattes'} or child.attrib == {'name': 'lattes'}):
							index = 2
						elif (child.attrib == {'name': 'none'} or child.attrib == {'name': 'pt_BR'}):
							index = 0
						else:
							index = -1
							tagnaoenc.append(child.attrib)
							print child.attrib , 'TAG NAO ENCONTRADA'
						for child in child.getchildren():
							if child.tag == '{http://www.lyncode.com/xoai}field':
								if child.text != None:
									print child.text , child.attrib
									array[0] = child.text.encode('utf-8')
							for n,child in enumerate(child.getchildren()):
								if child.text != None:
									print child.text, child.attrib
									array[index] = child.text.encode('utf-8')
									index = 0
				for r in child.findall("[@name='contributor']"):
					for child in r.getchildren():
						if not autorf and child.attrib == {'name': 'author'} or child.attrib == {'name': 'authorID'} or child.attrib == {'name': 'authorLattes'} :
							foundA = re.search( 'author(.*)' , child.attrib.values()[0]).group(1)
							for child in child.getchildren():
								for n,child in enumerate(child.getchildren()):
									if child.text != None:
										if foundA == 'Lattes':
											array[2] = child.text.encode('utf-8')
										elif foundA == 'ID':
											array[1] = child.text.encode('utf-8')
										elif n==0 and foundA == '':
											array[n] = child.text.encode('utf-8')
						elif (child.attrib != {'name': 'institution'} and child.attrib != {'name': 'other'}): 
							attrib = child.attrib.values()[0]
							num = re.findall('\d+', attrib)
							d = ['ID' , 'id' , 'Lattes' , 'lattes' ,'']
							for x in d:
								if x in attrib:
									enc = x
									if num == []:
										found = re.search('(.*)' + x , attrib).group(1)
										ind = found + '0'
									else:
										found = re.search('(.*)' + num[0] , attrib).group(1)
										ind = found + num[0]

						 			if not inseridos.has_key(ind):
										contrib.append(['' for x in range(0,3)])
										i = len(contrib) - 1
										inseridos[ind] = i
										break
									else:
										i = inseridos[ind]
										break
							if enc == 'ID':
								index = 1
							elif enc == 'Lattes':
								index = 2
							elif enc == '':  
								index = 0
							for child in child.getchildren():
								for n,child in enumerate(child.getchildren()):
									if child.text != None:
										contrib[i][index] = child.text.encode('utf-8')
										print child.text



		for indentifier in root.findall("{http://www.lyncode.com/xoai}identifier"):
			array[7] = indentifier.text[23:]
		
		for i in contrib:
			for j in i:
				array.append(j)

		escrever_arquivo(array)