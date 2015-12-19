#!/bin/bash
cd ~/Code/NLP/Downloads/stanford-parser-full-2015-04-20/
java -mx150m -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -outputFormat "typedDependencies" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz -
