import networkx, matplotlib.pyplot
from networkx.readwrite import json_graph
import logger, querier

def graphparse(dependencyparse):
	logger.logger.debug('INPUT <' + str(dependencyparse) + '>')
	returngraph = networkx.DiGraph()
	for dependency in dependencyparse:
		returngraph.add_node(int(dependency[2]), token = dependency[1])
		returngraph.add_node(int(dependency[4]), token = dependency[3])
		returngraph.add_edge(int(dependency[2]), int(dependency[4]), relation = dependency[0])
	logger.logger.info('OUTPUT <' + str(json_graph.node_link_data(returngraph)) + '>')
	return returngraph

def augmentgraph(graph, nestedlist, node = 1):
	if type(nestedlist[1]) == str:
		if node in graph.nodes():
			if graph.node[node]['token'] != nestedlist[1]:
				logger.logger.warn('TOKEN MISMATCH <' + graph.node[node]['token'] + ', ' + nestedlist[1] + '>')
			graph.node[node]['POS'] = nestedlist[0]
		node += 1
		logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
		logger.logger.debug('INPUT NESTEDLIST <' + str(nestedlist) + '>')
		logger.logger.log(logger.details, 'OUTPUT <' + str(node) + '>')
		return node
	for nest in nestedlist[1: ]:
		node = augmentgraph(graph, nest, node)
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT NESTEDLIST <' + str(nestedlist) + '>')
	logger.logger.log(logger.details, 'OUTPUT <' + str(node) + '>')
	return node

def contractsubgraph(graph):
	logger.logger.debug('INPUT <' + str(json_graph.node_link_data(graph)) + '>')
	labels = dict()
	counter = 0
	for node in graph.nodes():
		labels[node] = counter
		counter += 1
	graph = networkx.relabel_nodes(graph, labels, True)
	logger.logger.info('OUTPUT <' + str(json_graph.node_link_data(graph)) + '>')
	return graph

def subgraphplot(graph, POS = False, label = False, offset = 0.05):
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT LABEL <' + str(label) + '>')
	logger.logger.debug('INPUT OFFSET <' + str(offset) + '>')
	positions = networkx.shell_layout(graph)
	networkx.draw(graph, positions, labels = networkx.get_node_attributes(graph, 'token'))
	networkx.draw_networkx_edge_labels(graph, positions, edge_labels = networkx.get_edge_attributes(graph, 'relation'))
	if label:
		for position in positions:
			newposition = list(positions[position])
			newposition[1] += offset
			positions[position] = newposition
		networkx.draw_networkx_labels(graph, positions, labels = networkx.get_node_attributes(graph, 'label'))
	if POS:
		for position in positions:
			newposition = list(positions[position])
			newposition[1] += offset
			positions[position] = newposition
		networkx.draw_networkx_labels(graph, positions, labels = networkx.get_node_attributes(graph, 'POS'))
	matplotlib.pyplot.show()

def graphplot(graph, offset = 0.25):
	logger.logger.debug('INPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	logger.logger.debug('INPUT OFFSET <' + str(offset) + '>')
	positions = networkx.shell_layout(graph)
	networkx.draw(graph, positions, labels = networkx.get_node_attributes(graph, 'name'))
	networkx.draw_networkx_edge_labels(graph, positions, edge_labels = networkx.get_edge_attributes(graph,'relation'), label_pos = offset)
	matplotlib.pyplot.show()

def insertactivenode(frameID, node):
	global graph, active
	logger.logger.debug('INPUT FRAMEID <' + str(frameID) + '>')
	logger.logger.debug('INPUT NODE <' + str(json_graph.node_link_data(node)) + '>')
	active = frameID
	if frameID not in graph.nodes():
		frame = querier.smartquery('getframebyID', (frameID, ))
		graph.add_node(frameID, name = frame[0][1], subgraph = node)
		return
	offset = max(graph.node[frameID]['subgraph'].nodes()) if 0 in graph.node[frameID]['subgraph'].nodes() else 0
	labels = dict()
	for oldnode in graph.node[frameID]['subgraph'].nodes():
		labels[oldnode] = oldnode + offset
	labels[0] = 0
	node = networkx.relabel_nodes(node, labels, True)
	graph.node[frameID]['subgraph'].add_nodes_from(node.nodes(data = True))
	graph.node[frameID]['subgraph'].add_edges_from(node.edges(data = True))

def expandactivenode():
	global graph, active
	if not active:
		logger.logger.warn('INACTIVE')
		return
	newframes = set()
	toframes = querier.smartquery('getrelatedframesbyfromID', active)
	for toframe in toframes:
		toframeID = querier.smartquery('getframebyname', (toframe[1], ))
		if toframeID[0][0] not in graph.nodes():
			graph.add_node(int(toframeID[0][0]), name = toframeID[0][1], subgraph = networkx.DiGraph())
			newframes.add(int(toframeID[0][0]))
		graph.add_edge(active, int(toframeID[0][0]), relation = toframe[2])
	fromframes = querier.smartquery('getrelatedframesbytoID', active)
	for fromframe in fromframes:
		fromframename = querier.smartquery('getframebyID', (fromframe[0], ))
		if fromframename[0][0] not in graph.nodes():
			graph.add_node(int(fromframe[0]), name = fromframename[0][1], subgraph = networkx.DiGraph())
			newframes.add(int(fromframe[0]))
		graph.add_edge(int(fromframe[0]), active, relation = fromframe[2])
	logger.logger.info('OUTPUT <' + str(newframes) + '>')
	return newframes

graph = networkx.DiGraph()
active = None
logger.logger.info('CREATION')
