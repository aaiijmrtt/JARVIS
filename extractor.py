import os, xml.etree.ElementTree, warnings
import logger, connector, querier

def resetextracts():
	global frame, element, relates, unit, sentence, annotation, evokes, embodies
	frame = list()
	element = list()
	relates = list()
	unit = list()
	sentence = list()
	annotation = list()
	evokes = list()
	embodies = list()
	logger.logger.info('RESET')

def createdatabase():
	global tablenames
	warnings.filterwarnings('ignore')
	for table in tablenames:
		connector.execute(querier.simplequeries['create' + table])
		logger.logger.info(table.upper() + ' TABLE CREATION')
	warnings.resetwarnings()
	logger.logger.info('DATABASE CREATION')

def populatedatabase():
	global tablenames
	warnings.filterwarnings('ignore')
	for table in tablenames:
		if globals()[table]:
			connector.executemany(querier.simplequeries['insert' + table], globals()[table])
			logger.logger.info(table.upper() + ' TABLE POPULATION COUNT <' + str(len(globals()[table])) + '>')
	warnings.resetwarnings()
	logger.logger.info('DATABASE POPULATION')

def extractframes(directory, prefix = '{http://framenet.icsi.berkeley.edu}'):
	global frame, element, relates
	for filename in os.listdir(directory):
		if filename.split('.')[-1] != 'xml':
			continue
		tree = xml.etree.ElementTree.parse(directory + filename)
		root = tree.getroot()
		FID = int(root.attrib.get('ID'))
		Fname = root.attrib.get('name')
		frame.append((FID, Fname))
		for child in root:
			if child.tag == prefix + 'FE':
				FEID = int(child.attrib.get('ID'))
				FEname = child.attrib.get('name')
				FEcoretype = child.attrib.get('coreType')
				element.append((FEID, FID, FEname, FEcoretype))
			elif child.tag == prefix + 'frameRelation':
				FRtype = child.attrib.get('type')
				for subchild in child:
					if subchild.tag == prefix + 'relatedFrame':
						FRtext = subchild.text
						relates.append((FID, FRtext, FRtype))
	logger.logger.debug('OUTPUT FRAME ENTITIES COUNT <' + str(len(frame)) + '>')
	logger.logger.debug('OUTPUT ELEMENT ENTITIES COUNT <' + str(len(element)) + '>')
	logger.logger.debug('OUTPUT RELATES RELATIONS COUNT <' + str(len(relates)) + '>')
	logger.logger.info('FRAME EXTRACTION')
	return frame, element, relates

def extractunits(directory, prefix = '{http://framenet.icsi.berkeley.edu}'):
	global unit, sentence, annotation, evokes, embodies
	for filename in os.listdir(directory):
		if filename.split('.')[-1] != 'xml':
			continue
		tree = xml.etree.ElementTree.parse(directory + filename)
		root = tree.getroot()
		LUID = int(root.attrib.get('ID'))
		FID = int(root.attrib.get('frameID'))
		evokes.append((FID, LUID))
		for child in root:
			if child.tag == prefix + 'lexeme':
				LPOS = child.attrib.get('POS')
				Lname = child.attrib.get('name')
				unit.append((LUID, Lname, LPOS))
			elif child.tag == prefix + 'subCorpus':
				for subchild in child:
					if subchild.tag == prefix + 'sentence':
						SID = int(subchild.attrib.get('ID'))
						embodies.append((SID, LUID))
						annotateFE = dict()
						annotateGF = dict()
						annotatePT = dict()
						for subsubchild in subchild:
							if subsubchild.tag == prefix + 'text':
								text = subsubchild.text
								sentence.append((SID, text))
							elif subsubchild.tag == prefix + 'annotationSet':
								for subsubsubchild in subsubchild:
									if subsubsubchild.tag == prefix + 'layer':
										name = subsubsubchild.attrib.get('name')
										if name == 'FE':
											for subsubsubsubchild in subsubsubchild:
												if subsubsubsubchild.tag == prefix + 'label':
													start = int(subsubsubsubchild.attrib.get('start', -1))
													end = int(subsubsubsubchild.attrib.get('end', -1))
													FEID = int(subsubsubsubchild.attrib.get('feID'))
													annotateFE[(start, end)] = FEID
										elif name == 'GF':
											for subsubsubsubchild in subsubsubchild:
												if subsubsubsubchild.tag == prefix + 'label':
													start = int(subsubsubsubchild.attrib.get('start', -1))
													end = int(subsubsubsubchild.attrib.get('end', -1))
													GFname = subsubsubsubchild.attrib.get('name')
													annotateGF[(start, end)] = GFname
										elif name == 'PT':
											for subsubsubsubchild in subsubsubchild:
												if subsubsubsubchild.tag == prefix + 'label':
													start = int(subsubsubsubchild.attrib.get('start', -1))
													end = int(subsubsubsubchild.attrib.get('end', -1))
													PTname = subsubsubsubchild.attrib.get('name')
													annotatePT[(start, end)] = PTname
						for indices in annotateFE:
							if indices[0] != -1 and indices[1] != -1 and indices in annotateGF and indices in annotatePT:
								annotation.append((SID, indices[0], indices[1], annotateFE[indices], annotateGF[indices], annotatePT[indices]))
	logger.logger.debug('OUTPUT UNIT ENTITIES COUNT <' + str(len(unit)) + '>')
	logger.logger.debug('OUTPUT SENTENCE ENTITIES COUNT <' + str(len(sentence)) + '>')
	logger.logger.debug('OUTPUT ANNOTATION ENTITIES COUNT <' + str(len(annotation)) + '>')
	logger.logger.debug('OUTPUT EVOKES RELATIONS COUNT <' + str(len(evokes)) + '>')
	logger.logger.debug('OUTPUT EMBODIES RELATIONS COUNT <' + str(len(embodies)) + '>')
	logger.logger.info('UNIT EXTRACTION')
	return unit, sentence, annotation, evokes, embodies

frame = list()
element = list()
relates = list()
unit = list()
sentence = list()
annotation = list()
evokes = list()
embodies = list()

tablenames = ['frame', 'element', 'unit', 'sentence', 'annotation', 'evokes', 'relates', 'embodies']
logger.logger.info('CREATION')
