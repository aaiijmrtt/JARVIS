import re
import networkx, matplotlib.pyplot, jpype
from networkx.readwrite import json_graph
import configurer, logger, pyper

def initialize():
	global online, parser
	if online:
		logger.logger.warn('PARSER REINITIALIZATION')
		return
	parser = jpype.JClass('Parser')()
	parser.initialize()
	online = True
	logger.logger.info('PARSER INITIALIZATION')

def constituencyparse(line):
	global online, parser
	if not online:
		logger.logger.warn('UNINITIALIZED CONSTITUENCY PARSER INPUT <' + line.strip() + '>')
		return
	logger.logger.info('CONSTITUENCY PARSER INPUT <' + line.strip() + '>')
	returnparse = str(parser.constituencyParse(line).toString())
	logger.logger.info('CONSTITUENCY PARSER OUTPUT <' + returnparse + '>')
	return returnparse

def dependencyparse(line):
	global online, parser
	if not online:
		logger.logger.warn('UNINITIALIZED DEPENDENCY PARSER INPUT <' + line.strip() + '>')
		return
	logger.logger.debug('DEPENDENCY PARSER INPUT <' + line.strip() + '>')
	parse = parser.dependencyParse(line)
	returnparse = list()
	for dependency in parse:
		returnparse.append((str(dependency.reln().toString()), str(dependency.gov().toString()), int(dependency.gov().index()), str(dependency.dep().toString()), int(dependency.dep().index())))
	logger.logger.info('DEPENDENCY PARSER OUTPUT <' + str(returnparse) + '>')
	return returnparse

def graph(dependencyparse):
	logger.logger.debug('GRAPH INPUT <' + str(dependencyparse) + '>')
	returngraph = networkx.DiGraph()
	for dependency in dependencyparse:
		returngraph.add_node(int(dependency[2]), token = dependency[1])
		returngraph.add_node(int(dependency[4]), token = dependency[3])
		returngraph.add_edge(int(dependency[2]), int(dependency[4]), relation = dependency[0])
	logger.logger.info('GRAPH OUTPUT <' + str(json_graph.node_link_data(returngraph)) + '>')
	return returngraph

def plot(graph):
	logger.logger.debug('PLOT INPUT <' + str(json_graph.node_link_data(graph)) + '>')
	positions = networkx.spring_layout(graph)
	networkx.draw(graph, positions, labels = networkx.get_node_attributes(graph, 'token'))
	networkx.draw_networkx_edge_labels(graph, positions, labels = networkx.get_edge_attributes(graph,'relation'))
	matplotlib.pyplot.show()

def nestedlist(constituencyparse, index = 0):
	if index == 0:
		logger.logger.debug('NESTEDLIST INPUT <' + constituencyparse + '>')
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
			if rootindex == 0:
				logger.logger.info('NESTEDLIST OUTPUT <' + str(returnlist) + '>')
			return returnlist, index + 1, rootindex
		elif constituencyparse[index] == ' ':
			if lastindex != index:
				returnlist.append(constituencyparse[lastindex: index])
			index += 1
			lastindex = index
		else:
			index += 1
	if rootindex == 0:
		logger.logger.info('NESTEDLIST OUTPUT <' + str(returnlist) + '>')
	return returnlist, index, rootindex

def terminate():
	global online, parser
	if not online:
		logger.logger.warn('UNINITIALIZED PARSER TERMINATION')
		return
	parser.terminate()
	online = False
	logger.logger.info('PARSER TERMINATION')

pyper.addclasspath(configurer.stanfordparser)
pyper.addclasspath(configurer.stanfordmodels)
pyper.addclasspath(configurer.stanfordwrapper)
online = False
parser = None
logger.logger.info('PARSER CREATION')
