import logger, connector

def query(query, arguments):
	logger.logger.debug('INPUT QUERY <' + query + '>')
	logger.logger.debug('INPUT ARGUMENTS <' + str(arguments) + '>')
	connector.execute(query, arguments)
	returnvalue = connector.fetchall()
	logger.logger.log(logger.details, 'OUTPUT COUNT <' + str(len(returnvalue)) + '>')
	return returnvalue

def smartquery(smartquery, arguments):
	global simplequeries, complexqueries
	logger.logger.debug('INPUT QUERY <' + smartquery + '>')
	logger.logger.debug('INPUT ARGUMENTS <' + str(arguments) + '>')
	if smartquery in simplequeries:
		returnvalue = query(simplequeries[smartquery], arguments)
		logger.logger.info('OUTPUT COUNT <' + str(len(returnvalue)) + '>')
		return returnvalue
	if smartquery in complexqueries:
		returnvalue = globals()[smartquery](arguments)
		logger.logger.info('OUTPUT COUNT <' + str(len(returnvalue)) + '>')
		return returnvalue
	logger.logger.warn('INVALID INPUT')

def getsentencesandannotationsbyunitname(arguments):
	global simplequeries
	logger.logger.debug('INPUT <' + str(arguments) + '>')
	sentences = list()
	annotations = list()
	units = query(simplequeries['getunitbyname'], arguments)
	for unit in units:
		embodies = query(simplequeries['getembodyingsentencesbyunitID'], (unit[0], ))
		for embody in embodies:
			sentences.append(query(simplequeries['getsentencebyID'], (embody[0], )))
			annotations.append(query(simplequeries['getannotationsbysentenceID'], (embody[0], )))
	logger.logger.info('OUTPUT SENTENCE COUNT <' + str(len(sentences)) + '>')
	logger.logger.info('OUTPUT ANNOTATIONS COUNT <' + str(len(annotations)) + '>')
	return sentences, annotations

def getsentencesandannotationsbyunitnameandPOS(arguments):
	global simplequeries
	logger.logger.debug('INPUT <' + str(arguments) + '>')
	sentences = list()
	annotations = list()
	units = query(simplequeries['getunitbynameandPOS'], arguments)
	for unit in units:
		embodies = query(simplequeries['getembodyingsentencesbyunitID'], (unit[0], ))
		for embody in embodies:
			sentences.append(query(simplequeries['getsentencebyID'], (embody[0], )))
			annotations.append(query(simplequeries['getannotationsbysentenceID'], (embody[0], )))
	logger.logger.info('OUTPUT SENTENCE COUNT <' + str(len(sentences)) + '>')
	logger.logger.info('OUTPUT ANNOTATIONS COUNT <' + str(len(annotations)) + '>')
	return sentences, annotations

def getsentencesandannotationsbyframeID(arguments):
	global simplequeries
	logger.logger.debug('INPUT <' + str(arguments) + '>')
	sentences = list()
	annotations = list()
	units = query(simplequeries['getevokingunitsbyframeID'], arguments)
	for unit in units:
		embodies = query(simplequeries['getembodyingsentencesbyunitID'], (unit[0], ))
		for embody in embodies:
			sentences.append(query(simplequeries['getsentencebyID'], (embody[0], )))
			annotations.append(query(simplequeries['getannotationsbysentenceID'], (embody[0], )))
	logger.logger.info('OUTPUT SENTENCE COUNT <' + str(len(sentences)) + '>')
	logger.logger.info('OUTPUT ANNOTATIONS COUNT <' + str(len(annotations)) + '>')
	return sentences, annotations

simplequeries = {
	'createframe': 'CREATE TABLE IF NOT EXISTS Frame ( ID INT PRIMARY KEY, name CHAR(40) )',
	'createelement': 'CREATE TABLE IF NOT EXISTS Element ( ID INT PRIMARY KEY, FrameID INT, name CHAR(30), type CHAR(20), FOREIGN KEY(FrameID) REFERENCES Frame(ID) )',
	'createunit': 'CREATE TABLE IF NOT EXISTS Unit ( ID INT PRIMARY KEY, name CHAR(40), POS CHAR(10) )',
	'createsentence': 'CREATE TABLE IF NOT EXISTS Sentence ( ID INT PRIMARY KEY, text TEXT(1200) )',
	'createannotation': 'CREATE TABLE IF NOT EXISTS Annotation ( SentenceID INT, start INT, end INT, ElementID INT, Gfunction CHAR(20), Ptype CHAR(20), PRIMARY KEY(SentenceID, start, end), FOREIGN KEY(SentenceID) REFERENCES Sentence(ID), FOREIGN KEY(ElementID) REFERENCES Element(ID))',
	'createevokes': 'CREATE TABLE IF NOT EXISTS Evokes ( FrameID INT, UnitID INT, PRIMARY KEY(FrameID, UnitID), FOREIGN KEY(FrameID) REFERENCES Frame(ID), FOREIGN KEY(UnitID) REFERENCES Unit(ID) )',
	'createrelates': 'CREATE TABLE IF NOT EXISTS Relates ( FrameIDfrom INT, Framenameto CHAR(40), type CHAR(30), PRIMARY KEY(FrameIDfrom, Framenameto), FOREIGN KEY(FrameIDfrom) REFERENCES Frame(ID) )',
	'createembodies': 'CREATE TABLE IF NOT EXISTS Embodies ( SentenceID INT, UnitID INT, PRIMARY KEY(SentenceID, UnitID), FOREIGN KEY(SentenceID) REFERENCES Sentence(ID), FOREIGN KEY(UnitID) REFERENCES Unit(ID) )',
	'insertframe': 'INSERT IGNORE INTO Frame (ID, name) VALUES (%s, %s)',
	'insertelement': 'INSERT IGNORE INTO Element (ID, FrameID, name, type) VALUES (%s, %s, %s, %s)',
	'insertunit': 'INSERT IGNORE INTO Unit (ID, name, POS) VALUES (%s, %s, %s)',
	'insertsentence': 'INSERT IGNORE INTO Sentence (ID, text) VALUES (%s, %s)',
	'insertannotation': 'INSERT IGNORE INTO Annotation (SentenceID, start, end, ElementID, Gfunction, Ptype) VALUES (%s, %s, %s, %s, %s, %s)',
	'insertevokes': 'INSERT IGNORE INTO Evokes (FrameID, UnitID) VALUES (%s, %s)',
	'insertrelates': 'INSERT IGNORE INTO Relates (FrameIDfrom, Framenameto, type) VALUES (%s, %s, %s)',
	'insertembodies': 'INSERT IGNORE INTO Embodies (SentenceID, UnitID) VALUES (%s, %s)',
	'getframebyID': 'SELECT ID, name FROM Frame WHERE ID = %s',
	'getframebyname': 'SELECT ID, name FROM Frame WHERE name = %s',
	'getelementbyID': 'SELECT ID, frameID, name, type FROM Element WHERE ID = %s',
	'getelementsbyframeID': 'SELECT ID, frameID, name, type FROM Element WHERE frameID = %s',
	'getunitbyID': 'SELECT ID, name, POS FROM Unit WHERE ID = %s',
	'getunitbyname': 'SELECT ID, name, POS FROM Unit WHERE name = %s',
	'getunitbynameandPOS': 'SELECT ID, name, POS FROM Unit WHERE name = %s AND POS = %s',
	'getsentencebyID': 'SELECT ID, text FROM Sentence WHERE ID = %s',
	'getannotationsbysentenceID': 'SELECT SentenceID, start, end, ElementID, Gfunction, Ptype FROM Annotation WHERE SentenceID = %s',
	'getevokedframesbyunitID': 'SELECT FrameID, UnitID FROM Evokes WHERE UnitID = %s',
	'getevokedframesbyunitname': 'SELECT FrameID, UnitID FROM Evokes, Unit WHERE UnitID = ID AND name = %s',
	'getevokedframesbyunitnameandPOS': 'SELECT FrameID, UnitID FROM Evokes, Unit WHERE UnitID = ID AND name = %s AND POS = %s',
	'getevokingunitsbyframeID': 'SELECT FrameID, UnitID FROM Evokes WHERE FrameID = %s',
	'getembodiedunitsbysentenceID': 'SELECT SentenceID, UnitID FROM Embodies WHERE SentenceID = %s',
	'getembodyingsentencesbyunitID': 'SELECT SentenceID, UnitID FROM Embodies WHERE UnitID = %s',
	'getrelatedframesbytoID': 'SELECT FrameIDfrom, Framenameto, type FROM Relates, Frame WHERE Framenameto = name AND ID = %s',
	'getrelatedframesbyfromID': 'SELECT FrameIDfrom, Framenameto, type FROM Relates WHERE FrameIDfrom = %s',
	'getrelatedframesbytoname': 'SELECT FrameIDfrom, Framenameto, type FROM Relates WHERE Framenameto = %s',
	'getrelatedframesbyfromname': 'SELECT FrameIDfrom, Framenameto, type FROM Relates, Frame WHERE FrameIDfrom = ID AND name = %s',
	'getframesbysentenceID': 'SELECT ID, name from Frame WHERE ID IN (SELECT FrameID FROM Evokes WHERE UnitID IN (SELECT UnitID FROM Embodies WHERE SentenceID = %s))'
}
complexqueries = [
	'getsentencesandannotationsbyunitname',
	'getsentencesandannotationsbyunitnameandPOS',
	'getsentencesandannotationsbyframeID'
]
logger.logger.info('CREATION')
