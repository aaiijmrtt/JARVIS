import subprocess, re

class ConstituencyParser:
	def __init__(self, debug):
		self.debug = debug
		self.online = False

	def initialize(self):
		if not self.online:
			self.parser = subprocess.Popen('java -mx150m -classpath "../../Downloads/stanford-parser-full-2015-04-20/*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -outputFormat "oneline" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz -', stdin = subprocess.PIPE, stdout = subprocess.PIPE, shell = True)
		self.online = True
		if self.debug:
			print '[DEBUG: INITIALIZED CONSTITUENCY PARSER]'

	def parse(self, line):
		self.parser.stdin.write(line)
		readline = self.parser.stdout.readline()
		if self.debug:
			print '[DEBUG: CONSTITUENCY PARSER INPUT', line.strip(), ']'
			print '[DEBUG: CONSTITUENCY PARSER OUTPUT', readline.strip(), ']'
		return readline

	def nestedlist(self, parse, index = 0):
		returnlist = list()
		rootindex = index
		lastindex = index
		while index < len(parse):
			if parse[index] == '(':
				sublist, index, subrootindex = self.nestedlist(parse, index + 1)
				returnlist.append(sublist)
				lastindex = index
			elif parse[index] == ')':
				if lastindex != index:
					returnlist.append(parse[lastindex: index])
				if self.debug and rootindex == 0:
					print '[DEBUG: LISTING CONSTITUENCIES', returnlist, ']'
				return returnlist, index + 1, rootindex
			elif parse[index] == ' ':
				if lastindex != index:
					returnlist.append(parse[lastindex: index])
				index += 1
				lastindex = index
			else:
				index += 1
		if self.debug and rootindex == 0:
			print '[DEBUG: LISTING CONSTITUENCIES', returnlist, ']'
		return returnlist, index, rootindex

	def terminate(self):
		if self.online:
			self.parser.terminate()
		self.online = False
		if self.debug:
			print '[DEBUG: TERMINATED CONSTITUENCY PARSER]'

class DependencyParser:
	def __init__(self, debug):
		self.debug = debug
		self.pattern = re.compile('^([a-z:]*)\(([a-zA-Z]*)-([0-9]*), ([a-zA-Z]*)-([0-9]*)\)\n$')
		self.online = False

	def initialize(self):
		if not self.online:
			self.parser = subprocess.Popen('java -mx150m -classpath "../../Downloads/stanford-parser-full-2015-04-20/*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -outputFormat "typedDependencies" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz -', stdin = subprocess.PIPE, stdout = subprocess.PIPE, shell = True)
		self.online = True
		if self.debug:
			print '[DEBUG: INITIALIZED DEPENDENCY PARSER]'

	def parse(self, line):
		self.parser.stdin.write(line)
		returnparse = list()
		readline = self.parser.stdout.readline()
		while readline != '\n':
			returnparse.append(readline)
			readline = self.parser.stdout.readline()
		if self.debug:
			print '[DEBUG: DEPENDENCY PARSER INPUT', line.strip(), ']'
			print '[DEBUG: DEPENDENCY PARSER OUTPUT', returnparse, ']'
		return returnparse

	def graph(self, parse):
		import networkx
		returngraph = networkx.DiGraph()
		for line in parse:
			match = self.pattern.match(line)
			if match:
				returngraph.add_node(int(match.group(3)), token = match.group(2))
				returngraph.add_node(int(match.group(5)), token = match.group(4))
				returngraph.add_edge(int(match.group(3)), int(match.group(5)), relation = match.group(1))
		if self.debug:
			import matplotlib.pyplot
			print '[DEBUG: GRAPHING DEPENDENCIES]'
			labeling = dict()
			for node in returngraph.nodes(True):
				labeling[node[0]] = node[1]['token']
			networkx.draw_networkx(returngraph, labels = labeling)
			matplotlib.pyplot.show()
		return returngraph

	def terminate(self):
		if self.online:
			self.parser.terminate()
		self.online = False
		if self.debug:
			print '[DEBUG: TERMINATED DEPENDENCY PARSER]'
