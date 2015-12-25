import jpype
import configurer, logger

def addclasspath(classpath):
	global classpathlist
	classpathlist.append(classpath)
	logger.logger.debug('PYPER CLASSPATH ADDITION <' + classpath + '>')

def initialize():
	global online
	if online:
		logger.logger.warn('PYPER REINITIALIZATION')
	jpype.startJVM(configurer.libjvm, '-Djava.class.path=%s' %(':'.join(classpathlist)))
	online = True
	logger.logger.info('PYPER INITIALIZATION')

def terminate():
	global online, logger
	if not online:
		logger.logger.warn('UNINITIALIZED PYPER TERMINATION')
		return
	jpype.shutdownJVM()
	online = False
	logger.logger.info('PYPER TERMINATION')

classpathlist = ['*']
online = False
logger.logger.info('PYPER CREATION')
