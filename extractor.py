import os, xml.etree.ElementTree, warnings
import MySQLdb
import configurer, logger

def initialize():
	global online, database, cursor
	if online:
		logger.logger.warn('EXTRACTOR REINITIALIZATION')
		return
	database = MySQLdb.connect(configurer.host, configurer.user, db = configurer.database, charset = 'utf8')
	cursor = database.cursor()
	online = True
	logger.logger.info('EXTRACTOR INITIALIZATION')

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
	logger.logger.info('EXTRACTS RESET')

def createdatabase():
	global cursor
	warnings.filterwarnings('ignore')
	cursor.execute('CREATE TABLE IF NOT EXISTS Frame ( ID INT PRIMARY KEY, name CHAR(40) )')
	cursor.execute('CREATE TABLE IF NOT EXISTS Element ( ID INT PRIMARY KEY, FrameID INT, name CHAR(30), type CHAR(20), FOREIGN KEY(FrameID) REFERENCES Frame(ID) )')
	cursor.execute('CREATE TABLE IF NOT EXISTS Unit ( ID INT PRIMARY KEY, name CHAR(40), POS CHAR(10) )')
	cursor.execute('CREATE TABLE IF NOT EXISTS Sentence ( ID INT PRIMARY KEY, text TEXT(1200) )')
	cursor.execute('CREATE TABLE IF NOT EXISTS Annotation ( SentenceID INT, start INT, end INT, ElementID INT, Gfunction CHAR(20), Ptype CHAR(20), PRIMARY KEY(SentenceID, start, end), FOREIGN KEY(SentenceID) REFERENCES Sentence(ID), FOREIGN KEY(ElementID) REFERENCES Element(ID))')
	cursor.execute('CREATE TABLE IF NOT EXISTS Evokes ( FrameID INT, UnitID INT, PRIMARY KEY(FrameID, UnitID), FOREIGN KEY(FrameID) REFERENCES Frame(ID), FOREIGN KEY(UnitID) REFERENCES Unit(ID) )')
	cursor.execute('CREATE TABLE IF NOT EXISTS Relates ( FrameIDfrom INT, Framenameto CHAR(40), type CHAR(30), PRIMARY KEY(FrameIDfrom, Framenameto), FOREIGN KEY(FrameIDfrom) REFERENCES Frame(ID) )')
	cursor.execute('CREATE TABLE IF NOT EXISTS Embodies ( SentenceID INT, UnitID INT, PRIMARY KEY(SentenceID, UnitID), FOREIGN KEY(SentenceID) REFERENCES Sentence(ID), FOREIGN KEY(UnitID) REFERENCES Unit(ID) )')
	warnings.resetwarnings()
	logger.logger.info('DATABASE CREATION')

def populatedatabase():
	global cursor, frame, element, unit, sentence, annotation, evokes, relates, embodies
	warnings.filterwarnings('ignore')
	if frame:
		cursor.executemany('INSERT IGNORE INTO Frame (ID, name) VALUES (%s, %s)', frame)
		logger.logger.info('FRAME ENTITIES POPULATION COUNT <' + str(len(frame)) + '>')
	if element:
		cursor.executemany('INSERT IGNORE INTO Element (ID, FrameID, name, type) VALUES (%s, %s, %s, %s)', element)
		logger.logger.debug('ELEMENT ENTITIES POPULATION COUNT <' + str(len(element)) + '>')
	if unit:
		cursor.executemany('INSERT IGNORE INTO Unit (ID, name, POS) VALUES (%s, %s, %s)', unit)
		logger.logger.debug('UNIT ENTITIES POPULATION COUNT <' + str(len(unit)) + '>')
	if sentence:
		cursor.executemany('INSERT IGNORE INTO Sentence (ID, text) VALUES (%s, %s)', sentence)
		logger.logger.debug('SENTENCE ENTITIES POPULATION COUNT <' + str(len(sentence)) + '>')
	if annotation:
		cursor.executemany('INSERT IGNORE INTO Annotation (SentenceID, start, end, ElementID, Gfunction, Ptype) VALUES (%s, %s, %s, %s, %s, %s)', annotation)
		logger.logger.debug('ANNOTATION ENTITIES POPULATION COUNT <' + str(len(annotation)) + '>')
	if evokes:
		cursor.executemany('INSERT IGNORE INTO Evokes (FrameID, UnitID) VALUES (%s, %s)', evokes)
		logger.logger.debug('EVOKES RELATIONS POPULATION COUNT <' + str(len(evokes)) + '>')
	if relates:
		cursor.executemany('INSERT IGNORE INTO Relates (FrameIDfrom, Framenameto, type) VALUES (%s, %s, %s)', relates)
		logger.logger.debug('RELATES RELATIONS POPULATION COUNT <' + str(len(relates)) + '>')
	if embodies:
		cursor.executemany('INSERT IGNORE INTO Embodies (SentenceID, UnitID) VALUES (%s, %s)', embodies)
		logger.logger.debug('EMBODIES RELATIONS POPULATION COUNT <' + str(len(embodies)) + '>')
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
				FRtext = None
				for subchild in child:
					if subchild.tag == prefix + 'relatedFrame':
						FRtext = subchild.text
				if FRtext is not None:
					relates.append((FID, FRtext, FRtype))
	logger.logger.debug('FRAME ENTITIES EXTRACTION COUNT <' + str(len(frame)) + '>')
	logger.logger.debug('ELEMENT ENTITIES EXTRACTION COUNT <' + str(len(element)) + '>')
	logger.logger.debug('RELATES RELATIONS EXTRACTION COUNT <' + str(len(relates)) + '>')
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
	logger.logger.debug('UNIT ENTITIES EXTRACTION COUNT <' + str(len(unit)) + '>')
	logger.logger.debug('SENTENCE ENTITIES EXTRACTION COUNT <' + str(len(sentence)) + '>')
	logger.logger.debug('ANNOTATION ENTITIES EXTRACTION COUNT <' + str(len(annotation)) + '>')
	logger.logger.debug('EVOKES RELATIONS EXTRACTION COUNT <' + str(len(evokes)) + '>')
	logger.logger.debug('EMBODIES RELATIONS EXTRACTION COUNT <' + str(len(embodies)) + '>')
	logger.logger.info('UNIT EXTRACTION')
	return unit, sentence, annotation, evokes, embodies

def terminate():
	global online, cursor, database
	if not online:
		logger.logger.warn('UNINITIALIZED EXTRACTOR TERMINATION')
		return
	online = False
	cursor.close()
	database.commit()
	logger.logger.info('EXTRACTOR TERMINATION')

online = False
frame = None
element = None
relates = None
unit = None
sentence = None
annotation = None
evokes = None
embodies = None
resetextracts()
logger.logger.info('EXTRACTOR CREATION')
