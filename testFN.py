import os, xml.etree.ElementTree as ET

framenet = '{http://framenet.icsi.berkeley.edu}'
directory = '../../Downloads/framenet_v15/frame/'

frames = list()
frameelements = list()
lexicalunits = list()

for filename in os.listdir(directory):
	if filename.split('.')[-1] != 'xml':
		continue

	tree = ET.parse(directory + filename)
	root = tree.getroot()
	FID = int(root.attrib.get('ID'))
	Fname = root.attrib.get('name')
	frameData = (FID, Fname) 
	frames.append(frameData)

	for child in root.iter():
		if child.tag == framenet + 'FE':
			FEID = child.attrib.get('ID')
			FEname = child.attrib.get('name')
			FEcoretype = child.attrib.get('coreType')
			FEabbrev = child.attrib.get('abbrev')
			FEdata = (FEID, FEname, FID, FEcoretype, FEabbrev)
			frameelements.append(FEdata)

		if child.tag == framenet + 'lexUnit':
			LUID = child.attrib.get('ID')
			LUname = child.attrib.get('name')
			LUPOS = child.attrib.get('POS')
			for subchild in child:
				if subchild.tag == framenet + 'sentenceCount':
					LUannotated = int(subchild.attrib.get('annotated'))
			LUdata = (LUID, LUname, FID, LUPOS, LUannotated)
			lexicalunits.append(LUdata)
