import networkx
from networkx.readwrite import json_graph
import logger

def setsimilarity(sourceset, targetset):
	logger.logger.debug('INPUT SOURCESET <' + str(sourceset) + '>')
	logger.logger.debug('INPUT TARGETSET <' + str(targetset) + '>')
	similarity = float(len(sourceset.intersection(targetset))) / float(max(len(sourceset), len(targetset)))
	logger.logger.log(logger.details, 'OUTPUT <' + str(similarity) + '>')
	return similarity

def depth(graph, node = 0):
	height = 0
	for child in graph.edge[node]:
		height = max(height, depth(graph, child))
	height += 1
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT NODE <' + str(node) + '>')
	logger.logger.log(logger.details, 'OUTPUT <' + str(height) + '>')
	return height

def dependencyspan(graph, node = 0):
	span = set()
	for child in graph.edge[node]:
		span.update(dependencyspan(graph, child))
	span.add(node)
	graph.node[node]['span'] = span
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT NODE <' + str(node) + '>')
	logger.logger.log(logger.details, 'OUTPUT <' + str(span) + '>')
	return span

def wordspan(text, startindex, endindex, graph):
	logger.logger.debug('INPUT TEXT <' + text.strip() + '>')
	logger.logger.debug('INPUT STARTINDEX <' + str(startindex) + '>')
	logger.logger.debug('INPUT ENDINDEX <' + str(endindex) + '>')
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	spannedwords = set(text[startindex: endindex + 1].split())
	start = 1
	end = graph.number_of_nodes() - 1
	bestscore = 0.0
	while True:
		score = setsimilarity(set([graph.node[node]['token'] for node in range(start, end + 1)]), spannedwords)
		if score <= bestscore:
			break
		start += 1
	start -= 1
	while True:
		score = setsimilarity(set([graph.node[node]['token'] for node in range(start, end + 1)]), spannedwords)
		if score <= bestscore:
			break
		end -= 1
	end += 1
	span = set(range(start, end + 1))
	logger.logger.log(logger.details, 'OUTPUT <' + str(span) + '>')
	return span

def relate(graph, node = 0, label = None):
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT NODE <' + str(node) + '>')
	logger.logger.debug('INPUT LABEL <' + str(label) + '>')
	if 'label' in graph.node[node] and graph.node[node]['label']:
		return
	for child in graph.edge[node]:
		relate(graph, child, label)
	graph.node[node]['label'] = label

def fill(graph, sourcenode, targetnode, label):
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT SOURCENODE <' + str(sourcenode) + '>')
	logger.logger.debug('INPUT TARGETNODE <' + str(targetnode) + '>')
	logger.logger.debug('INPUT LABEL <' + str(label) + '>')
	if not networkx.has_path(graph, sourcenode, targetnode):
		return
	for node in networkx.shortest_path(graph, sourcenode, targetnode)[1: -1]:
		if 'label' in graph[node] and graph.node[node]['label']:
			return
	for node in networkx.shortest_path(graph, sourcenode, targetnode)[1: -1]:
		graph.node[node]['label'] = label

def labelgraph(graph, sentence, annotations):
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT SENTENCE <' + sentence.strip() + '>')
	logger.logger.debug('INPUT ANNOTATIONS <' + str(annotations) + '>')
	dependencyspan(graph)
	relate(graph)
	relations = dict()
	for annotation in annotations:
		bestscore = 0.0
		relations[annotation[3]] = [None, None]
		for node in graph.nodes():
			similarity = setsimilarity(wordspan(sentence, annotation[1], annotation[2], graph), graph.node[node]['span'])
			if similarity > bestscore:
				bestscore = similarity
				relations[annotation[3]] = [depth(graph, node), node]
	for relation in sorted(relations.items(), key = lambda values: values[1]):
		relate(graph, relation[1][1], relation[0])

def labelalign(sourcegraph, targetgraph, alignment):
	logger.logger.debug('INPUT SOURCEGRAPH <' + str(json_graph.node_link_data(sourcegraph)) + '>')
	logger.logger.debug('INPUT TARGETGRAPH <' + str(json_graph.node_link_data(targetgraph)) + '>')
	logger.logger.debug('INPUT ALIGNMENT <' + str(alignment) + '>')
	dependencyspan(targetgraph)
	relate(targetgraph)
	for i in range(len(alignment)):
		if alignment[i]:
			targetgraph.node[alignment[i]]['label'] = sourcegraph.node[i]['label']
	for sourcenode in targetgraph.nodes():
		if targetgraph.node[sourcenode]['label']:
			for targetnode in targetgraph.node[sourcenode]['span']:
				if targetgraph.node[targetnode]['label'] and targetgraph.node[sourcenode]['label'] == targetgraph.node[targetnode]['label']:
					fill(targetgraph, sourcenode, targetnode, targetgraph.node[sourcenode]['label'])

def trimlist(nestedlist):
	if type(nestedlist[1]) == int:
		logger.logger.debug('INPUT <' + str(nestedlist) + '>')
		logger.logger.log(logger.details, 'OUTPUT <' + str(True) + '>')
		return True
	if type(nestedlist[1]) == str:
		logger.logger.debug('INPUT <' + str(nestedlist) + '>')
		logger.logger.log(logger.details, 'OUTPUT <' + str(False) + '>')
		return False
	i = 1
	returnvalue = False
	while i < len(nestedlist):
		if not trimlist(nestedlist[i]):
			del nestedlist[i]
			i -= 1
		else:
			returnvalue = True
		i += 1
	logger.logger.debug('INPUT <' + str(nestedlist) + '>')
	logger.logger.log(logger.details, 'OUTPUT <' + str(returnvalue) + '>')
	return returnvalue

def labellist(nestedlist, graph, alignment, node = 1):
	if type(nestedlist[1]) == str:
		if node < len(alignment) and alignment[node]:
			nestedlist[1] = alignment[node]
		node += 1
		logger.logger.debug('INPUT NESTEDLIST <' + str(nestedlist) + '>')
		logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
		logger.logger.debug('INPUT ALIGNMENT <' + str(alignment) + '>')
		logger.logger.log(logger.details, 'OUTPUT <' + str(node) + '>')
		return node
	for nest in nestedlist[1: ]:
		node = labellist(nest, graph, alignment, node)
	logger.logger.debug('INPUT NESTEDLIST <' + str(nestedlist) + '>')
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT ALIGNMENT <' + str(alignment) + '>')
	logger.logger.log(logger.details, 'OUTPUT <' + str(node) + '>')
	return node

def relabellist(nestedlist, graph):
	if type(nestedlist[1]) == int:
		nestedlist[1] = graph.node[nestedlist[1]]['token']
		logger.logger.debug('INPUT NESTEDLIST <' + str(nestedlist) + '>')
		logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
		return
	for nest in nestedlist[1: ]:
		relabellist(nest, graph)
	logger.logger.debug('INPUT NESTEDLIST <' + str(nestedlist) + '>')
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')

logger.logger.info('CREATION')
