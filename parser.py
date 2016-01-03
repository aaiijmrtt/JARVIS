import re
import jpype
import configurer, logger, pyper

def initialize():
	global online, parser
	if online:
		logger.logger.warn('REINITIALIZATION')
		return
	parser = jpype.JClass('Parser')()
	parser.initialize()
	online = True
	logger.logger.info('INITIALIZATION')

def constituencyparse(line):
	global online, parser
	if not online:
		logger.logger.warn('UNINITIALIZED')
		logger.logger.warn('INPUT <' + line.strip() + '>')
		return
	logger.logger.info('INPUT <' + line.strip() + '>')
	returnparse = str(parser.constituencyParse(line).toString())
	logger.logger.info('OUTPUT <' + returnparse + '>')
	return returnparse

def dependencyparse(line):
	global online, parser
	if not online:
		logger.logger.warn('UNINITIALIZED')
		logger.logger.warn('INPUT <' + line.strip() + '>')
		return
	logger.logger.debug('INPUT <' + line.strip() + '>')
	parse = parser.dependencyParse(line)
	returnparse = list()
	for dependency in parse:
		returnparse.append((str(dependency.reln().toString()), str(dependency.gov().value()), int(dependency.gov().index()), str(dependency.dep().value()), int(dependency.dep().index())))
	logger.logger.info('OUTPUT <' + str(returnparse) + '>')
	return returnparse

def nestedlist(constituencyparse, index = 0):
	returnlist = list()
	rootindex = index
	lastindex = index
	while index < len(constituencyparse):
		if constituencyparse[index] == '(':
			sublist, index, subrootindex = nestedlist(constituencyparse, index + 1)
			returnlist.append(sublist)
			lastindex = index
		elif constituencyparse[index] == ')':
			if lastindex != index:
				returnlist.append(constituencyparse[lastindex: index])
				logger.logger.debug('INPUT <' + constituencyparse + '>')
				logger.logger.log(logger.details, 'OUTPUT <' + str(returnlist) + '>')
			return returnlist, index + 1, rootindex
		elif constituencyparse[index] == ' ':
			if lastindex != index:
				returnlist.append(constituencyparse[lastindex: index])
			index += 1
			lastindex = index
		else:
			index += 1
	logger.logger.debug('INPUT <' + constituencyparse + '>')
	logger.logger.log(logger.details, 'OUTPUT <' + str(returnlist) + '>')
	return returnlist, index, rootindex

def terminate():
	global online, parser
	if not online:
		logger.logger.warn('UNINITIALIZED')
		return
	parser.terminate()
	online = False
	logger.logger.info('TERMINATION')

pyper.addclasspath(configurer.stanfordparser)
pyper.addclasspath(configurer.stanfordmodels)
pyper.addclasspath(configurer.stanfordwrapper)
online = False
parser = None
logger.logger.info('CREATION')
