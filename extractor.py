class Extractor:
	def __init__(self, debug = True):
		self.debug = debug
		self.online = False
		self.resetextracts()

	def initialize(self, host, user, password):
		import MySQLdb
		if not self.online:
			self.database = MySQLdb.connect(host, user, password, 'Jarvis', charset = 'utf8')
			self.cursor = self.database.cursor()
		self.online = True
		if self.debug:
			print '[DEBUG: INITIALIZED DATABASE]'

	def resetextracts(self):
		self.frame = list()
		self.element = list()
		self.relates = list()
		self.unit = list()
		self.sentence = list()
		self.annotation = list()
		self.evokes = list()
		self.embodies = list()

	def createdatabase(self):
		import warnings
		warnings.filterwarnings('ignore')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Frame ( ID INT PRIMARY KEY, name CHAR(40) )')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Element ( ID INT PRIMARY KEY, FrameID INT, name CHAR(30), type CHAR(20), FOREIGN KEY(FrameID) REFERENCES Frame(ID) )')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Unit ( ID INT PRIMARY KEY, name CHAR(40), POS CHAR(10) )')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Sentence ( ID INT PRIMARY KEY, text TEXT(1200) )')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Annotation ( SentenceID INT, start INT, end INT, ElementID INT, Gfunction CHAR(20), Ptype CHAR(20), PRIMARY KEY(SentenceID, start, end), FOREIGN KEY(SentenceID) REFERENCES Sentence(ID), FOREIGN KEY(ElementID) REFERENCES Element(ID))')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Evokes ( FrameID INT, UnitID INT, PRIMARY KEY(FrameID, UnitID), FOREIGN KEY(FrameID) REFERENCES Frame(ID), FOREIGN KEY(UnitID) REFERENCES Unit(ID) )')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Relates ( FrameIDfrom INT, Framenameto CHAR(40), type CHAR(30), PRIMARY KEY(FrameIDfrom, Framenameto), FOREIGN KEY(FrameIDfrom) REFERENCES Frame(ID) )')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS Embodies ( SentenceID INT, UnitID INT, PRIMARY KEY(SentenceID, UnitID), FOREIGN KEY(SentenceID) REFERENCES Sentence(ID), FOREIGN KEY(UnitID) REFERENCES Unit(ID) )')
		warnings.resetwarnings()
		if self.debug:
			print '[DEBUG: CREATED DATABASE]'

	def populatedatabase(self):
		import warnings
		warnings.filterwarnings('ignore')
		if self.frame:
			self.cursor.executemany('INSERT IGNORE INTO Frame (ID, name) VALUES (%s, %s)', self.frame)
		if self.element:
			self.cursor.executemany('INSERT IGNORE INTO Element (ID, FrameID, name, type) VALUES (%s, %s, %s, %s)', self.element)
		if self.unit:
			self.cursor.executemany('INSERT IGNORE INTO Unit (ID, name, POS) VALUES (%s, %s, %s)', self.unit)
		if self.sentence:
			self.cursor.executemany('INSERT IGNORE INTO Sentence (ID, text) VALUES (%s, %s)', self.sentence)
		if self.annotation:
			self.cursor.executemany('INSERT IGNORE INTO Annotation (SentenceID, start, end, ElementID, Gfunction, Ptype) VALUES (%s, %s, %s, %s, %s, %s)', self.annotation)
		if self.evokes:
			self.cursor.executemany('INSERT IGNORE INTO Evokes (FrameID, UnitID) VALUES (%s, %s)', self.evokes)
		if self.relates:
			self.cursor.executemany('INSERT IGNORE INTO Relates (FrameIDfrom, Framenameto, type) VALUES (%s, %s, %s)', self.relates)
		if self.embodies:
			self.cursor.executemany('INSERT IGNORE INTO Embodies (SentenceID, UnitID) VALUES (%s, %s)', self.embodies)
		warnings.resetwarnings()
		if self.debug:
			print '[DEBUG: POPULATED DATABASE]'

	def extractframes(self, directory, prefix = '{http://framenet.icsi.berkeley.edu}'):
		import os, xml.etree.ElementTree
		for filename in os.listdir(directory):
			if filename.split('.')[-1] != 'xml':
				continue
			tree = xml.etree.ElementTree.parse(directory + filename)
			root = tree.getroot()
			FID = int(root.attrib.get('ID'))
			Fname = root.attrib.get('name')
			self.frame.append((FID, Fname))
			for child in root:
				if child.tag == prefix + 'FE':
					FEID = int(child.attrib.get('ID'))
					FEname = child.attrib.get('name')
					FEcoretype = child.attrib.get('coreType')
					self.element.append((FEID, FID, FEname, FEcoretype))
				elif child.tag == prefix + 'frameRelation':
					FRtype = child.attrib.get('type')
					FRtext = None
					for subchild in child:
						if subchild.tag == prefix + 'relatedFrame':
							FRtext = subchild.text
					if FRtext is not None:
						self.relates.append((FID, FRtext, FRtype))
		if self.debug:
			print '[DEBUG: EXTRACTED', len(self.frame), 'FRAME ENTITIES]'
			print '[DEBUG: EXTRACTED', len(self.element), 'ELEMENT ENTITIES]'
			print '[DEBUG: EXTRACTED', len(self.relates), 'RELATES RELATIONS]'
		return self.frame, self.element, self.relates

	def extractunits(self, directory, prefix = '{http://framenet.icsi.berkeley.edu}'):
		import os, xml.etree.ElementTree
		for filename in os.listdir(directory):
			if filename.split('.')[-1] != 'xml':
				continue
			tree = xml.etree.ElementTree.parse(directory + filename)
			root = tree.getroot()
			LUID = int(root.attrib.get('ID'))
			FID = int(root.attrib.get('frameID'))
			self.evokes.append((FID, LUID))
			for child in root:
				if child.tag == prefix + 'lexeme':
					LPOS = child.attrib.get('POS')
					Lname = child.attrib.get('name')
					self.unit.append((LUID, Lname, LPOS))
				elif child.tag == prefix + 'subCorpus':
					for subchild in child:
						if subchild.tag == prefix + 'sentence':
							SID = int(subchild.attrib.get('ID'))
							self.embodies.append((SID, LUID))
							annotateFE = dict()
							annotateGF = dict()
							annotatePT = dict()
							for subsubchild in subchild:
								if subsubchild.tag == prefix + 'text':
									text = subsubchild.text
									self.sentence.append((SID, text))
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
									self.annotation.append((SID, indices[0], indices[1], annotateFE[indices], annotateGF[indices], annotatePT[indices]))
		if self.debug:
			print '[DEBUG: EXTRACTED', len(self.unit), 'UNIT ENTITIES]'
			print '[DEBUG: EXTRACTED', len(self.sentence), 'SENTENCE ENTITIES]'
			print '[DEBUG: EXTRACTED', len(self.annotation), 'ANNOTATION ENTITIES]'
			print '[DEBUG: EXTRACTED', len(self.evokes), 'EVOKES RELATIONS]'
			print '[DEBUG: EXTRACTED', len(self.embodies), 'EMBODIES RELATIONS]'
		return self.unit, self.sentence, self.annotation, self.evokes, self.embodies

	def terminate(self):
		self.cursor.close()
		self.database.commit()
		if self.debug:
			print '[DEBUG: TERMINATED DATABASE]'
