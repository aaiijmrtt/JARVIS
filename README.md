# JARVIS

**Natural Language Understanding Artificially Intelligent Being**

This is not a toy.

**Features**:

* Speech to Text Interface
* Dependency Parsing
* Frame Semantic Role Labeling
* Graph Alignment
* Integer Linear Programming
* Knowledge Graph
* Database Management
* Constituency Parsing
* Natual Language Generation
* Text To Speech Interface

**Note**:

* Requires Python
* Requires MySQLdb
* Requires jpype
* Requires nltk
* Requires networkx
* Requires matplotlib
* Requires pulp
* Requires MySQL
* Requires Java
* Requires CMU Sphinx 
* Requires Stanford Parser
* Requires SimplgNLG
* Requires Espeak

**MySQL Configuration**:

* Host Name: localhost
* User Name: root
* No Password
* Database Name: Jarvis

**Directory Structure**:

	Root
	+-- Downloads
	|   +-- espeak-1.48.04-source
	|   |   +-- linux_32bit
	|   |       +-- espeak
	|   +-- framenet_v15
	|   |   +-- frame
	|   |   |   +-- *.xml
	|   |   +-- lu
	|   |       +-- *.xml
	|   +-- jdk1.8.0_92
	|   |   +-- jre
	|   |       +-- lib
	|   |           +-- amd64
	|   |               +-- server
	|   |                   +-- libjvm.so
	|   +-- simplenlg-v4.4.8
	|   |   +-- simplenlg-v4.4.8
	|   |   |   +-- SimpleNLG-4.4.8.jar
	|   +-- sphinx4-5prealpha-src
	|   |   +-- sphinx4-core
	|   |   |   +-- target
	|   |   |       +-- sphinx4-core-1.0-SNAPSHOT.jar
	|   |   +-- sphinx4-data
	|   |       +-- target
	|   |           +-- sphinx4-data-1.0-SNAPSHOT.jar
	|   +-- stanford-parser-full-2015-12-09
	|       +-- stanford-parser.jar
	|       +-- stanford-parser-3.6.0-models.jar
	+-- Sources
		+-- Jarvis
		    +-- aligner.py
		    +-- configurer.py
		    +-- connector.py
		    +-- extractor.py
		    +-- generator.py
		    +-- grapher.py
		    +-- labeler.py
		    +-- listener.py
		    +-- logger.py
		    +-- modeler.py
		    +-- parser.py
		    +-- pyper.py
		    +-- querier.py
		    +-- speaker.py
		    +-- tester.py
		    +-- Parser.java
		    +-- parser.jar

**Exploring the Code**:

You might want to take a look at `tester.py` once you have installed all the dependencies / positioned them according to the outlined directory structure. If you change the directory structure, you must suitably modify the paths in `configurer.py`. Pick and run the test for a module to get an idea of how it works. Please run `testExtractor()` first, as this initializes the database. Make sure MySQL server is running, and the timeout is set to an obscenely large period. Don't bother letting `testModeler()` complete.
