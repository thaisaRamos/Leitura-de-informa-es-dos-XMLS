from xml.etree import ElementTree
import csv
import io
import os
import mechanize
from bs4 import BeautifulSoup

files = []
diretorio = 'mtd2-br/'
for file in os.listdir(diretorio):
    if file.endswith(".xml"):
        files.append(file)

def escrever_arquivo(array):
		with io.open ('listaBDTD.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)

tags = []

for filexml in files:
	with open(diretorio + filexml, 'rt') as f:
	    tree = ElementTree.parse(f)

	root = tree.getroot()
	for indentifier in root.findall('identifier'):
		id = indentifier.text[23:]

	for indentifier in root.findall('{http://www.ibict.br/schema/}identifier'):
		id = indentifier.text[23:]
	


	array = ['' for x in range(0,9)]
	contrib = []
	for autor in root.findall('{http://oai.ibict.br/mtd2-br/}Autor'):
		info = autor.getchildren()
		for i in info:
			if not i.getchildren():
				if i.text != None:
					if i.tag == '{http://oai.ibict.br/mtd2-br/}Nome':
						array[0] = i.text.encode('utf-8')
					elif i.tag == '{http://oai.ibict.br/mtd2-br/}Lattes':
						array[2] = i.text.encode('utf-8')
					elif i.tag == '{http://oai.ibict.br/mtd2-br/}CPF':
						array[1] = i.text.encode('utf-8')
					else:
						tags.append(i.tag)
	for titulo in root.findall('{http://oai.ibict.br/mtd2-br/}Titulo'):
		print titulo.attrib , titulo.tag , titulo.text
		if (titulo.attrib == {'Idioma': 'pt'} or titulo.attrib == {'Idioma': 'por'}):
			if titulo.text != None:
				array[3] = titulo.text.encode('utf-8')

	for data in root.findall('{http://oai.ibict.br/mtd2-br/}DataDefesa'):
		if data.text != None:
			array[5] = data.text.encode('utf-8')

	for dados in root.findall('{http://oai.ibict.br/mtd2-br/}InstituicaoDefesa'):
		info = dados.getchildren()
		for i in info:
			if i.tag == '{http://oai.ibict.br/mtd2-br/}Nome':
				if i.text != None:
					array[6] = i.text.encode('utf-8')
			if i.tag == '{http://oai.ibict.br/mtd2-br/}Programa':
				for i in i:
					if i.text != None:
						array[4] = i.text.encode('utf-8')

	for j,contribuidor in enumerate(root.findall('{http://oai.ibict.br/mtd2-br/}Contribuidor')):
		contrib.append(['' for x in range(0,3)])
		info = contribuidor.getchildren()
		for n,i in enumerate(info):
			if i.text != None:
				if i.tag == '{http://oai.ibict.br/mtd2-br/}Nome':
					contrib[j][0] = i.text.encode('utf-8')
				elif i.tag == '{http://oai.ibict.br/mtd2-br/}Lattes':
					contrib[j][2] = i.text.encode('utf-8')
				elif i.tag == '{http://oai.ibict.br/mtd2-br/}CPF':
					contrib[j][1] = i.text.encode('utf-8')
	array[7] = id
	array[8] = filexml
	for i in contrib:
		for j in i:
			array.append(j)

	print filexml

	escrever_arquivo(array)