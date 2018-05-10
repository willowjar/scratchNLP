from generate_vocab import generate_vocab_list
from generate_vocab import add_unknowns_to_grammar

# Generate fixed base vocabulary
generate_vocab_list('../test_fixtures/vocab.gr')

# Create combined grammar.
final_grammar_path = "../test_fixtures/GRAMMAR.gr"
final_grammar = open(final_grammar_path, "w+")
with open('../test_fixtures/grammar_base.gr', 'r') as base:
	with open('../test_fixtures/vocab.gr', 'r')as vocab:
		final_grammar.write(base.read())
		final_grammar.write(vocab.read())
final_grammar.close()

print 'generated GRAMMAR.gr...'

grammar_copy_path = 'GRAMMAR_copy.gr'
final_grammar = open(final_grammar_path, "r")
with open(grammar_copy_path, 'w+') as grammar_copy:
	grammar_copy.write(final_grammar.read())
final_grammar.close()
print 'generated GRAMMAR_copy.gr...'

with open("../test_fixtures/tina_test_sentences", "r") as test_sentences:
	with open("../test_fixtures/processed_test_sentences", "w+") as processed:
		for sentence in test_sentences.readlines():
			print 'read sentence:' + sentence
			new_sentence = add_unknowns_to_grammar(sentence, grammar_copy_path)
			processed.write(new_sentence + '\n')