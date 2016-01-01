import MySQLdb
import configurer, logger

def initialize():
	global online, database, cursor
	if online:
		logger.logger.warn('REINITIALIZATION')
		return
	database = MySQLdb.connect(configurer.host, configurer.user, db = configurer.database, charset = 'utf8')
	cursor = database.cursor()
	online = True
	logger.logger.info('INITIALIZATION')

def execute(query, arguments = None):
	global online, cursor
	if not online:
		logger.logger.warn('UNINITIALIZED')
		logger.logger.warn('INPUT QUERY <' + query + '>')
		logger.logger.warn('INPUT ARGUMENTS <' + str(arguments) + '>')
		return
	logger.logger.log(logger.details, 'INPUT QUERY <' + query + '>')
	logger.logger.log(logger.details, 'INPUT ARGUMENTS <' + str(arguments) + '>')
	cursor.execute(query, arguments)

def executemany(query, arguments):
	global online, cursor
	if not online:
		logger.logger.warn('UNINITIALIZED')
		logger.logger.warn('INPUT QUERY <' + query + '>')
		logger.logger.warn('INPUT ARGUMENTS COUNT <' + str(len(arguments)) + '>')
		return
	logger.logger.log(logger.details, 'INPUT QUERY <' + query + '>')
	logger.logger.log(logger.details, 'INPUT ARGUMENTS COUNT <' + str(len(arguments)) + '>')
	cursor.executemany(query, arguments)

def fetchall():
	global online, cursor
	if not online:
		logger.logger.warn('UNINITIALIZED')
		return
	returnvalue = cursor.fetchall()
	logger.logger.log(logger.details, 'CONNECTOR FETCH COUNT <' + str(len(returnvalue)) + '>')
	return returnvalue

def terminate():
	global online, database, cursor
	if not online:
		logger.logger.warn('UNINITIALIZED')
		return
	online = False
	cursor.close()
	database.commit()
	logger.logger.info('TERMINATION')

online = False
database = None
cursor = None
logger.logger.info('CREATION')
