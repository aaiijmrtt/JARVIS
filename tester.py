def testAligner():
	from networkx.readwrite import json_graph
	import aligner
	sourcegraph = json_graph.node_link_graph({'directed': True, 'graph': [], 'nodes': [{'token': 'ROOT', 'id': 0}, {'token': 'This', 'id': 1}, {'token': 'sentence', 'id': 2}, {'token': 'is', 'id': 3}, {'token': 'a', 'id': 4}, {'token': 'test', 'id': 5}], 'links': [{'source': 0, 'relation': 'root', 'target': 5}, {'source': 2, 'relation': 'det', 'target': 1}, {'source': 5, 'relation': 'nsubj', 'target': 2}, {'source': 5, 'relation': 'cop', 'target': 3}, {'source': 5, 'relation': 'det', 'target': 4}], 'multigraph': False})
	targetgraph = json_graph.node_link_graph({'directed': True, 'graph': [], 'nodes': [{'token': 'ROOT', 'id': 0}, {'token': 'This', 'id': 1}, {'token': 'sentence', 'id': 2}, {'token': 'is', 'id': 3}, {'token': 'another', 'id': 4}, {'token': 'test', 'id': 5}], 'links': [{'source': 0, 'relation': 'root', 'target': 5}, {'source': 2, 'relation': 'det', 'target': 1}, {'source': 5, 'relation': 'nsubj', 'target': 2}, {'source': 5, 'relation': 'cop', 'target': 3}, {'source': 5, 'relation': 'det', 'target': 4}], 'multigraph': False})

	score, alignment = aligner.align(sourcegraph, targetgraph)
	aligner.score(sourcegraph, targetgraph, alignment)

def testConfigurer():
	import configurer

	print configurer.database

def testConnector():
	import connector

	connector.initialize()
	connector.execute('SELECT * FROM Frame')
	connector.execute('SELECT * FROM Frame WHERE ID = %s', (5, ))
	connector.executemany('SELECT * FROM Frame WHERE ID = %s', ((1, ), (2, ), (3, ), (4, ), (5, )))
	connector.fetchall()
	connector.terminate()

def testExtractor():
	import connector, extractor, configurer

	extractor.extractframes(configurer.frames)
	extractor.extractunits(configurer.units)
	print len(extractor.frame)
	print len(extractor.element)
	print len(extractor.relates)
	print len(extractor.unit)
	print len(extractor.sentence)
	print len(extractor.annotation)
	print len(extractor.evokes)
	print len(extractor.embodies)
	connector.initialize()
	extractor.createdatabase()
	extractor.populatedatabase()
	connector.terminate()

def testGenerator():
	import generator, pyper
	parsedlist = [['ROOT', ['S', ['NP', ['DT', 'This'], ['NN', 'sentence']], ['VP', ['VBZ', 'is'], ['NP', ['DT', 'a'], ['NN', 'test']]], ['.', '.']]]]

	pyper.initialize()
	generator.initialize()
	generated = generator.generate(parsedlist[0][1])
	generator.terminate()
	pyper.terminate()

def testGrapher():
	import grapher, connector
	dependencyparse = [('det', 'sentence', 2, 'This', 1), ('nsubj', 'test', 5, 'sentence', 2), ('cop', 'test', 5, 'is', 3), ('det', 'test', 5, 'a', 4), ('root', 'ROOT', 0, 'test', 5)]
	parsedlist = [['ROOT', ['S', ['NP', ['DT', 'This'], ['NN', 'sentence']], ['VP', ['VBZ', 'is'], ['NP', ['DT', 'a'], ['NN', 'test']]], ['.', '.']]]]

	connector.initialize()
	graph = grapher.graphparse(dependencyparse)
	grapher.insertactivenode(107, graph)
	grapher.subgraphplot(grapher.graph.node[107]['subgraph'])
	grapher.expandactivenode()
	grapher.graphplot(grapher.graph)
	graph = grapher.graphparse(dependencyparse)
	grapher.insertactivenode(107, graph)
	graph = grapher.graphparse(dependencyparse)
	grapher.insertactivenode(198, graph)
	grapher.subgraphplot(grapher.graph.node[107]['subgraph'])
	grapher.subgraphplot(grapher.graph.node[198]['subgraph'])
	grapher.expandactivenode()
	grapher.graphplot(grapher.graph)
	connector.terminate()
	grapher.augmentgraph(graph, parsedlist[0])
	grapher.subgraphplot(graph, POS = True)

def testLabeler():
	from networkx.readwrite import json_graph
	import labeler, grapher
	sourcesentence = 'This sentence is a test.'
	sourcegraph = json_graph.node_link_graph({'directed': True, 'graph': [], 'nodes': [{'token': 'ROOT', 'id': 0}, {'token': 'This', 'id': 1}, {'token': 'sentence', 'id': 2}, {'token': 'is', 'id': 3}, {'token': 'a', 'id': 4}, {'token': 'test', 'id': 5}], 'links': [{'source': 0, 'relation': 'root', 'target': 5}, {'source': 2, 'relation': 'det', 'target': 1}, {'source': 5, 'relation': 'nsubj', 'target': 2}, {'source': 5, 'relation': 'cop', 'target': 3}, {'source': 5, 'relation': 'det', 'target': 4}], 'multigraph': False})
	targetgraph = json_graph.node_link_graph({'directed': True, 'graph': [], 'nodes': [{'token': 'ROOT', 'id': 0}, {'token': 'This', 'id': 1}, {'token': 'sentence', 'id': 2}, {'token': 'is', 'id': 3}, {'token': 'another', 'id': 4}, {'token': 'test', 'id': 5}], 'links': [{'source': 0, 'relation': 'root', 'target': 5}, {'source': 2, 'relation': 'det', 'target': 1}, {'source': 5, 'relation': 'nsubj', 'target': 2}, {'source': 5, 'relation': 'cop', 'target': 3}, {'source': 5, 'relation': 'det', 'target': 4}], 'multigraph': False})
	annotations = [(1, 5, 13, 'subject'), (1, 14, 16, 'verb'), (1, 19, 23, 'object')]
	alignment = [None, 1, 2, 3, 4, 5]
	realignment = [None, 1, 2, 3, None, 4]
	parsedlist = [['ROOT', ['S', ['NP', ['DT', 'This'], ['NN', 'sentence']], ['VP', ['VBZ', 'is'], ['NP', ['DT', 'a'], ['NN', 'test']]], ['.', '.']]]]

	labeler.labelgraph(sourcegraph, sourcesentence, annotations)
	labeler.labelalign(sourcegraph, targetgraph, alignment)
	grapher.subgraphplot(sourcegraph, label = True)
	grapher.subgraphplot(targetgraph, label = True)
	labeler.labellist(parsedlist[0], targetgraph, realignment)
	labeler.trimlist(parsedlist[0])
	labeler.relabellist(parsedlist[0], targetgraph)
	print parsedlist

def testListener():
	import listener, pyper

	pyper.initialize()
	listener.initialize()
	listener.listen()
	listener.terminate()
	pyper.terminate()

def testLogger():
	import logger

	logger.logger.debug('DEBUG')
	logger.logger.log(logger.details, 'DETAILS')
	logger.logger.info('INFO')

def testModeler():
	from networkx.readwrite import json_graph
	import connector, pyper, parser, modeler, grapher
	ingraph = json_graph.node_link_graph({'directed': True, 'graph': [], 'nodes': [{'token': 'ROOT', 'id': 0}, {'token': 'This', 'POS': 'DT', 'id': 1}, {'token': 'sentence', 'POS': 'NN', 'id': 2}, {'token': 'is', 'POS': 'VBZ', 'id': 3}, {'token': 'a', 'POS': 'DT', 'id': 4}, {'token': 'test', 'POS': 'NN', 'id': 5}], 'links': [{'source': 0, 'relation': 'root', 'target': 5}, {'source': 2, 'relation': 'det', 'target': 1}, {'source': 5, 'relation': 'nsubj', 'target': 2}, {'source': 5, 'relation': 'cop', 'target': 3}, {'source': 5, 'relation': 'det', 'target': 4}], 'multigraph': False})
	outgraph = json_graph.node_link_graph({'directed': True, 'graph': [], 'nodes': [{'token': 'ROOT', 'span': set([0, 1, 2, 3, 4, 5]), 'id': 0, 'label': None}, {'token': 'This', 'label': None, 'span': set([1]), 'id': 1, 'POS': 'DT'}, {'token': 'sentence', 'label': None, 'span': set([1, 2]), 'id': 2, 'POS': 'NN'}, {'token': 'is', 'label': None, 'span': set([3]), 'id': 3, 'POS': 'VBZ'}, {'token': 'a', 'label': None, 'span': set([4]), 'id': 4, 'POS': 'DT'}, {'token': 'test', 'label': None, 'span': set([1, 2, 3, 4, 5]), 'id': 5, 'POS': 'NN'}], 'links': [{'source': 0, 'relation': 'root', 'target': 5}, {'source': 2, 'relation': 'det', 'target': 1}, {'source': 5, 'relation': 'nsubj', 'target': 2}, {'source': 5, 'relation': 'cop', 'target': 3}, {'source': 5, 'relation': 'det', 'target': 4}], 'multigraph': False})

	connector.initialize()
	pyper.initialize()
	parser.initialize()
	modeler.stimulate(ingraph)
	grapher.insertactivenode(107, outgraph), aligner, grapher, labeler
	modeler.respond()
	parser.terminate()
	pyper.terminate()
	connector.terminate()

def testParser():
	import parser, pyper
	line = 'This sentence is a test.'

	pyper.initialize()
	parser.initialize()
	parse = parser.constituencyparse(line)
	parser.nestedlist(parse)
	parse = parser.dependencyparse(line)
	parser.terminate()
	pyper.terminate()

def testPyper():
	import jpype, pyper
	line = 'This sentence is a test.'

	pyper.initialize()
	jpype.java.lang.System.out.println(line)
	pyper.terminate()

def testQuerier():
	import connector, querier

	connector.initialize()
	querier.smartquery('getframebyID', (5, ))
	querier.smartquery('getframebyname', ('Causation', ))
	querier.smartquery('getelementbyID', (18, ))
	querier.smartquery('getelementsbyframeID', (5, ))
	querier.smartquery('getunitbyID', (2, ))
	querier.smartquery('getunitbyname', ('cause', ))
	querier.smartquery('getunitbynameandPOS', ('cause', 'V'))
	querier.smartquery('getsentencebyID', (651962, ))
	querier.smartquery('getannotationsbysentenceID', (651962, ))
	querier.smartquery('getevokedframesbyunitID', (2, ))
	querier.smartquery('getevokedframesbyunitname', ('cause', ))
	querier.smartquery('getevokedframesbyunitnameandPOS', ('cause', 'V'))
	querier.smartquery('getevokingunitsbyframeID', (5, ))
	querier.smartquery('getembodiedunitsbysentenceID', (651962, ))
	querier.smartquery('getembodyingsentencesbyunitID', (2, ))
	querier.smartquery('getrelatedframesbytoID', (5, ))
	querier.smartquery('getrelatedframesbyfromID', (5, ))
	querier.smartquery('getrelatedframesbytoname', ('Causation', ))
	querier.smartquery('getrelatedframesbyfromname', ('Causation', ))
	querier.smartquery('getframesbysentenceID', (651962, ))
	querier.smartquery('getsentencesandannotationsbyunitnameandPOS', ('cause', 'V'))
	connector.terminate()

def testSpeaker():
	import speaker
	line = 'This sentence is a test.'

	speaker.initialize()
	speaker.speak(line)
	speaker.terminate()

if __name__ == '__main__':
	pass
#	testExtractor()
#	testAligner()
#	testConfigurer()
#	testConnector()
#	testGenerator()
#	testGrapher()
#	testLabeler()
#	testListener()
#	testLogger()
#	testModeler()
#	testParser()
#	testPyper()
#	testQuerier()
#	testSpeaker()
