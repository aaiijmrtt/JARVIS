import parser

class ILPAligner:
	def __init__(self, debug, dparser = None):
		self.debug = debug
		self.parser = dparser if dparser is not None else parser.DependencyParser(self.debug)
		self.parser.initialize()

	def similarity(self, target, source):
		import nltk.corpus
		scores = [nltk.corpus.wordnet.path_similarity(synsource, syntarget) for synsource in nltk.corpus.wordnet.synsets(source) for syntarget in nltk.corpus.wordnet.synsets(target)]
		scores = [score for score in scores if score is not None]
		score = 0.0 if len(scores) == 0 else max(scores)
		if self.debug:
			print '[DEBUG: SIMILARITY (', target, ',', source, ') = ', score, ']'
		return score

	def align(self, targetline, sourceline):
		import pulp
		sources = sourceline.split()
		targets = targetline.split()
		sourceparse = self.parser.parse(sourceline)
		targetparse = self.parser.parse(targetline)
		lex = [[self.similarity(target, source) for target in targets] for source in sources]
		syn = [[[[0.0 for i in range(len(targets))] for j in range(len(sources))] for k in range(len(targets))] for l in range(len(sources))]
		synsource = self.parser.graph(sourceparse)
		syntarget = self.parser.graph(targetparse)

		problem = pulp.LpProblem('ALIGNMENT', pulp.LpMaximize)
		x = [[pulp.LpVariable(str(j) + ':' + str(i), 0, 1, pulp.LpInteger) for i in range(len(targets))] for j in range(len(sources))]
		y = [[[[pulp.LpVariable(str(l) + ':' + str(k) + '::' + str(j) + ':' + str(i), 0, 1, pulp.LpInteger) for i in range(len(targets))] for j in range(len(sources))] for k in range(len(targets))] for l in range(len(sources))]
		for i in range(len(sources)):
			problem += pulp.lpSum([x[i][j] for j in range(len(targets))]) <= 1
		for j in range(len(targets)):
			problem += pulp.lpSum([x[i][j] for i in range(len(sources))]) <= 1
		for i in range(len(sources)):
			for j in range(len(targets)):
				for k in range(len(sources)):
					for l in range(len(targets)):
						problem += y[i][j][k][l] <= x[i][j]
						problem += y[i][j][k][l] <= x[k][l]
						problem += y[i][j][k][l] >= x[i][j] + x[k][l] - 1
						syn[i][j][k][l] = 1.0 if synsource.has_edge(i + 1, k + 1) and syntarget.has_edge(j + 1, l + 1) and synsource[i + 1][k + 1]['relation'] == syntarget[j + 1][l + 1]['relation'] else 0.0

		problem += pulp.lpSum([lex[i][j] * x[i][j] for j in range(len(targets)) for i in range(len(sources))] + [syn[i][j][k][l] * y[i][j][k][l] for l in range(len(targets)) for k in range(len(sources)) for j in range(len(targets)) for i in range(len(sources))])
		problem.solve()
		alignment = [None for i in range(len(sources))]
		for variable in problem.variables():
			if variable.name.find('::') == -1 and variable.varValue == 1:
				source, target = variable.name.split(':')
				alignment[int(source)] = int(target)
		if self.debug:
			print '[DEBUG: ALIGNMENT SOURCE', sourceline.strip(), ']'
			print '[DEBUG: ALIGNMENT TARGET', targetline.strip(), ']'
			print '[DEBUG: ALIGNMENT', alignment, ']'
		return alignment
