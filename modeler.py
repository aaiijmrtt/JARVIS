#!/usr/bin/python
import re, sys, subprocess, networkx, matplotlib.pyplot

parser_pattern = re.compile("^([a-z:]*)\(([a-zA-Z]*)-([0-9]*), ([a-zA-Z]*)-([0-9]*)\)\n$")

sys.stdout.write("[DEBUG: INITIALIZING ENGINES]\n")
tts_engine = subprocess.Popen("~/Code/NLP/Downloads/espeak-1.48.04-source/linux_32bit/espeak -s 130 -p 50 -k 1", stdin=subprocess.PIPE, shell=True)
dependency_parser = subprocess.Popen("~/Code/NLP/Sources/ConversationModel/streamer.sh", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

try:
	for line in sys.stdin:
		graph = networkx.DiGraph()
		sys.stdout.write("[DEBUG: INPUT %s]\n" %line.strip())
		sys.stdout.write("[DEBUG: CALLING DEPENDENCY PARSER]\n")
		dependency_parser.stdin.write(line)
		while True:
			readline = dependency_parser.stdout.readline()
			match = parser_pattern.match(readline)
			if match:
				graph.add_node(int(match.group(3)), token = match.group(2))
				graph.add_node(int(match.group(5)), token = match.group(4))
				graph.add_edge(int(match.group(3)), int(match.group(5)), relation = match.group(1))
			else:
				break
			sys.stdout.write("[DEBUG: DEPENDENCY PARSER OUTPUT %s]\n" %readline.strip())
		sys.stdout.write("[DEBUG: CALLING TEXT TO SPEECH]\n")
		tts_engine.stdin.write(line)
		sys.stdout.write("[DEBUG: PLOTTING GRAPH]\n")
		networkx.draw_networkx(graph)
		matplotlib.pyplot.show()

except KeyboardInterrupt:
	sys.stdout.write("\n[DEBUG: EXITING]\n")
	tts_engine.terminate()
	dependency_parser.terminate()
	sys.exit()
