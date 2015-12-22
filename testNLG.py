import sys, parser
sys.path.append('../../Downloads/simplenlg-v442/simplenlg-v4.4.2.jar')
import simplenlg

def initialize():
	global lexicon, factory, realiser
	lexicon = simplenlg.lexicon.Lexicon.getDefaultLexicon()
	factory = simplenlg.framework.NLGFactory(lexicon)
	realiser = simplenlg.realiser.english.Realiser(lexicon)

def Whandler(word, category = None, plural = None, tense = None):
	global factory
	word = factory.createNLGElement(word)
	if category is not None:
		word.setCategory(category)
	if plural is not None:
		word.setPlural(plural)
	if tense is not None:
		word.setTense(tense)
	return word

words = {
	'CC':	(simplenlg.framework.LexicalCategory.CONJUNCTION, None, None),
	'CD':	(simplenlg.framework.LexicalCategory.ANY, None, None),
	'DT':	(simplenlg.framework.LexicalCategory.DETERMINER, None, None),
	'EX':	(simplenlg.framework.LexicalCategory.ANY, None, None),
	'FW':	(simplenlg.framework.LexicalCategory.ANY, None, None),
	'IN':	(simplenlg.framework.LexicalCategory.PREPOSITION, None, None),
	'JJ':	(simplenlg.framework.LexicalCategory.ADJECTIVE, None, None),
	'JJR':	(simplenlg.framework.LexicalCategory.ADJECTIVE, None, None),
	'JJS':	(simplenlg.framework.LexicalCategory.ADJECTIVE, None, None),
	'LS':	(simplenlg.framework.LexicalCategory.ANY, None, None),
	'MD':	(simplenlg.framework.LexicalCategory.MODAL, None, None),
	'NN':	(simplenlg.framework.LexicalCategory.NOUN, False, None),
	'NNS':	(simplenlg.framework.LexicalCategory.NOUN, True, None),
	'NNP':	(simplenlg.framework.LexicalCategory.NOUN, False, None),
	'NNPS':	(simplenlg.framework.LexicalCategory.NOUN, True, None),
	'PDT':	(simplenlg.framework.LexicalCategory.DETERMINER, None, None),
	'POS':	(simplenlg.framework.LexicalCategory.ANY, None, None),
	'PRP':	(simplenlg.framework.LexicalCategory.PRONOUN, None, None),
	'PRP$':	(simplenlg.framework.LexicalCategory.PRONOUN, None, None),
	'RB':	(simplenlg.framework.LexicalCategory.ADVERB, None, None),
	'RBR':	(simplenlg.framework.LexicalCategory.ADVERB, None, None),
	'RBS':	(simplenlg.framework.LexicalCategory.ADVERB, None, None),
	'SYM':	(simplenlg.framework.LexicalCategory.SYMBOL, None, None),
	'TO':	(simplenlg.framework.LexicalCategory.ANY, None, None),
	'UH':	(simplenlg.framework.LexicalCategory.ANY, None, None),
	'VB':	(simplenlg.framework.LexicalCategory.VERB, None, None),
	'VBD':	(simplenlg.framework.LexicalCategory.VERB, None, simplenlg.features.Tense.PAST),
	'VBG':	(simplenlg.framework.LexicalCategory.VERB, None, simplenlg.features.Tense.PRESENT),
	'VBN':	(simplenlg.framework.LexicalCategory.VERB, None, simplenlg.features.Tense.PAST),
	'VBP':	(simplenlg.framework.LexicalCategory.VERB, False, simplenlg.features.Tense.PRESENT),
	'VBZ':	(simplenlg.framework.LexicalCategory.VERB, False, simplenlg.features.Tense.PRESENT),
	'WDT':	(simplenlg.framework.LexicalCategory.DETERMINER, None, None),
	'WP':	(simplenlg.framework.LexicalCategory.PRONOUN, None, None),
	'WP$':	(simplenlg.framework.LexicalCategory.PRONOUN, None, None),
	'WRB':	(simplenlg.framework.LexicalCategory.ADVERB, None, None)
}

def NPhandler(sublist):
	global factory
	generation = factory.createNounPhrase()
	Fnoun = True
	for subsentence in sublist:
		if isinstance(subsentence, simplenlg.framework.WordElement):
			if subsentence.getCategory() == simplenlg.framework.LexicalCategory.DETERMINER:
				generation.setSpecifier(subsentence)
			elif subsentence.getCategory() == simplenlg.framework.LexicalCategory.NOUN:
				if Fnoun:
					generation.setNoun(subsentence)
					Fnoun = False
				else:
					generation.addModifier(subsentence)
		elif isinstance(subsentence, simplenlg.framework.PhraseElement):
			if isinstance(subsentence, simplenlg.phrasespec.NPPhraseSpec):
				if Fnoun:
					generation.setNoun(subsentence)
					Fnoun = False
				else:
					generation.addModifier(subsentence)
			else:
				generation.addModifier(subsentence)
	return generation

def VPhandler(sublist):
	global factory
	generation = factory.createVerbPhrase()
	Fverb = True
	Fobject = True
	for subsentence in sublist:
		if isinstance(subsentence, simplenlg.framework.WordElement):
			if subsentence.getCategory() == simplenlg.framework.LexicalCategory.VERB:
				if Fverb:
					generation.setVerb(subsentence)
					Fverb = False
				else:
					generation.addModifier(subsentence)
			elif subsentence.getCategory() == simplenlg.framework.LexicalCategory.NOUN:
				if Fobject:
					generation.setObject(subsentence)
					Fobject = False
				else:
					generation.addModifier(subsentence)
		elif isinstance(subsentence, simplenlg.framework.PhraseElement):
			if isinstance(subsentence, simplenlg.phrasespec.VPPhraseSpec):
				if Fverb:
					generation.setVerb(subsentence)
					Fverb = False
				else:
					generation.addModifier(subsentence)
			elif isinstance(subsentence, simplenlg.phrasespec.NPPhraseSpec):
				if Fobject:
					generation.setObject(subsentence)
					Fobject = False
				else:
					generation.addModifier(subsentence)
	return generation

phrases = {
	'ADJP':		None,
	'ADVP':		None,
	'CONJP':	None,
	'FRAG':		None,
	'INITJ':	None,
	'LST':		None,
	'NAC':		None,
	'NP':		NPhandler,
	'NX':		None,
	'PP':		None,
	'PRN':		None,
	'PRT':		None,
	'QP':		None,
	'RRC':		None,
	'UCP':		None,
	'VP':		VPhandler,
	'WHADP':	None,
	'WHAVP':	None,
	'WHNP':		None,
	'WHPP':		None,
	'X':		None
}

def Shandler(sublist):
	global factory
	generation = factory.createClause()
	Fsubject = True
	Fverb = True
	for subsentence in sublist:
		if isinstance(subsentence, simplenlg.framework.PhraseElement):
			if isinstance(subsentence, simplenlg.phrasespec.NPPhraseSpec):
				if Fsubject:
					generation.setSubject(subsentence)
					Fsubject = False
				else:
					generation.addModifier(subsentence)
			elif isinstance(subsentence, simplenlg.phrasespec.VPPhraseSpec):
				if Fverb:
					generation.setVerbPhrase(subsentence)
					Fverb = False
				else:
					generation.addModifier(subsentence)
			else:
				generation.addModifier(subsentence)
	return generation

clauses = {
	'S':		Shandler,
	'SBAR':		None,
	'SBARQ':	None,
	'SINV':		None,
	'SQ':		None
}

def handler(parsedlist):
	global factory, words
	if parsedlist[0] in words:
		word = parsedlist[1]
		features = words[parsedlist[0]]
		category = features[0]
		plural = features[1]
		tense = features[2]
		return Whandler(word, category, plural, tense)
	sublist = list()
	for subparse in parsedlist[1: ]:
		subgenerate = handler(subparse)
		if subgenerate is not None:
			sublist.append(subgenerate)
	if parsedlist[0] in phrases:
		return phrases[parsedlist[0]](sublist)
	if parsedlist[0] in clauses:
		return clauses[parsedlist[0]](sublist)
	return None
