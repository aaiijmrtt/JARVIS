import os, xml.etree.ElementTree as ET

framenet = '{http://framenet.icsi.berkeley.edu}'
directory = '../../Downloads/framenet_v15/lu/'

sentences = dict()
annotations = list()

for filename in os.listdir(directory):
	if filename.split('.')[-1] != 'xml':
		continue

	tree = ET.parse(directory + filename)
	root = tree.getroot()

	FID = int(root.attrib.get('frameID'))
	LUID = int(root.attrib.get('ID'))
	LUname = root.attrib.get('name')
	LUPOS = root.attrib.get('POS')

	for child in root.iter():
		if child.tag == framenet + 'sentence':
			annotation = dict()
			SENTENCEtree = child
			SENTENCEID = int(SENTENCEtree.attrib.get('ID'))
			SENTENCEtext = ''

			for sentChild in SENTENCEtree.iter():
				if sentChild.tag == framenet + 'text':
					SENTENCEtext = sentChild.text

				elif sentChild.tag == framenet + 'layer':
					LAYER = sentChild
					LAYERname = LAYER.attrib.get('name')

					for LABEL in LAYER:
						if LABEL.tag != framenet + 'label':
							continue

						LABELstart = int(LABEL.attrib.get('start', -1))
						LABELend = int(LABEL.attrib.get('end', -1))
						LABELname = LABEL.attrib.get('name')
						LABELID = int(LABEL.attrib.get('feID', -1))

						if LABELstart == -1 or LABELend == -1:
							continue
						elif (LABELstart, LABELend) not in annotation:
							annotation[(LABELstart, LABELend)] = dict()

						annotation[(LABELstart, LABELend)][LAYERname] = (LABELname, LABELID)
			sentences[SENTENCEID] = SENTENCEtext

			for key in annotation:
				ann = annotation[key]
				if ann.get('FE', None) == None:
					continue
				INDEXstart = key[0]
				INDEXend = key[1]
				FEname = ann.get('FE')[0]
				FEID = ann.get('FE')[1]
				PTname = ann.get('PT', ('', 0))[0]
				GFname = ann.get('GF', ('', 0))[0]
				COUNT = len(SENTENCEtext[INDEXstart: INDEXend + 1].strip().split())

				FEannotation = (FID, LUname, LUID, FEID, FEname, PTname, GFname, SENTENCEID, INDEXstart, INDEXend, COUNT)
				annotations.append(FEannotation)
