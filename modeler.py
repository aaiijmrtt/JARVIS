import networkx, matplotlib.pyplot
from networkx.readwrite import json_graph
import logger, querier, parser, grapher, aligner, labeler

def model(graph, sentences, annotations):
	logger.logger.debug('INPUT <' + str(json_graph.node_link_data(graph)) + '>')
	bestscore = 0.0
	bestalignment = None
	bestsentence = None
	bestgraph = None
	bestannotation = None
	for sentence, annotation in zip(sentences, annotations):
		sentencetext = sentence[0][1].encode('ascii', 'ignore')
		sentenceparse = parser.dependencyparse(sentencetext)
		sentencegraph = grapher.graphparse(sentenceparse)
		contractedgraph = grapher.contractsubgraph(sentencegraph)
		score, alignment = aligner.align(contractedgraph, graph)
		if score > bestscore:
			bestscore = score
			bestalignment = alignment
			bestgraph = contractedgraph
			bestsentence = sentence
			bestannotation = annotation
	logger.logger.info('OUTPUT BESTSCORE <' + str(bestscore) + '>')
	logger.logger.info('OUTPUT BESTALIGNMENT <' + str(bestalignment) + '>')
	logger.logger.info('OUTPUT BESTSENTENCE <' + str(bestsentence) + '>')
	logger.logger.info('OUTPUT BESTGRAPH <' + str(bestgraph) + '>')
	logger.logger.info('OUTPUT BESTANNOTATION <' + str(bestannotation) + '>')
	return bestscore, bestalignment, bestsentence, bestgraph, bestannotation

def stimulate(graph):
	logger.logger.debug('INPUT <' + str(json_graph.node_link_data(graph)) + '>')
	sentences = list()
	annotations = list()
	for edge in networkx.bfs_edges(graph, 0):
		name = graph.node[edge[1]]['token']
		newsentences, newannotations = querier.smartquery('getsentencesandannotationsbyunitname', (name, ))
		sentences.extend(newsentences)
		annotations.extend(newannotations)
	bestscore, bestalignment, bestsentence, bestgraph, bestannotation = model(graph, sentences, annotations)
	labeler.labelgraph(bestgraph, bestsentence[0][1], bestannotation)
	labeler.labelalign(bestgraph, graph, bestalignment)
	frame = querier.smartquery('getframesbysentenceID', (bestsentence[0][0], ))
	logger.logger.info('OUTPUT FRAME <' + str(frame) + '>')
	logger.logger.info('OUTPUT GRAPH <' + str(json_graph.node_link_data(graph)) + '>')
	return frame, graph

def respond(frameID):
	logger.logger.debug('INPUT <' + str(frameID) + '>')
	graph = grapher.graph.node[frameID]['subgraph']
	sentences, annotations = querier.smartquery('getsentencesandannotationsbyframeID', (frameID, ))
	bestscore, bestalignment, bestsentence, bestgraph, bestannotation = model(graph, sentences, annotations)
	sentencetext = bestsentence[0][1].encode('ascii', 'ignore')
	sentenceparse = parser.constituencyparse(sentencetext)
	sentencelist, index, rootindex = parser.nestedlist(sentenceparse)
	labeler.labellist(sentencelist[0], graph, bestalignment)
	labeler.trimlist(sentencelist[0])
	labeler.relabellist(sentencelist[0], graph)
	logger.logger.info('OUTPUT <' + str(sentencelist) + '>')
	return sentencelist

logger.logger.info('CREATION')
