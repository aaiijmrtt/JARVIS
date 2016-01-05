import jpype
import configurer, logger

def addclasspath(classpath):
	global classpathlist
	logger.logger.debug('INPUT <' + classpath + '>')
	classpathlist.append(classpath)

def initialize():
	global online
	if online:
		logger.logger.warn('REINITIALIZATION')
		return
	jpype.startJVM(configurer.libjvm, '-Djava.class.path=%s' %(':'.join(classpathlist)))
	online = True
	logger.logger.info('INITIALIZATION')

def terminate():
	global online
	if not online:
		logger.logger.warn('UNINITIALIZED')
		return
	jpype.shutdownJVM()
	online = False
	logger.logger.info('TERMINATION')

classpathlist = ['*']
online = False
logger.logger.info('CREATION')
