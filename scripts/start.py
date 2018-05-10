from generate_vocab import generate_vocab_list

# Generate fixed base vocabulary
generate_vocab_list('../test_fixtures/vocab.gr')

# Create combined grammar.
with open("../test_fixtures/GRAMMAR.gr", "w+") as final_grammar:
	with open('../test_fixtures/grammar_base.gr', 'r') as base:
		with open('../test_fixtures/vocab.gr', 'r')as vocab:
			final_grammar.write(base.read())
			final_grammar.write(vocab.read())
