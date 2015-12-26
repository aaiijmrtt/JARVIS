import java.util.List;
import java.util.Collection;
import java.io.StringReader;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreebankLanguagePack;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;

public class Parser {
	public String model;
	public LexicalizedParser parser;
	public TreebankLanguagePack treebanklanguagepack;
	public GrammaticalStructureFactory grammaticalstructurefactory;
	boolean online;

	public Parser() {
		model = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
		online = false;
	}

	public void initialize() {
		if(!online) {
			parser = LexicalizedParser.loadModel(model);
			treebanklanguagepack = parser.treebankLanguagePack();
			grammaticalstructurefactory = treebanklanguagepack.grammaticalStructureFactory();
		}
		online = true;
	}

	public Collection dependencyParse(String line) {
		if(!online)
			return null;
		Tokenizer<? extends HasWord> tokenizer = treebanklanguagepack.getTokenizerFactory().getTokenizer(new StringReader(line));
		List<? extends HasWord> sentence = tokenizer.tokenize();
		Tree parse = parser.apply(sentence);
		GrammaticalStructure grammaticalstructure = grammaticalstructurefactory.newGrammaticalStructure(parse);
		Collection dependencies = grammaticalstructure.typedDependenciesCCprocessed();
		return dependencies;
	}

	public Tree constituencyParse(String line) {
		if(!online)
			return null;
		Tokenizer<? extends HasWord> tokenizer = treebanklanguagepack.getTokenizerFactory().getTokenizer(new StringReader(line));
		List<? extends HasWord> sentence = tokenizer.tokenize();
		Tree parse = parser.apply(sentence);
		return parse;
	}

	public void terminate() {
		online = false;
	}
}
