from xml.etree import ElementTree
import csv
import io
import os
 
diretorio = 'mtd-br/'

files = []
for file in os.listdir(diretorio):
    if file.endswith(".xml"):
        files.append(file)

def escrever_arquivo(array):
		with io.open ('listaBDTD.csv', 'ab') as fp:
		    writer = csv.writer(fp, delimiter=';')
		    writer.writerow(array)

tags = []

for i,filexml in enumerate(files):
	with open(diretorio + filexml, 'rt') as f:
		tree = ElementTree.parse(f)

		print filexml
		array = ['' for x in range(0,8)]
		contrib = []

		root = tree.getroot()

		for indentifier in root.findall('{http://www.ibict.br/schema/}identifier'):
			id = indentifier.text[23:]


		for autor in root.findall('{http://www.ibict.br/schema/}Autor'):
			info = autor.getchildren()
			for n,i in enumerate(info):
				if not i.getchildren():
					if i.tag == '{http://www.ibict.br/schema/}Nome':
						array[0] = i.text.encode('utf-8')
					elif i.tag == '{http://www.ibict.br/schema/}Lattes':
						array[2] = i.text.encode('utf-8')
					elif i.tag == '{http://www.ibict.br/schema/}CPF':
						array[1] = i.text.encode('utf-8')
					elif i.tag != '{http://www.ibict.br/schema/}Citacao':
						tags.append(i.tag)
		
		for titulo in root.findall('{http://www.ibict.br/schema/}Titulo'):
			print titulo.attrib , titulo.tag , titulo.text
			if (titulo.attrib == {'Idioma': 'pt'} or titulo.attrib == {'Idioma': 'por'}):
				if titulo.text != None:
					array[3] = titulo.text.encode('utf-8')

		for data in root.findall('{http://www.ibict.br/schema/}DataDefesa'):
			if data.text != None:
				array[5] = data.text.encode('utf-8')

		for dados in root.findall('{http://www.ibict.br/schema/}InstituicaoDefesa'):
			info = dados.getchildren()
			for i in info:
				if i.tag == '{http://www.ibict.br/schema/}Nome':
					if i.text != None:
						array[6] = i.text.encode('utf-8')
				if i.tag == '{http://www.ibict.br/schema/}Programa':
					for i in i:
						if i.text != None:
							array[4] = i.text.encode('utf-8')

		for j,contribuidor in enumerate(root.findall('{http://www.ibict.br/schema/}Contribuidor')):
			contrib.append(['' for x in range(0,3)])
			info = contribuidor.getchildren()
			for n,i in enumerate(info):
				if i.text != None:
					if i.tag == '{http://www.ibict.br/schema/}Nome':
						contrib[j][0] = i.text.encode('utf-8')
					elif i.tag == '{http://www.ibict.br/schema/}Lattes':
						contrib[j][2] = i.text.encode('utf-8')
					elif i.tag == '{http://www.ibict.br/schema/}CPF':
						contrib[j][1] = i.text.encode('utf-8')
		array[7] = id
		for i in contrib:
			for j in i:
				array.append(j)


		escrever_arquivo(array)