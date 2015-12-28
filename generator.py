import jpype
import configurer, logger, pyper

def initialize():
	global online, package, words, phrases, clauses, lexicon, factory, realiser
	if online:
		logger.logger.warn('GENERATOR REINITIALIZATION')
		return
	package = jpype.JPackage('simplenlg')
	words = {
		'CC':	(package.framework.LexicalCategory.CONJUNCTION, None, None),
		'CD':	(package.framework.LexicalCategory.ANY, None, None),
		'DT':	(package.framework.LexicalCategory.DETERMINER, None, None),
		'EX':	(package.framework.LexicalCategory.ANY, None, None),
		'FW':	(package.framework.LexicalCategory.ANY, None, None),
		'IN':	(package.framework.LexicalCategory.PREPOSITION, None, None),
		'JJ':	(package.framework.LexicalCategory.ADJECTIVE, None, None),
		'JJR':	(package.framework.LexicalCategory.ADJECTIVE, None, None),
		'JJS':	(package.framework.LexicalCategory.ADJECTIVE, None, None),
		'LS':	(package.framework.LexicalCategory.ANY, None, None),
		'MD':	(package.framework.LexicalCategory.MODAL, None, None),
		'NN':	(package.framework.LexicalCategory.NOUN, False, None),
		'NNS':	(package.framework.LexicalCategory.NOUN, True, None),
		'NNP':	(package.framework.LexicalCategory.NOUN, False, None),
		'NNPS':	(package.framework.LexicalCategory.NOUN, True, None),
		'PDT':	(package.framework.LexicalCategory.DETERMINER, None, None),
		'POS':	(package.framework.LexicalCategory.ANY, None, None),
		'PRP':	(package.framework.LexicalCategory.PRONOUN, None, None),
		'PRP$':	(package.framework.LexicalCategory.PRONOUN, None, None),
		'RB':	(package.framework.LexicalCategory.ADVERB, None, None),
		'RBR':	(package.framework.LexicalCategory.ADVERB, None, None),
		'RBS':	(package.framework.LexicalCategory.ADVERB, None, None),
		'SYM':	(package.framework.LexicalCategory.SYMBOL, None, None),
		'TO':	(package.framework.LexicalCategory.ANY, None, None),
		'UH':	(package.framework.LexicalCategory.ANY, None, None),
		'VB':	(package.framework.LexicalCategory.VERB, None, None),
		'VBD':	(package.framework.LexicalCategory.VERB, None, package.features.Tense.PAST),
		'VBG':	(package.framework.LexicalCategory.VERB, None, package.features.Tense.PRESENT),
		'VBN':	(package.framework.LexicalCategory.VERB, None, package.features.Tense.PAST),
		'VBP':	(package.framework.LexicalCategory.VERB, False, package.features.Tense.PRESENT),
		'VBZ':	(package.framework.LexicalCategory.VERB, False, package.features.Tense.PRESENT),
		'WDT':	(package.framework.LexicalCategory.DETERMINER, None, None),
		'WP':	(package.framework.LexicalCategory.PRONOUN, None, None),
		'WP$':	(package.framework.LexicalCategory.PRONOUN, None, None),
		'WRB':	(package.framework.LexicalCategory.ADVERB, None, None)
	}
	phrases = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INITJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP', 'RRC', 'UCP', 'VP', 'WHADP', 'WHAVP', 'WHNP', 'WHPP', 'X']
	clauses = ['S', 'SBAR', 'SBARQ', 'SINV', 'SQ']
	lexicon = package.lexicon.Lexicon.getDefaultLexicon()
	factory = package.framework.NLGFactory(lexicon)
	realiser = package.realiser.english.Realiser(lexicon)
	online = True
	logger.logger.info('GENERATOR INITIALIZATION')

def Wgenerator(word, category, plural, tense):
	global online, factory
	if not online:
		return
	word = factory.createNLGElement(word)
	if category is not None:
		word.setCategory(category)
	if plural is not None:
		word.setPlural(plural)
	if tense is not None:
		word.setTense(tense)
	logger.logger.debug('GENERATOR(W) OUTPUT <' + str(word.toString()) + '>')
	return word

def NPgenerator(sublist):
	global online, factory
	if not online:
		return None
	generation = factory.createNounPhrase()
	Fnoun = True
	for subsentence in sublist:
		if isinstance(subsentence, package.framework.WordElement):
			if subsentence.getCategory() == package.framework.LexicalCategory.DETERMINER:
				generation.setSpecifier(subsentence)
			elif subsentence.getCategory() == package.framework.LexicalCategory.NOUN:
				if Fnoun:
					generation.setNoun(subsentence)
					Fnoun = False
				else:
					generation.addModifier(subsentence)
		elif isinstance(subsentence, package.framework.PhraseElement):
			if isinstance(subsentence, package.phrasespec.NPPhraseSpec):
				if Fnoun:
					generation.setNoun(subsentence)
					Fnoun = False
				else:
					generation.addModifier(subsentence)
			else:
				generation.addModifier(subsentence)
	logger.logger.debug('GENERATOR(NP) OUTPUT <' + str(generation.toString()) + '>')
	return generation

def VPgenerator(sublist):
	global online, factory
	if not online:
		return
	generation = factory.createVerbPhrase()
	Fverb = True
	Fobject = True
	for subsentence in sublist:
		if isinstance(subsentence, package.framework.WordElement):
			if subsentence.getCategory() == package.framework.LexicalCategory.VERB:
				if Fverb:
					generation.setVerb(subsentence)
					Fverb = False
				else:
					generation.addModifier(subsentence)
			elif subsentence.getCategory() == package.framework.LexicalCategory.NOUN:
				if Fobject:
					generation.setObject(subsentence)
					Fobject = False
				else:
					generation.addModifier(subsentence)
		elif isinstance(subsentence, package.framework.PhraseElement):
			if isinstance(subsentence, package.phrasespec.VPPhraseSpec):
				if Fverb:
					generation.setVerb(subsentence)
					Fverb = False
				else:
					generation.addModifier(subsentence)
			elif isinstance(subsentence, package.phrasespec.NPPhraseSpec):
				if Fobject:
					generation.setObject(subsentence)
					Fobject = False
				else:
					generation.addModifier(subsentence)
	logger.logger.debug('GENERATOR(VP) OUTPUT <' + str(generation.toString()) + '>')
	return generation

def Sgenerator(sublist):
	global online, factory
	if not online:
		return
	generation = factory.createClause()
	Fsubject = True
	Fverb = True
	for subsentence in sublist:
		if isinstance(subsentence, package.framework.PhraseElement):
			if isinstance(subsentence, package.phrasespec.NPPhraseSpec):
				if Fsubject:
					generation.setSubject(subsentence)
					Fsubject = False
				else:
					generation.addModifier(subsentence)
			elif isinstance(subsentence, package.phrasespec.VPPhraseSpec):
				if Fverb:
					generation.setVerbPhrase(subsentence)
					Fverb = False
				else:
					generation.addModifier(subsentence)
			else:
				generation.addModifier(subsentence)
	logger.logger.debug('GENERATOR(S) OUTPUT <' + str(generation.toString()) + '>')
	return generation

def generator(parsedlist):
	global online, words, phrases, clauses
	if not online:
		return
	if parsedlist[0] in words:
		word = parsedlist[1]
		features = words[parsedlist[0]]
		return Wgenerator(word, features[0], features[1], features[2])
	sublist = list()
	for subparse in parsedlist[1: ]:
		subgenerate = generator(subparse)
		if subgenerate is not None:
			sublist.append(subgenerate)
	if parsedlist[0] in phrases:
		return globals()[parsedlist[0] + 'generator'](sublist)
	if parsedlist[0] in clauses:
		return globals()[parsedlist[0] + 'generator'](sublist)
	return

def generate(parsedlist):
	global online, realiser
	if not online:
		logger.logger.warn('UNINITIALIZED GENERATOR INPUT <' + str(parsedlist) + '>')
		return
	logger.logger.debug('GENERATOR INPUT <' + str(parsedlist) + '>')
	generation = generator(parsedlist)
	realisation = str(realiser.realise(generation))
	logger.logger.info('GENERATOR OUTPUT <' + realisation + '>')
	return realisation

def terminate():
	global online
	if not online:
		logger.logger.warn('UNINITIALIZED GENERATOR TERMINATION')
		return
	online = False
	logger.logger.info('GENERATOR TERMINATION')

pyper.addclasspath(configurer.simplenlg)
online = False
words = None
phrases = None
clauses = None
lexicon = None
factory = None
realiser = None
logger.logger.info('GENERATOR CREATION')
