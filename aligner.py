import pulp, nltk.corpus
from networkx.readwrite import json_graph
import logger

def similarity(source, target):
	logger.logger.debug('SIMILARITY INPUT SOURCE <' + source + '>')
	logger.logger.debug('SIMILARITY INPUT TARGET <' + source + '>')
	scores = [nltk.corpus.wordnet.path_similarity(synsource, syntarget) for synsource in nltk.corpus.wordnet.synsets(source) for syntarget in nltk.corpus.wordnet.synsets(target)]
	scores = [score for score in scores if score is not None]
	score = 0.0 if len(scores) == 0 else max(scores)
	logger.logger.log(logger.details, 'SIMILARITY OUTPUT <' + str(score) + '>')
	return score

def align(sourcegraph, targetgraph):
	logger.logger.debug('ALIGNMENT INPUT SOURCE <' + str(json_graph.node_link_data(sourcegraph)) + '>')
	logger.logger.debug('ALIGNMENT INPUT TARGET <' + str(json_graph.node_link_data(targetgraph)) + '>')
	lexical = [[similarity(targetgraph.node[i]['token'], sourcegraph.node[j]['token']) for i in range(1, targetgraph.number_of_nodes())] for j in range(1, sourcegraph.number_of_nodes())]
	syntactic = [[[[0.0 for i in range(targetgraph.number_of_nodes() - 1)] for j in range(sourcegraph.number_of_nodes() - 1)] for k in range(targetgraph.number_of_nodes() - 1)] for l in range(sourcegraph.number_of_nodes() - 1)]

	problem = pulp.LpProblem('ALIGNMENT', pulp.LpMaximize)
	x = [[pulp.LpVariable(str(j) + ':' + str(i), 0, 1, pulp.LpInteger) for i in range(targetgraph.number_of_nodes() - 1)] for j in range(sourcegraph.number_of_nodes() - 1)]
	y = [[[[pulp.LpVariable(str(l) + ':' + str(k) + '::' + str(j) + ':' + str(i), 0, 1, pulp.LpInteger) for i in range(targetgraph.number_of_nodes() - 1)] for j in range(sourcegraph.number_of_nodes() - 1)] for k in range(targetgraph.number_of_nodes() - 1)] for l in range(sourcegraph.number_of_nodes() - 1)]
	for i in range(sourcegraph.number_of_nodes() - 1):
		problem += pulp.lpSum([x[i][j] for j in range(targetgraph.number_of_nodes() - 1)]) <= 1
	for j in range(targetgraph.number_of_nodes() - 1):
		problem += pulp.lpSum([x[i][j] for i in range(sourcegraph.number_of_nodes() - 1)]) <= 1
	for i in range(sourcegraph.number_of_nodes() - 1):
		for j in range(targetgraph.number_of_nodes() - 1):
			for k in range(sourcegraph.number_of_nodes() - 1):
				for l in range(targetgraph.number_of_nodes() - 1):
					problem += y[i][j][k][l] <= x[i][j]
					problem += y[i][j][k][l] <= x[k][l]
					problem += y[i][j][k][l] >= x[i][j] + x[k][l] - 1
					syntactic[i][j][k][l] = 1.0 if sourcegraph.has_edge(i + 1, k + 1) and targetgraph.has_edge(j + 1, l + 1) and sourcegraph[i + 1][k + 1]['relation'] == targetgraph[j + 1][l + 1]['relation'] else 0.0

	problem += pulp.lpSum([lexical[i][j] * x[i][j] for j in range(targetgraph.number_of_nodes() - 1) for i in range(sourcegraph.number_of_nodes() - 1)] + [syntactic[i][j][k][l] * y[i][j][k][l] for l in range(targetgraph.number_of_nodes() - 1) for k in range(sourcegraph.number_of_nodes() - 1) for j in range(targetgraph.number_of_nodes() - 1) for i in range(sourcegraph.number_of_nodes() - 1)])
	problem.solve()
	alignment = [None for i in range(sourcegraph.number_of_nodes())]
	for variable in problem.variables():
		if variable.name.find('::') == -1 and variable.varValue == 1:
			source, target = variable.name.split(':')
			alignment[int(source) + 1] = int(target) + 1
	logger.logger.info('ALIGNMENT OUTPUT <' + str(alignment) + '>')
	logger.logger.info('ALIGNMENT OUTPUT VALUE <' + str(problem.objective.value()) + '>')
	return problem.objective.value(), alignment

def score(sourcegraph, targetgraph, alignment):
	logger.logger.debug('SCORE INPUT SOURCE <' + str(json_graph.node_link_data(sourcegraph)) + '>')
	logger.logger.debug('SCORE INPUT TARGET <' + str(json_graph.node_link_data(targetgraph)) + '>')
	logger.logger.debug('SCORE INPUT ALIGNMENT <' + str(alignment) + '>')
	score = 0.0
	for i in range(len(alignment)):
		if alignment[i]:
			score += similarity(sourcegraph.node[i]['token'], targetgraph.node[alignment[i]]['token'])
			for j in range(len(alignment)):
				if i != j and alignment[j]:
					if sourcegraph.has_edge(i, j) and targetgraph.has_edge(alignment[i], alignment[j]) and sourcegraph.edge[i][j] == targetgraph.edge[alignment[i]][alignment[j]]:
						score += 1.0
	logger.logger.info('SCORE OUTPUT <' + str(score) + '>')
	return score

logger.logger.info('ALIGNER CREATION')
