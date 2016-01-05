import jpype
import configurer, logger, pyper

def initialize():
	global online, configuration, recognizer
	if online:
		logger.logger.warn('REINITIALIZATION')
		return
	configuration = jpype.JClass('edu.cmu.sphinx.api.Configuration')()
	configuration.setAcousticModelPath("resource:/edu/cmu/sphinx/models/en-us/en-us")
	configuration.setDictionaryPath("resource:/edu/cmu/sphinx/models/en-us/cmudict-en-us.dict")
	configuration.setLanguageModelPath("resource:/edu/cmu/sphinx/models/en-us/en-us.lm.bin")
	recognizer = jpype.JClass('edu.cmu.sphinx.api.LiveSpeechRecognizer')(configuration)
	online = True
	logger.logger.info('INITIALIZATION')

def listen():
	global online, recognizer
	if not online:
		logger.logger.warn('UNINITIALIZED')
		return
	recognizer.startRecognition(False)
	logger.logger.info('AWAITING INPUT')
	result = recognizer.getResult()
	returnhypothesis = result.getHypothesis()
	recognizer.stopRecognition()
	logger.logger.info('OUTPUT <' + returnhypothesis + '>')
	return returnhypothesis

def terminate():
	global online
	if not online:
		logger.logger.warn('UNINITIALIZED')
		return
	online = False
	logger.logger.info('TERMINATION')

pyper.addclasspath(configurer.sphinxcore)
pyper.addclasspath(configurer.sphinxdata)
configuration = None
recognizer = None
online = False
logger.logger.info('CREATION')
