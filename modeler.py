#!/usr/bin/python
import sys, parser, speaker

Jcparser = parser.ConstituencyParser(True)
Jcparser.initialize()
Jdparser = parser.DependencyParser(True)
Jdparser.initialize()
Jspeaker = speaker.Speaker(True)
Jspeaker.initialize()

try:
	for line in sys.stdin:
		constituencies = Jcparser.parse(line)
		listing, index, rootindex = Jcparser.nestedlist(constituencies[1: ])
		dependencies = Jdparser.parse(line)
		graph = Jdparser.graph(dependencies)
		listing = Jdparser.nestedlist(dependencies)
		Jspeaker.speak(line)

except KeyboardInterrupt:
	Jcparser.terminate()
	Jdparser.terminate()
	Jspeaker.terminate()
